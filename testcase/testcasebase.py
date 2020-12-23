from common.commonapi import CommonApi
import yaml


class Testcasebase():
    def setup(self):
        print('开始测试')

    # def getToken(self):
    #     self.commonApi = CommonApi()
    #     self.data = yaml.safe_load(open("./zhibozhushouApi/login.yaml"))
    #     self.r = self.commonApi.send(self.data).text
    #     self.r_json = json.loads(self.r, strict=False)
    #     self.token = self.r_json["result"]['token']
    #     return self.token

    def getToken(self):
        self.commonApi = CommonApi()
        self.data = yaml.safe_load(open("./zhibozhushouApi/login.yaml"))
        self.token = self.commonApi.send(self.data).json()["result"]['token']
        print(self.token)
        return self.token

    #获取响应
    def getResponse(self,data):
        self.data=data
        self.commonApi = CommonApi()
        self.r = self.commonApi.send(self.data)
        return self.r


    def teardown(self):
        print('测试结束')
