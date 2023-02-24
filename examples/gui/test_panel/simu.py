# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/23 10:54
@File : simu.py
@Desc : 仪表模拟器网络请求接口
"""
import json

import requests


class Simu:

    def __init__(self, baseUrl='http://127.0.0.1', port=12019, connector="::"):
        self.baseUrl = baseUrl
        self.sConnector = connector  # 端口为12019时默认值
        # self.port = 12019
        # if port == 12017:  # 端口为12017时连接符
        #     self.sConnector = "@"
        self.port = port
        self.addr = f"{self.baseUrl}:{self.port}"  # 请求IP地址

    def set(self, params):
        """
        设置值
        :param params: 参数列表如[paneldata;speed_value;string;30]
        :return: 网络返回的响应
        """
        # par1 = {"name": "config::project_type", "type": "int", "value": "0"}
        setUrl = f"{self.addr}/simu?"
        paramsSent = {"name": f"{params[0]}{self.sConnector}{params[1]}", "type": params[2], "value": params[3]}
        res = requests.get(setUrl, paramsSent)
        del params
        del paramsSent
        return res

    def get(self, params):
        """
        获取值
        :param params: 获取的值的键
        :return: res:网络返回的响应， resValue：解析后的值
        """
        # par1 = {"name": "config::project_type"}
        getUrl = f"{self.addr}/datas?"
        nameStr = f"{params[0]}{self.sConnector}{params[1]}"  # "config::project_type"
        paramsSent = {"name": nameStr}
        res = requests.get(getUrl, paramsSent)
        resValue = str(res.json()[0][nameStr])
        del params, paramsSent
        return res, resValue


SIMU = Simu()

if __name__ == "__main__":
    setInfo = """{"name": "paneldata::speed_value", "type": "string", "value": "50"}"""
    getInfo = """{"name": "paneldata::speed_value", "type": "string", "value": "80"}"""
    par = json.loads(setInfo)
    layout = Simu()
    layout.set(["paneldata", "speed_value", "string", "20"])
