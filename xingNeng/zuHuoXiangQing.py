#! /usr/bin/python
# coding=utf-8
from random import randint

__author__ = 'qiangweo'



from locust import HttpUser, task,between
import json

#模拟3个用户同时登陆
class Zhibo(HttpUser):
    host = "http://dev-live-assistant.zhiyitech.cn"
    wait_time = between(1,2)


    #使用随机方式登陆
    def on_start(self):
        self.login_data = ['90000000001', '90000000002',
                           '90000000003','90000000004',
                           '90000000005','90000000006',
                           '90000000007','90000000008',
                           '90000000009','900000000010',
                           '90000000011','90000000012',
                           '90000000013','90000000014',
                           '90000000015','90000000016',
                           '90000000017','90000000018',
                           '90000000019','90000000020',
                           '90000000021','90000000022',
                           '90000000023','90000000024',
                           '90000000025','90000000026',
                           '90000000027','90000000028',
                           '90000000029','90000000030',
                           '90000000031','90000000031',
                           '90000000033','90000000034',
                           '90000000035','90000000036',
                           '90000000037','90000000038',
                           '90000000039','90000000040',
                           '90000000041','90000000042',
                           '90000000043','90000000044',
                           '90000000045','90000000046',
                           '90000000047','90000000048',
                           '90000000049','90000000050']
        self.ranIndex = randint(0, len(self.login_data) - 1)
        mobile=self.login_data[self.ranIndex]
        playload = {
            "mobile": mobile,
            "messageCode": "asd456"
        }
        response = self.client.post("/security-api/login", json=playload)
        json_dict = json.loads(response.text, strict=False)
        if json_dict['success'] == True:
            self.token = json_dict['result']['token']
            print(self.token)
        else:
            print("fails")

    @task(1)
    def activityGoodsListV2(self):
        """
        组货详情商品接口改造
        :return:
        """
        print("验证是否调用不同的token:", self.token)
        params = {
            "deptType":"1",
            "id":"860",
            "optionType":"2"
        }
        headers = {
            'Content-Type': 'application/json',
            'token': self.token
        }
        with self.client.post("/live-assistant/v1_0/activity-detail/goods-list-v2", json=params, headers=headers,
                              catch_response=True) as response:
            json_dict = json.loads(response.text, strict=False)
            print(json_dict)
            if json_dict['success'] == True:
                response.success()
            else:
                response.failure('Failed')
    #
    # @task(1)
    # def activityFieldRelatedList(self):
    #     """
    #     组货商品关联字段
    #     :return:
    #     """
    #     params = {
    #         "deptType": "1",
    #         "id": "860",
    #         "optionType": "2"
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v1_0/activity-detail/field-related-list", json=params, headers=headers,
    #                           catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         # print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')
    #
    # @task(1)
    # def activityLLogisticsRelatedList(self):
    #     """
    #     组货商品关联字段
    #     :return:
    #     """
    #     print("验证是否调用不同的token:", self.token)
    #     params = {
    #         "deptType": "1",
    #         "id": "860",
    #         "optionType": "2"
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v1_0/activity-detail/logistics-related-list", json=params, headers=headers,
    #                           catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         # print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')
    #
    # @task(1)
    # def activityProgramList(self):
    #     """
    #     组货商品活动
    #     :return:
    #     """
    #     print("验证是否调用不同的token:", self.token)
    #     params = {
    #         "deptType": "1",
    #         "id": "860",
    #         "optionType": "2"
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v1_0/activity-detail/program-list", json=params,
    #                           headers=headers,
    #                           catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         # print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')
    #
    # @task(1)
    # def activitySalePointList(self):
    #     """
    #     组货商品卖点
    #     :return:
    #     """
    #     print("验证是否调用不同的token:", self.token)
    #     params = {
    #         "deptType": "1",
    #         "id": "860",
    #         "optionType": "2"
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v1_0/activity-detail/sale-point-list", json=params,
    #                           headers=headers,
    #                           catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         # print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')

    # @task(1)
    # def activityDetail(self):
    #     params = {
    #         "goodsId": "",
    #         "goodsName": "",
    #         "shopName": "",
    #         "rootCategoryId": "",
    #         "categoryId": "",
    #         "rootCategoryName": "",
    #         "categoryName": "",
    #         "id": "860",
    #         "deptType": "1",
    #         "optionType": 2
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v1_0/activity/detail", json=params, headers=headers,
    #                           catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         # print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')
    #
    # @task(1)
    # def activityGoods(self):
    #     params = {
    #         "goodsId": "",
    #         "goodsName": "",
    #         "shopName": "",
    #         "rootCategoryId": "",
    #         "categoryId": "",
    #         "rootCategoryName": "",
    #         "categoryName": "",
    #         "id": "860",
    #         "deptType": "1",
    #         "optionType": 2
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v1_0/activity-detail/goods-list", json=params, headers=headers,
    #                           catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         # print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')



"""
if __name__ == "__main__":
    import os
    os.system("locust -f locust.py --host=http://dev-live-assistant.zhiyitech.cn")
"""

