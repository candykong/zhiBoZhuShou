from locust import User, task, events, constant,HttpUser
import time
import websocketnew
import ssl
import json
import jsonpath
from random import randint
import pytest
import pymysql

import socket




#设置默认超时时间
timeout = 20
socket.setdefaulttimeout(timeout)

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

    def connect(self, burl):
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url=burl)
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
        return self.conn

    def recv(self):
        return self.ws.recv()

    def send(self, msg):
        self.ws.send(msg)


class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


class TestApiUser(WebsocketUser):
    host = "http://dev-live-assistant.zhiyitech.cn"
    # host = 'ws://116.62.106.122:5111/'
    wait_time = constant(0)


    # 使用随机方式取出组货详情要编辑的内容：activityGoodsID,fieldName,fieldValue
    def on_start(self):
        activity_id = 860

        #查询组货详情的activityGoodsIds
        sql = "select a.`id` from `live_assistant_temp`.`tb_activity_goods` a where a.`activity_id`={activity_id} and a.`related_status`=1;".format(
            activity_id=activity_id)
        activityGoodsIds = selectSql(sql)
        # activityGoodsId=['4569','4566']
        ranIndex1 = randint(0, len(activityGoodsIds) - 1)

        #字段对应内容
        value = ["888", "777"]
        ranIndex2 = randint(0, len(value) - 1)

        #将详情编辑信息放在一个列表中
        self.activity=[activityGoodsIds[ranIndex1][0],value[ranIndex2]]
        return self.activity

    @task(1)
    # @pytest.mark.parametrize('activityGoodsId',[4569,4566])
    # @pytest.mark.parametrize('value', ["900","999"])
    def test_pft(self):
        self.url='ws://116.62.106.122:5111/?sid=860missionGoodsDetail&token=2777af36-d4f0-48a1-910c-0bb1a9711730'
        data ='{"optionType":"2","deptType":"1","activityGoodsId":'+str(self.activity[0])+',"fieldName":"minPrice","value":'+self.activity[1]+',"action":"EDIT_FIELD"}'
        print(data)
        self.client.connect(self.url)
        # 修改历史最低价
        self.client.send(data)
        while True:
            # 消息接收计时
            start_time = time.time()
            recv = self.client.recv()
            total_time = int((time.time() - start_time) * 1000)
            # 为每个推送过来的事件进行归类和独立计算性能指标
            try:
                recv_j = json.loads(recv)
                eventType_s = jsonpath.jsonpath(recv_j, expr='$.eventType')
                eventType_success(eventType_s[0], recv, total_time)
            except websocketnew.WebSocketConnectionClosedException as e:
                events.request_failure.fire(request_type="[ERROR] WebSocketConnectionClosedException",
                                            name='Connection is already closed.',
                                            response_time=total_time,
                                            exception=e)
            except:
                print(recv)
                # 正常 OK 响应，或者其它心跳响应加入进来避免当作异常处理
                if 'ok' in recv:
                    eventType_success('ok', 'ok', total_time)

