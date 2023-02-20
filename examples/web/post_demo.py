import requests
import sys
import os
import json

from utils.log_util import LogUtil
from utils.req_util import ReqUtil

project_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def post_web():
    url = "http://www.hcbgps.com/login?v=1633355657"
    data = {"username":"861117003565363", 
        "password":"eee566efb763ce7e2664fc696226d174",
        "loginType":"ADMIN",
        "rememberMe":"false",
        "domain":"www.hcbgps.com"}
    res = requests.post(url=url,data=data)
    print(res.text)

def get_user_info(target_url):
    header = {"Content-Type":"text/html", "X-Token":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wiYWNjb3VudE5vbkV4cGlyZWRcIjp0cnVlLFwiYWNjb3VudE5vbkxvY2tlZFwiOnRydWUsXCJhdXRob3JpdGllc1wiOlt7XCJhdXRob3JpdHlcIjpcInVzZXJcIn0se1wiYXV0aG9yaXR5XCI6XCJhbG1Vc2VyXCJ9XSxcImNyZWRlbnRpYWxzTm9uRXhwaXJlZFwiOnRydWUsXCJlbWFpbFwiOlwiRG9uZ2NoZW5nLldlaUBkZXNheS1zdmF1dG9tb3RpdmUuY29tXCIsXCJlbmFibGVkXCI6dHJ1ZSxcInN5c0F1dGhzXCI6W1widXNlclwiLFwiYWxtVXNlclwiXSxcInVpZFwiOlwidWlkcTA0NjBcIixcInVzZXJuYW1lXCI6XCJXZWkgRG9uZ2NoZW5nXCJ9IiwiZXhwIjoxNjM1NTc5NTYyLCJqdGkiOiJPVFUzWWpnME9UQXRNbVprTnkwMFlUWTRMV0U1TlRVdFl6UTNNbVJsWTJGbVpUUXgifQ.A0i65kJfUsFALvYW3WV206PTSxj2JV2tfg7c0ro7yOg"}
    # url = target_url
    # params = {"mapType":1, "accountId":1, "v":1634776354}
    # res = requests.get(url=target_url,params=params)
    print("url=" + target_url)
    res = requests.get(url=target_url, headers=header)
    # res = requests.get(url=url)
    print(res.text)
    LogUtil().LOGGER.debug("end...")

def get_ListMyRouter(target_url):
    LogUtil().LOGGER.debug("get_ListMyRouter ...")
    header = {"Content-Type":"text/html", "X-Token":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wiYWNjb3VudE5vbkV4cGlyZWRcIjp0cnVlLFwiYWNjb3VudE5vbkxvY2tlZFwiOnRydWUsXCJhdXRob3JpdGllc1wiOlt7XCJhdXRob3JpdHlcIjpcInVzZXJcIn0se1wiYXV0aG9yaXR5XCI6XCJhbG1Vc2VyXCJ9XSxcImNyZWRlbnRpYWxzTm9uRXhwaXJlZFwiOnRydWUsXCJlbWFpbFwiOlwiRG9uZ2NoZW5nLldlaUBkZXNheS1zdmF1dG9tb3RpdmUuY29tXCIsXCJlbmFibGVkXCI6dHJ1ZSxcInN5c0F1dGhzXCI6W1widXNlclwiLFwiYWxtVXNlclwiXSxcInVpZFwiOlwidWlkcTA0NjBcIixcInVzZXJuYW1lXCI6XCJXZWkgRG9uZ2NoZW5nXCJ9IiwiZXhwIjoxNjM1NTc5NTYyLCJqdGkiOiJPVFUzWWpnME9UQXRNbVprTnkwMFlUWTRMV0U1TlRVdFl6UTNNbVJsWTJGbVpUUXgifQ.A0i65kJfUsFALvYW3WV206PTSxj2JV2tfg7c0ro7yOg"}
    # url = target_url
    # params = {"mapType":1, "accountId":1, "v":1634776354}
    # res = requests.get(url=target_url,params=params)
    LogUtil().LOGGER.debug("url=" + target_url)
    res = requests.get(url=target_url, headers=header)
    # res = requests.get(url=url)
    LogUtil().LOGGER.info(res.text)

def get_ProjectTree(target_url):
    LogUtil().LOGGER.debug("get_ProjectTree ...")
    header = {"Content-Type":"text/html", "X-Token":"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoie1wiYWNjb3VudE5vbkV4cGlyZWRcIjp0cnVlLFwiYWNjb3VudE5vbkxvY2tlZFwiOnRydWUsXCJhdXRob3JpdGllc1wiOlt7XCJhdXRob3JpdHlcIjpcInVzZXJcIn0se1wiYXV0aG9yaXR5XCI6XCJhbG1Vc2VyXCJ9XSxcImNyZWRlbnRpYWxzTm9uRXhwaXJlZFwiOnRydWUsXCJlbWFpbFwiOlwiRG9uZ2NoZW5nLldlaUBkZXNheS1zdmF1dG9tb3RpdmUuY29tXCIsXCJlbmFibGVkXCI6dHJ1ZSxcInN5c0F1dGhzXCI6W1widXNlclwiLFwiYWxtVXNlclwiXSxcInVpZFwiOlwidWlkcTA0NjBcIixcInVzZXJuYW1lXCI6XCJXZWkgRG9uZ2NoZW5nXCJ9IiwiZXhwIjoxNjM1NTc5NTYyLCJqdGkiOiJPVFUzWWpnME9UQXRNbVprTnkwMFlUWTRMV0U1TlRVdFl6UTNNbVJsWTJGbVpUUXgifQ.A0i65kJfUsFALvYW3WV206PTSxj2JV2tfg7c0ro7yOg"}
    # url = target_url
    # params = {"mapType":1, "accountId":1, "v":1634776354}
    # res = requests.get(url=target_url,params=params)
    LogUtil().LOGGER.debug("url=" + target_url)
    res = requests.get(url=target_url, headers=header)
    # res = requests.get(url=url)
    LogUtil().LOGGER.info(res.text)
    # LogUtil().LOGGER.warn(res.text)
    # res_json = json.dumps(res.text)
    bean_json = json.loads(res.text)
    print("code = " + str(bean_json["code"]))
    # LogUtil().LOGGER.warn(res.keys())


if __name__ == "__main__":
    # post_web()
    # get_web("http://www.hcbgps.com/rest/device/861117003565363?")
    # get_user_info("http://trinity.desaysv.com/trinity/sys/user/userinfo")
    # get_ListMyRouter("http://trinity.desaysv.com/trinity/sys/menu/listMyRouter")
    # get_ProjectTree("http://trinity.desaysv.com/trinity/pm/api/getProjectTree")
    req = ReqUtil("http://trinity.desaysv.com/trinity")
    req.post_req("security/login/alm")