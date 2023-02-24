# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/19 16:21
@File : 030_baidu_translate.py
@Desc : https://fanyi-api.baidu.com/doc/21
"""

import requests
import random
import json
from hashlib import md5

# Set your own appid/appkey.
appid = '20190128000259844'
appkey = 'qmdF5iPC6UkiaMVsxkzb'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang = 'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'


# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


salt = random.randint(32768, 65536)
sign = make_md5(appid + query + str(salt) + appkey)

# Build request
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

# Send request
r = requests.post(url, params=payload, headers=headers)
result = r.json()

# Show response
print(json.dumps(result, indent=4, ensure_ascii=False))
