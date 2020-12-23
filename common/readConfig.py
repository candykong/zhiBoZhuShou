#!/usr/bin/python
# -*- coding:UTF-8 -*-


import configparser

#读取配置文件


class ReadConfig:
    def __init__(self,configPath):
        self.configPath = configPath
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    #获取相应的值
    def getValue(self,section,param):
        host = self.cf.get(section,param)
        return host



