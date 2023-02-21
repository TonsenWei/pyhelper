# -*- coding: utf-8 -*-
import requests
import time
import hashlib
import base64
import json
import hashlib

URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/general"
APPID = "5f96194b"
API_KEY = "10d682223457048a071af171de15c33f"


class Ocr(object):
    def __init__(self, filepath):
        self.filepath = filepath

    def _imageTextDetection(self):
        # 上传文件并进行base64位编码
        with open(self.filepath, 'rb') as f:
            f1 = f.read()
        f1_base64 = str(base64.b64encode(f1), 'utf-8')
        data = {
            'image': f1_base64
        }
        r = requests.post(URL, data=data, headers=self._getHeader())
        detectionResult = str(r.content, 'utf-8')
        return detectionResult

    def _getHeader(self):
        #  当前时间戳
        curTime = str(int(time.time()))
        #  支持语言类型和是否开启位置定位(默认否)
        param = {"language": "cn|en", "location": "false"}
        param = json.dumps(param)
        paramBase64 = base64.b64encode(param.encode('utf-8'))
        m2 = hashlib.md5()
        str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def CharacterRecognition(self):
        textresult = self._imageTextDetection()
        textresult = json.loads(textresult)
        textstring = []
        for item in textresult["data"]["block"][0]["line"]:
            for item1 in item["word"]:
                textstring.append(item1["content"])
        return textstring


if __name__ == "__main__":
    # big_p0009 = "00-09.png"
    big_png = "飞书20221020-165527.jpg"
    big_p0009 = "00-09.png"
    # imageTextDete = Ocr(r"D:\autotest\V3_auto\image_source\222.png")
    imageTextDete = Ocr(big_png)
    text = imageTextDete.CharacterRecognition()
    print(text)
