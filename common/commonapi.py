from string import Template

import requests
import yaml
import ast




class CommonApi:
    env = yaml.safe_load(open("./config/env.yaml"))
    #data 是一个请求的信息
    def send(self,data:dict):
        url = self.env["dev-live-assistant.zhiyitech.cn"][self.env["default"]]+str(data["url"])
        if(data["method"]=="get" and data["json"]==None):
            r = requests.get(url=url,headers=data["headers"])
        elif (data["method"] == "get" and data["json"] != None):
            r = requests.get(url=url, headers=data["headers"],params=data["json"])
        elif (data["method"] == "post" and data["form"]=="json"):
            r = requests.post(url=url, headers=data["headers"],json=data["json"])
        elif (data["method"] == "post" and data["form"]=="json"):
            r = requests.post(url=url, headers=data["headers"],json=data["json"])
        elif (data["method"] == "post" and data["form"] == "multipart/form-data"):
            r = requests.post(url=url, headers=data["headers"], files=ast.literal_eval(data["json"]))
        else:
            print("'暂时不支持该方法，请继续补充方法'")
            r= None
        return r




