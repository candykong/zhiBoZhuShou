
import json
import time
import _thread

import pymysql
import websocketnew
from threading import Thread




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




def on_message(ws,message):
    print(message)

def on_errors(ws,error):

    print(error)

def on_close(ws):
    print("close connection")

def on_open(ws):
    #查询组货详情字段
    def run(*args):
        """
        修改各个商品各个字段的信息
        :param args:
        :return:
        """
        activity_id = 860
        # 查询组货详情中的商品id
        sql = "select a.`id` from `live_assistant_temp`.`tb_activity_goods` a where a.`activity_id`={activity_id} and a.`related_status`=1;".format(
            activity_id=activity_id)
        activityGoodsIds = selectSql(sql)
        for activityGoodsId in activityGoodsIds:
            #查询商品的默认字段名
            activityGoodsId = activityGoodsId[0]
            sql = "select a.`field_name` from `live_assistant_temp`.`tb_activity_goods_field` a where a.`activity_goods_id`={activityGoodsId} and a.`field_type`=1 and a.`deleted_at` is null".format(activityGoodsId=activityGoodsId)
            defaultFieldNames = selectSql(sql)
            for defaultFieldName in defaultFieldNames:
                defaultFieldName = defaultFieldName[0]
                values = ['22']
                for value in values:
                    standard = {"optionType":"2","deptType":"2","activityGoodsId":activityGoodsId,"fieldName":defaultFieldName,"value":value,"action":"EDIT_FIELD".format(defaultFieldName=defaultFieldName)}
                    print(standard)
                    ws.send(json.dumps(standard))
                    time.sleep(2)
        time.sleep(1)
        ws.close()
    def run2(*args):
        """
        添加/删除商品
        :param args:
        :return:
        """
    def run3(*args):
        """
        修改商品状态（确定选中/未选中/初选/待选）
        :param args:
        :return:
        """
    # _thread.start_new_thread(run,())
    Thread(target=run).start()


if __name__ == '__main__':
    websocketnew.enableTrace(True)
    SERVER_URL = 'ws://116.62.106.122:5111/?sid=860missionGoodsDetail&token=2777af36-d4f0-48a1-910c-0bb1a9711730'
    ws = websocketnew.WebSocketApp(SERVER_URL,
                                   on_message=on_message,
                                   on_error=on_errors,
                                   on_close=on_close)
    ws.on_open = on_open
    # #socket保持长连接，一直连接着，就可以使用run_forever方法：
    ws.run_forever()
