# -*- encoding:utf-8 -*-
from locust import User, task, events, constant,HttpUser
import time
import websocketnew
import ssl
import json
import jsonpath
import pytest
import pymysql
from threading import Thread
from  gevent._semaphore import Semaphore


host='rm-bp1ghcqu341s7aqoj.mysql.rds.aliyuncs.com'
port=3306
user='kongzhibing'
passwd='Kongzhibingqwer123456'


def selectSql(sql):
    db = pymysql.connect(
        host=host,
        port=port,
        user=user,
        passwd=passwd,
        charset='utf8')
    cursor = db.cursor()
    cursor.execute(sql)
    data = list(cursor.fetchall())
    return data



#TODO:设置集合点
# all_locusts_spawned = Semaphore()
# all_locusts_spawned.acquire()


def on_message(ws, message):
    print(message)


# 重新实现对应事件
def on_error(ws, error):
    print("occur error " + error)


def on_close(ws):
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^con is closed^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


def on_open(ws):
    # data = '{"optionType":"2","deptType":"1","activityGoodsId":4907,"fieldName":"minPrice","value":"66","action":"EDIT_FIELD"}'
    # ws.send(data)
    # 查询组货详情字段
    def run(*args):
        """
        修改各个商品各个字段的信息
        :param args:
        :return:
        """
        activity_id = 885
        # 查询组货详情中的商品id
        sql = "select a.`id` from `live_assistant_temp`.`tb_activity_goods` a where a.`activity_id`={activity_id} and a.`related_status`=1;".format(
            activity_id=activity_id)
        activityGoodsIds = selectSql(sql)
        for activityGoodsId in activityGoodsIds:
            # 查询商品的默认字段名
            activityGoodsId = activityGoodsId[0]
            sql = "select a.`field_name` from `live_assistant_temp`.`tb_activity_goods_field` a where a.`activity_goods_id`={activityGoodsId} and a.`field_type`=1 and a.`deleted_at` is null".format(
                activityGoodsId=activityGoodsId)
            defaultFieldNames = selectSql(sql)
            for defaultFieldName in defaultFieldNames:
                defaultFieldName = defaultFieldName[0]
                values = ['2222']
                for value in values:
                    standard = {"optionType": "2", "deptType": "2", "activityGoodsId": activityGoodsId,
                                "fieldName": defaultFieldName, "value": value,
                                "action": "EDIT_FIELD".format(defaultFieldName=defaultFieldName)}
                    print(standard)
                    ws.send(json.dumps(standard))
                    time.sleep(2)
        time.sleep(1)
        ws.close()


def eventType_success(eventType, recvText, total_time):
    events.request_success.fire(request_type="[RECV]",
                                name=eventType,
                                response_time=total_time,
                                response_length=len(recvText))


class WebSocketClient(object):
    _locust_environment = None

    def __init__(self, host):
        self.host = host
        # 针对 WSS 关闭 SSL 校验警报
        self.ws = websocketnew.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

    def connect(self):
        start_time = time.time()
        try:
            self.ws = websocketnew.WebSocketApp(self.host,
                                                on_message = on_message,
                                                on_error = on_error,
                                                on_open = on_open,
                                                on_close=on_close,)
            self.ws.run_forever()
        except websocketnew.WebSocketConnectionClosedException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='Connection is already closed', response_time=total_time, exception=e)
        except websocketnew.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type="[Connect]", name='TimeOut', response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(
                request_type="[Connect]", name='WebSocket', response_time=total_time, response_length=0)



    def execut(self):
        self.ws.run_forever()


class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


class ApiUser(WebsocketUser):
    host = 'ws://116.62.106.122:5111/?sid=860missionGoodsDetail&token=2777af36-d4f0-48a1-910c-0bb1a9711730'
    wait_time = constant(0)

    # def on_start(self):
    #     self.client.connect()
    #     all_locuts_spwned.wait()

    @task
    def executLONG(self):
        self.client.connect()



