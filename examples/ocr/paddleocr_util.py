# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/10/20 17:14
@File : paddleocr_util.py
@Desc :
pip install paddlepaddle
pip install shapely
pip install paddleocr
"""
import time

from paddleocr import PaddleOCR
from paddleocr.tools.infer.utility import draw_ocr

png1 = "hdqcsc.png"  # [[[11.0, 12.0], [127.0, 12.0], [127.0, 36.0], [11.0, 36.0]], ('换挡请踩刹车', 0.9216315150260925)]
png2 = "powerlow.png"  # '电量消耗多', '进入省电模式'
"""
[[[22.0, 14.0], [185.0, 12.0], [186.0, 38.0], [23.0, 40.0]], ('电量消耗过多', 0.9924144744873047)]
[[[24.0, 46.0], [186.0, 46.0], [186.0, 73.0], [24.0, 73.0]], ('进入省电模式', 0.9843379855155945)]
"""

png3 = "tv.png"
# [[[762.0, 443.0], [1150.0, 443.0], [1150.0, 504.0], [762.0, 504.0]], ('SKYWORTH', 0.9065746068954468)]
# 四个定点坐标： 左上，右上，右下，左下

multi = "多字.png"
big_png = "飞书20221020-165527.jpg"
big_p0009 = "00-09.png"
airbag = "airbag.png"
# pngs = [png1, png2, png3]
pngs = [airbag]


ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# 输入待识别图片路径
# img_path = multi
# 输出结果保存路径
start_time = time.time()
for img_path in pngs:
    results = ocr.ocr(img_path, cls=True)
    print("cost_time = " + str(time.time() - start_time))
    for lines in results:
        print("===============================")
        # print(line)
        for line in lines:
            print(line)

# from PIL import Image
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in results]
# txts = [line[1][0] for line in results]
# scores = [line[1][1] for line in results]
# im_show = draw_ocr(image, boxes, txts, scores)
# im_show = Image.fromarray(im_show)
# # im_show = Image.fromarray(image)
# im_show.show()
