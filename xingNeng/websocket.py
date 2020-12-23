
import json
import time
import _thread
import websocketnew
from threading import Thread




class LongWebsocket(websocketnew.WebSocketApp):

    def on_message(self,message):
        print(message)

    def on_errors(self,error):

        print(error)

    def on_close(self):
        print("close connection")

    def on_open(self,):
        def run(*args):
            values = ['25', '26', '27', '28']
            for value in values:
                standard = {"optionType": "2", "deptType": "2", "activityGoodsId": 4921, "fieldName": "dailyPrice",
                            "value": value, "action": "EDIT_FIELD"}
                self.send(json.dumps(standard))
                time.sleep(2)
            time.sleep(1)
            self.close()

        # _thread.start_new_thread(run,())
        Thread(target=run).start()




if __name__ == '__main__':
    websocketnew.enableTrace(True)
    url= 'ws://116.62.106.122:5111/?sid=885missionGoodsDetail&token=9289c06d-1825-4025-b012-b99c3762f471'
    ws = LongWebsocket(url)
    ws.on_open
    ws.run_forever()
