from locust import User, task, events, constant
import time
import websocketnew
import ssl
import json
import jsonpath
from random import randint
import pytest



def eventType_success(eventType, recvText, total_time):
    events.request_success.fire(request_type="[RECV]",
                                name=eventType,
                                response_time=total_time,
                                response_length=len(recvText))


class WebSocketClient(object,websocketnew.WebSocketApp):
    _locust_environment = None

    def __init__(self, host):
        self.host = host
        # 针对 WSS 关闭 SSL 校验警报
        self.ws = websocketnew.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})

    def on_message(ws, message):
        print(message)

    def on_errors(ws, error):

        print(error)

    def on_close(ws):
        print("close connection")

    def on_open(ws):
        # 查询组货详情字段
        def run(*args):
            """
            修改各个商品各个字段的信息
            :param args:
            :return:
            """
            standard = {"optionType": "2", "deptType": "2", "activityGoodsId": 4921, "fieldName": "dailyPrice",
                        "value":1, "action": "EDIT_FIELD"}
            ws.send(json.dumps(standard))
            time.sleep(2)
        ws.close()
        Thread(target=run).start()



class WebsocketUser(User):
    abstract = True

    def __init__(self, *args, **kwargs):
        super(WebsocketUser, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)
        self.client._locust_environment = self.environment


class ApiUser(WebsocketUser):
    host = "http://dev-live-assistant.zhiyitech.cn"
    wait_time = constant(0)

    # 使用随机方式登陆
    def on_start(self):
        self.login_data = ['90000000001', '90000000002']
        self.ranIndex = randint(0, len(self.login_data) - 1)
        mobile = self.login_data[self.ranIndex]
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
    @pytest.mark.parametrize('value', ["900","999"])
    def pft(self):
        # wss 地址
        self.url = 'ws://116.62.106.122:5111/?sid=681missionGoodsDetail&token='+self.token
        print(self.url)
        self.data = {}
        self.client.connect(self.url)
        # 修改历史最低价
        self.client.send('{"optionType":"2","deptType":"1","activityGoodsId":4665,"fieldName":"minPrice","value":{value},"action":"EDIT_FIELD"}')
        while True:
            # 消息接收计时
            start_time = time.time()
            recv = self.client.recv()
            total_time = int((time.time() - start_time) * 1000)
            print(recv)
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
