"""
Author: Wei Dongcheng
Date:  
LastEditTime:  
LastEditors: Wei Dongcheng
Description:
"""
import hashlib
import requests
import json

# 待加密信息
# task_id = "20220424002"
# task_id = "20220424002"
# 20220517001
# task_id = "20220517001"
task_id = "wei.dongcheng"

# target_str = task_id + "byd_testing"
target_str = "byd_auto.7zbyd_testing"
# 创建md5对象
hl = hashlib.md5()

# Tips
# 此处必须声明encode
# 若写法为hl.update(str) 报错为： Unicode-objects must be encoded before hashing
hl.update(target_str.encode(encoding='utf-8'))
first_md5 = hl.hexdigest()

h2 = hashlib.md5()
h2.update(first_md5.encode(encoding='utf-8'))
token = h2.hexdigest()

print('MD5加密前为 ：' + target_str)
print('MD5加密后为 ：' + first_md5)
print('MD5二次加密后为 ：' + token)

# url = "http://10.167.67.49:8099/api/getTaskInformation?taskId=20220424002&token=d1eba6b727cbef45ce7dce0f320899ff"
# url = "http://10.167.67.49:8090/api/getTaskInformation?taskId=20220424002&token=d1eba6b727cbef45ce7dce0f320899ff"
# url = "http://10.167.67.49:8090/api/getTaskInformation?taskId=20220517001&token=11d13d4c7d336a24b843a63251efa75a"
# url = "http://10.167.67.49:8090/api/getTasks?userName=wei.dongcheng&token=01dc9f64d70e3da3a2fd4943ec3b21d5"
# url = "http://10.167.67.49:8090/api/getVersion?token=" + token
url = "http://10.167.67.49:8090/api/downloadFile?fileName=byd_auto.exe&token=" + token
print(url)
# url = "http://10.167.67.49:8090/api/downloadFile?token=fbed8cebeb83e30c1607763fb4f29a91"
# print(url)
# 


# r = requests.get(url)

# 获取返回的json
# js = r.json()
# print("---------------------------------------------------------------------------")
# print("返回的json:")
# print(js)
# print("---------------------------------------------------------------------------")
# data_list = js["data"]
# for dat in data_list:
#     print("mTaskId = " + str(dat["mTaskId"]))
#     print("mInputMap = " + str(dat["mInputMap"]))
#     inputmapobj = json.loads(dat["mInputMap"])
#     for one_obj in inputmapobj:
#         print(one_obj)
# r = requests.get(url)
# print(r.content)
# with open("BYDauto.exe", "wb") as code:
#     code.write(r.content)
