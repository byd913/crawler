#encoding=utf-8

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
from logging.handlers import TimedRotatingFileHandler

from bjguahao_login import BjguahaoLogin

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
                                                                                 

if __name__ == "__main__":
    init_log()

    hospital_id = 142
    department_id = 200039608

    cookie = BjguahaoLogin('*******', '*******').get_cookie()
    logging.getLogger('server').info('login|cookie=%s' % (cookie))

    headers = {'Cookie': cookie}
    data = {
       "hospitalId": hospital_id,
       "departmentId": department_id,
       "dutyCode": 2,
       "dutyDate": '2018-11-29',
       "isAjax": True
    }

    request_times = 6
    finished = False
    while request_times >= 0 and not finished:
        request = urllib2.Request(url='http://www.bjguahao.gov.cn/dpt/partduty.htm',
                                data=urllib.urlencode(data), headers=headers)
        duty_data = json.loads(urllib2.urlopen(request).read())
        
        logging.getLogger('server').info('get duty data|data=%s' % (json.dumps(duty_data)))
        duty_list = filter(lambda item: item['doctorTitleName'].find(u'专家') != -1 or
                        item['doctorTitleName'].find(u'主任') != -1, duty_data['data'])
        if len(duty_data['data']) > 0:
            finished = True
        request_times -= 1
        time.sleep(1)

    choosed_duty = duty_list[0]
    request = urllib2.Request(url='http://www.bjguahao.gov.cn/v/sendorder.htm',
                                data=urllib.urlencode({}), headers=headers)
    ret_data = json.loads(urllib2.urlopen(request).read())

    register_data = {
        "dutySourceId": choosed_duty['dutySourceId'],
        "hospitalId": hospital_id,
        "departmentId": department_id,
        "doctorId": choosed_duty['doctorId'],
        "patientId": 239452730,
        "hospitalCardId": '',
        "medicareCardId": '',
        "reimbursementType": -1,
        "smsVerifyCode": 1234,
        "childrenBirthday": '',
        "isAjax": True
    }

    verify_code = input('输入短信验证码:')
    register_data['smsVerifyCode'] = int(verify_code)
    request = urllib2.Request(url='http://www.bjguahao.gov.cn/order/confirmV1.htm',
                                data=urllib.urlencode(register_data), 
                                headers=headers)
    data = urllib2.urlopen(request).read()
    ret_data = json.loads(data)
    
