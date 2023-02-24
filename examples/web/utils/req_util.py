import requests
import sys
import os
import json

from log_util import LogUtil

project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ReqUtil(object):
    domain_url = ""
    header = {}
    token_x = ""
    def __init__(self, domain):
        self.domain_url = domain
        self.header["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    
    def add_header(self, header_key, header_value):
        self.header[header_key] = header_value
    
    def post_req(self, url, *args):
        res = requests.post(url=self.domain_url + "/" + url)
        print(res.text)
        bean_json = json.loads(res.text)
        self.token_x = bean_json["data"]["token"]
        LogUtil().LOGGER.warn(self.token_x)

def req_demo001():
    # url = 'http://127.0.0.1:12019/simu?name=Gauge::Speed&type=int&value=99'
    # url = 'http://127.0.0.1:12019/simu?name=paneldata::speed_value&type=string&value=99'
    url = 'http://127.0.0.1:12019/simu?'
    getInfourl = 'http://127.0.0.1:12019/datas?'
    # ReqUtil.get(url='http://127.0.0.1:12019/simu?name=Gauge::Speed&type=int&value=99')
    # par1 = {"name": "config::project_type", "type": "int", "value": "0"}
    # par2 = {"name": "config::p01_car_module_type", "type": "int", "value": "0"}
    # res = requests.get(url=url, nodeList=par1)
    # res = requests.get(url=url, nodeList=par2)
    pppp = """{"name": "paneldata::speed_value", "type": "string", "value": "80"}"""
    getInfo = """{"name": "paneldata::speed_value", "type": "string", "value": "80"}"""
    par = json.loads(pppp)
    print(par)
    parGet = {"name": "paneldata::speed_value"}
    res = requests.get(url=url, params=par)
    print(res.json())
    res = requests.get(url=getInfourl, params=parGet)
    print(res.json())


if __name__ == "__main__":
    req = ReqUtil("http://trinity.desaysv.com/trinity")
    req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    
    pwd = r"GjMRMxL8zhMoK%2FkwFQwb8g%3D%3D"
    # pwd = r"GjMRMxL8zhMoK%252FkwFQwb8g%253D%253D"
    print(pwd)
    data = {"uid":r"uidq0460", "pwd":pwd, "X-Token":req.token_x}
    req.post_req("security/login/alm", data, headers=req.header)