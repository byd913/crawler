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

from bjguahao_login import BjguahaoLogin


if __name__ == "__main__":
    hospital_id = 142
    department_id = 200039490

    cookie = BjguahaoLogin('*********', '***********').get_cookie()

    headers = {'Cookie': cookie}
    data = {
       "hospitalId": 142,
       "departmentId": 200039490,
       "dutyCode": 2,
       "dutyDate": '2018-12-01',
       "isAjax": True
    }
    request = urllib2.Request(url='http://www.bjguahao.gov.cn/dpt/partduty.htm',
                              data=urllib.urlencode(data), headers=headers)
    duty_data = json.loads(urllib2.urlopen(request).read())
    
    # if len(duty_data['data']) > 0:
    request = urllib2.Request(url='http://www.bjguahao.gov.cn/v/sendorder.htm',
                                data=urllib.urlencode({}), headers=headers)
    ret_data = json.loads(urllib2.urlopen(request).read())
    if int(ret_data['code']) != 200:
        pass
    print ret_data

    register_data = {
        "dutySourceId": duty_data['data'][0]['dutySourceId'],
        "hospitalId": hospital_id,
        "departmentId": department_id,
        "doctorId": duty_data['data'][0]['doctorId'],
        "patientId": 233695148,
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
    print data
    ret_data = json.loads(data)
    