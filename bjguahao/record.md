# 爬虫的步骤

## 获取空余信息

1. request

[get doc list](http://www.bjguahao.gov.cn/dpt/partduty.htm)

```json
hospitalId: 142
departmentId: 200039618
dutyCode: 2
dutyDate: 2018-11-27
isAjax: true
```

2. response

```json
{
    "data": [
        {
            "dutySourceId": 58667730,
            "portrait": "",
            "doctorName": "韩彤妍",
            "doctorTitleName": "特需专家号二100",
            "skill": "儿童保",
            "totalFee": 100,
            "remainAvailableNumber": 1,
            "dutySourceStatus": 1,
            "hospitalId": 142,
            "departmentId": "200039618",
            "doctorId": "201156292",
            "drCode": null,
            "planCode": null,
            "dutyDate": null,
            "dutyCode": null,
            "departmentName": null,
            "isShowFee": 1,
            "dlDutySources": null,
            "morningnum": 0,
            "afternoonnum": 0,
            "majorName": null,
            "majorIntroduce": null,
            "dldutyDate": null,
            "dldutyCode": null,
            "regNo": 0
        },
        {
            "dutySourceId": 58667722,
            "portrait": "",
            "doctorName": "朴梅花",
            "doctorTitleName": "特需专家号三200",
            "skill": "新生儿疾病、儿童保健",
            "totalFee": 200,
            "remainAvailableNumber": 1,
            "dutySourceStatus": 1,
            "hospitalId": 142,
            "departmentId": "200039618",
            "doctorId": "201154956",
            "drCode": null,
            "planCode": null,
            "dutyDate": null,
            "dutyCode": null,
            "departmentName": null,
            "isShowFee": 1,
            "dlDutySources": null,
            "morningnum": 0,
            "afternoonnum": 0,
            "majorName": null,
            "majorIntroduce": null,
            "dldutyDate": null,
            "dldutyCode": null,
            "regNo": 0
        }
    ],
    "hasError": false,
    "code": 200,
    "msg": "OK"
}
```

## 挂号网页单

[guahao_page](http://www.bjguahao.gov.cn/order/confirm/{hospitalId}-{departmentId}-{doctorId}-{dutySourceId}.htm)

## short message code

[send short message](http://www.bjguahao.gov.cn/v/sendorder.htm)

## message conform

[message conform](http://www.bjguahao.gov.cn/order/confirmV1.htm)

```json
dutySourceId: 58667730
hospitalId: 142
departmentId: 200039618
doctorId: 201156292
patientId: 233695148
hospitalCardId: 
medicareCardId: 
reimbursementType: -1
smsVerifyCode: 134555
childrenBirthday: 
isAjax: true
```

```json
dutySourceId: 58802486
hospitalId: 142
departmentId: 200039490
doctorId: 201157204
patientId: 233695148
hospitalCardId: 
medicareCardId: 
reimbursementType: -1
smsVerifyCode: 1234
childrenBirthday: 
isAjax: true
```

```json
dutySourceId: 58802486
hospitalId: 142
departmentId: 200039490
doctorId: 201157204
patientId: 239452730
hospitalCardId: 
medicareCardId: 
reimbursementType: -1
smsVerifyCode: 1234
childrenBirthday: 
isAjax: true
```