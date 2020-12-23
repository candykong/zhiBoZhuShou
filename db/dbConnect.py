#!/usr/bin/python
# -*- coding：UTF-8 -*-

#import numpy as np
#import pandas as pd



import pymysql.cursors


class DB():
    def __init__(self,host,port,user,passwd):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd

    def dbConnect(self):
        self.db = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            passwd=self.passwd,
            charset='utf8')
        return self.db

    def dbSelect(self,sql):
        self.cursor = self.dbConnect().cursor()
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print(data)
        self.db.close()
        return data












