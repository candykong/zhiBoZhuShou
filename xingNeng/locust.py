#! /usr/bin/python
# coding=utf-8



__author__ = 'qiangweo'


from locust import HttpUser, task,between
import json

"""
#模拟3个用户同时登陆
class Zhibo(HttpUser):
    host = "http://dev-live-assistant.zhiyitech.cn"
    wait_time = between(1,2)


    #使用随机方式登陆
    def on_start(self):
        self.login_data = ['09876543215', '09876543217', '13107700873']
        self.ranIndex = randint(0, len(self.login_data) - 1)
        username=self.login_data[self.ranIndex]
        playload = {
            "mobile": username,
            "messageCode": "qwe123"
        }
        response = self.client.post("/security-api/login", json=playload)
        json_dict = json.loads(response.text, strict=False)
        if json_dict['success'] == True:
            self.token = json_dict['result']['token']
            print(self.token)
        else:
            print("fails")

    @task(1)
    def index_page(self):
        params = {}
        print("验证是否调用不同的token:",self.token)
        headers = {
            'Content-Type': 'application/json',
            'token': self.token
        }
        with self.client.post("/security-api/v2/user-info", json=params, headers=headers,
                              catch_response=True) as response:
            json_dict = json.loads(response.text, strict=False)
            # print(json_dict)
            if json_dict['success'] == True:
                response.success()
            else:
                response.failure('Failed')
        # 使用assert json_dict['success'] ==True断言是一样的
"""

"""
    #使用队列的方式登陆
    def fifoLogin(self):
        #使用队列
        userQueue = queue.Queue()
        usernames = ['09876543215', '09876543217', '13107700873']
        for username in usernames:
            userQueue.put(username)
        playload = {
            "mobile": userQueue.get(),
            "messageCode": "qwe123"
        }
        response=self.client.post("/security-api/login", json=playload)
        json_dict = json.loads(response.text, strict=False)
        if json_dict['success'] ==True:
            self.token=json_dict['result']['token']
            print(self.token)
        else:
            print("fails")
"""



"""
#该方式不知道为什么总调用不了taskset
class Zhibo(TaskSet):
    host = "http://dev-live-assistant.zhiyitech.cn"
    wait_time = between(1, 2)

    def on_start(self):
        playload = {
            "mobile": "13107700873",
            "messageCode": "qwe123"
        }
        header = {
            "Accept": "application / json, text / plain, * / *"
        }
        self.client.post("/security-api/login", data=playload, headers=header)

class websitUser(HttpUser):
    tasks = [Zhibo]
    min_wait = 3000
    max_wait = 6000
"""


class Zhibo(HttpUser):
    host = "http://dev-live-assistant.zhiyitech.cn"
    wait_time = between(1,2)

    def on_start(self):
        playload = {
            "mobile": "15088688475",
            "messageCode": "asd456"
        }
        response=self.client.post("/security-api/login", json=playload)
        json_dict = json.loads(response.text, strict=False)
        if json_dict['success'] ==True:
            self.token=json_dict['result']['token']
            print(self.token)
        else:
            print("fails")

    @task(1)
    def activityDetail(self):
        params = {
            "goodsId":"",
            "goodsName":"",
            "shopName":"",
            "rootCategoryId":"",
            "categoryId":"",
            "rootCategoryName":"",
            "categoryName":"",
            "id":"495",
            "deptType":"1",
            "optionType":2
            }
        headers = {
            'Content-Type': 'application/json',
            'token': self.token
        }
        with self.client.post("/live-assistant/v1_0/activity/detail", json=params, headers=headers,
                              catch_response=True) as response:
            json_dict = json.loads(response.text, strict=False)
            # print(json_dict)
            if json_dict['success'] == True:
                response.success()
            else:
                response.failure('Failed')

    @task(1)
    def activityGoods(self):
        params = {
            "goodsId":"",
            "goodsName":"",
            "shopName":"",
            "rootCategoryId":"",
            "categoryId":"",
            "rootCategoryName":"",
            "categoryName":"",
            "id":"495",
            "deptType":"1",
            "optionType":2
            }
        headers = {
            'Content-Type': 'application/json',
            'token': self.token
        }
        with self.client.post("/live-assistant/v1_0/activity-detail/goods-list", json=params, headers=headers,
                              catch_response=True) as response:
            json_dict = json.loads(response.text, strict=False)
            # print(json_dict)
            if json_dict['success'] == True:
                response.success()
            else:
                response.failure('Failed')

    # @task(1)
    # def index_page(self):
    #     params={}
    #     headers={
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/security-api/v2/user-info",json=params,headers=headers,catch_response=True) as response:
    #         json_dict=json.loads(response.text,strict=False)
    #         #print(json_dict)
    #         if json_dict['success'] ==True:
    #             response.success()
    #         else:
    #             response.failure('Failed')
    #     #使用assert json_dict['success'] ==True断言是一样的
    #
    # @task(2)
    # def get_schedual(self):
    #     playload = {
    #         "startLiveDate":"2020-10-07",
    #         "endLiveDate":"2020-11-06"
    #     }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'token': self.token
    #     }
    #     with self.client.post("/live-assistant/v2_8/schedule/list",json=playload,headers=headers,catch_response=True) as response:
    #         json_dict = json.loads(response.text, strict=False)
    #         #print(json_dict)
    #         if json_dict['success'] == True:
    #             response.success()
    #         else:
    #             response.failure('Failed')


"""
if __name__ == "__main__":
    import os
    os.system("locust -f locust.py --host=http://dev-live-assistant.zhiyitech.cn")
"""

