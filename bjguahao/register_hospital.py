# encoding=utf-8

''' 根据医院、科室和日期选择自动挂号

整体的步骤如下:
1. 模拟登陆获取cookie信息
2. 获取对应医院、科室当天的医生情况
3. 填写手机号获取短信验证码
4. 提交验证码表单进行挂号
'''

import urllib
import urllib2
import json
import os
import logging
import time
import configparser
from logging.handlers import TimedRotatingFileHandler

from bjguahao_login import BjguahaoLogin

VR_CODE_FILE = '/home/xiaoju/data/hospital/vr_code.txt'
CUR_PATH = os.path.abspath(os.path.dirname(__file__))


def init_log():
    if not os.path.exists('log'):
        os.makedirs('log')

    server_log = logging.getLogger('server')
    rotating_handler = TimedRotatingFileHandler(filename='log/crawler.log', when='midnight')
    formatter = logging.Formatter(
        '%(levelname)s\t%(asctime)s\t[%(thread)d]\t[%(filename)s:%(lineno)d]\t%(message)s')
    rotating_handler.setFormatter(formatter)
    rotating_handler.suffix = 'log.%Y-%m-%d'
    server_log.addHandler(rotating_handler)
    server_log.setLevel(logging.INFO)


if __name__ == "__main__":
    init_log()
    if os.path.exists(VR_CODE_FILE):
        os.remove(VR_CODE_FILE)

    hospital_id = 142
    # department_id = 200039608
    department_id = 200039490
    patient_id = 239452730

    cf = configparser.ConfigParser()
    cf.read(os.path.join(CUR_PATH, 'crawler.conf'))
    user = cf.get('login', 'user')
    passwd = cf.get('login', 'passwd')

    cookie = BjguahaoLogin(user, passwd).get_cookie()
    logging.getLogger('server').info('login|cookie=%s' % (cookie))

    headers = {'Cookie': cookie}
    data = {
       "hospitalId": hospital_id,
       "departmentId": department_id,
       "dutyCode": 2,
       "dutyDate": '2018-12-06',
       "isAjax": True
    }

    request_times = 6
    finished = False
    while request_times >= 0 and not finished:
        request = urllib2.Request(url='http://www.bjguahao.gov.cn/dpt/partduty.htm',
                                  data=urllib.urlencode(data), headers=headers)
        content = urllib2.urlopen(request).read()
        duty_data = json.loads(content)

        logging.getLogger('server').info('get duty data|data=%s' % (content))
        # duty_list = filter(lambda item: item['doctorTitleName'].find(u'专家') != -1 or
        # item['doctorTitleName'].find(u'主任') != -1, duty_data['data'])
        duty_list = duty_data['data']
        if len(duty_list) > 0:
            finished = True
        request_times -= 1
        time.sleep(1)
    if not finished:
        logging.getLogger('server').info('No doctor reday')
        exit(1)
    choosed_duty = duty_list[0]

    request = urllib2.Request(url='http://www.bjguahao.gov.cn/v/sendorder.htm',
                              data=urllib.urlencode({}), headers=headers)
    content = urllib2.urlopen(request).read()
    ret_data = json.loads(content)
    logging.getLogger('server').info('send order|message=%s' % (content))

    wait_minites = 10
    start_time = time.time()
    # while (not os.path.exists(VR_CODE_FILE) and
    #        int(time.time() - start_time) <= wait_minites * 60):
    #     time.sleep(30)

    # if not os.path.exists(VR_CODE_FILE):
    #     logging.getLogger('server').warn('wait for %s minutes for vr code fail'
    #                                      % (wait_minites))
    #     exit(1)

    # verify_code = open(VR_CODE_FILE).read()
    verify_code = raw_input('input vr code:')
    post_data = ('dutySourceId=%s&hospitalId=%s&departmentId=%s&doctorId=%s&patientId=%s'
                 '&hospitalCardId=&medicareCardId=&reimbursementType=-1&smsVerifyCode=%s'
                 '&childrenBirthday=&isAjax=true'
                 % (choosed_duty['dutySourceId'], hospital_id, department_id, choosed_duty['doctorId'],
                    patient_id, verify_code))
    logging.getLogger('server').info('short message conform|data=%s'
                                     % (post_data))
    request = urllib2.Request(url='http://www.bjguahao.gov.cn/order/confirmV1.htm',
                              data=post_data,
                              headers=headers)
    data = urllib2.urlopen(request).read()
    ret_data = json.loads(data)
    logging.getLogger('server').info('ret_data=%s' % (data))
