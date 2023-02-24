# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/10/20 17:00
@File : easyocr_util.py
@Desc :
pip install easyocr
执行时会下载检测模块Downloading detection model
初次运行需要在线下载检测模型和识别模型，建议在网速好点的环境运行
"""
import time

import cv2
import easyocr

# png_path = "换档请踩刹车.png"  # 路径有中文路径会报错
import numpy as np

from utils.time_util import TimeUtil

airbag = "airbag.png"  # 换挡谑踩刹车
png1 = "hdqcsc.png"  # 换挡谑踩刹车
png2 = "powerlow.png"  # '电量消耗多', '进入省电模式'
png3 = "tv.png"  # 'SKYWORTH'
# pngs = [png1, png2, png3]
# pngs = ["feishu20221020-165527.jpg"]  # ['没^0', '0丰00', '86oC', '行驶数据 A', '00: 09', '00', 'km', 'km/h', '2km', 'SPORT', 'E', '~F']
pngs = [airbag]  # ['没^0', '0丰00', '86oC', '行驶数据 A', '00: 09', '00', 'km', 'km/h', '2km', 'SPORT', 'E', '~F']

# 设置识别中英文两种语言
reader = easyocr.Reader(['ch_sim', 'en'],
                        gpu=False,
                        model_storage_directory="./easyocr_demo/model",
                        download_enabled=False)
# reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)  # need to run only once to load model into memory
# reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)  # need to run only once to load model into memory
# result = reader.readtext(r"d:\Desktop\4A34A16F-6B12-4ffc-88C6-FC86E4DF6912.png", detail=0)
start_time = time.time()
new_frame = cv2.imdecode(np.fromfile(airbag, dtype=np.uint8), cv2.IMREAD_COLOR)
for png_path in pngs:
    result = reader.readtext(png_path)
    print("cost_time = " + str(time.time() - start_time))  # 0.9408
    for line in result:
        # print(line)  # ([[113, 147], [247, 147], [247, 165], [113, 165]], '插入Mermaid流程图', 0.3992503737187054)
        pos = line[0]
        word_str = line[1]
        confidence_f = line[2]
        print("位置：" + str(pos) + ", word_str=" + str(word_str) + ", confidence_f=" + str(round(confidence_f, 3)))
        try:
            cv2.rectangle(new_frame,
                          tuple(pos[0]),
                          tuple(pos[2]), (0, 255, 0), 2)
        except Exception as e:
            print(e)
    while True:
        cv2.imshow('real_img', new_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
