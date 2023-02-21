# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/10/20 16:25
@File : ddddocr_util.py
@Desc :
用于验证码识别比较准确，常规文字识别错误率比较高而且经常识别不到，比如图片中有很多文字的时候
pip install ddddocr  # 需要安装4.3版本以下的
opencv-python-3.4.18.65 验证OK
opencv-python-4.1.2.30 验证OK
"""
import ddddocr

ocr = ddddocr.DdddOcr()

# with open("待识别验证码.png", 'rb') as f:
# png_path = "电量消耗过多进入省电模式.png"  # 识别错误,乱码
# png_path = "换档请踩刹车.png"  # 她省谢甲孙车，尽量只裁剪文字后：换挡请课刹车
png_path = "feishu20221020-165527.jpg"  # 她省谢甲孙车，尽量只裁剪文字后：换挡请课刹车
with open(png_path, 'rb') as f:
    img_bytes = f.read()

res = ocr.classification(img_bytes)

print(res)
