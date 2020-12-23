
import websocketnew
from websocketnew import create_connection





if __name__ == '__main__':
    websocketnew.enableTrace(True)
    SERVER_URL = 'ws://116.62.106.122:5111/?sid=860missionGoodsDetail&token=2777af36-d4f0-48a1-910c-0bb1a9711730'
    # 如果想要通信一条短消息，并在完成后立即断开连接，我们可以使用短连接：
    ws = create_connection(SERVER_URL)
    print('修改页面价')
    ws.send('{"optionType":"2","deptType":"2","activityGoodsId":4566,"fieldName":"dailyPrice","value":689,"action":"EDIT_FIELD"}')
    result = ws.recv()
    print("Received '%s'" %result)
    ws.close()
