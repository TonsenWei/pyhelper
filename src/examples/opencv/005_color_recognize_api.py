# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/5 16:05
@File : 005_color_recognize_api.py
@Desc : 
"""
import collections

import cv2
import numpy as np


def getColorList():
    dictColor = collections.defaultdict(list)

    # 黑色
    lower_black = np.array([0, 0, 0])
    higher_black = np.array([25, 35, 46])
    color_list = []
    color_list.append(lower_black)
    color_list.append(higher_black)
    dictColor['黑'] = color_list

    # 灰色
    lower_gray = np.array([0, 0, 46])
    higher_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(higher_gray)
    dictColor['灰'] = color_list

    # 白色
    lower_white = np.array([0, 0, 221])
    higher_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(higher_white)
    dictColor['白'] = color_list

    # 红色
    lower_red = np.array([0, 150, 150])
    higher_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(higher_red)
    dictColor["红"] = color_list

    # 橙色
    lower_orange = np.array([11, 43, 46])
    higher_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(higher_orange)
    dictColor["橙"] = color_list

    # 黄
    lower_yellow = np.array([26, 43, 46])
    higher_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(higher_yellow)
    dictColor["黄"] = color_list

    # 绿
    lower_green = np.array([35, 43, 46])
    higher_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(higher_green)
    dictColor["绿"] = color_list

    # 青
    lower_qing = np.array([78, 43, 46])
    higher_qing = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_qing)
    color_list.append(higher_qing)
    dictColor["青"] = color_list

    # 蓝
    lower_blue = np.array([100, 43, 46])
    higher_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(higher_blue)
    dictColor['蓝'] = color_list

    # 紫色
    lower_purple = np.array([125, 43, 46])
    higher_purple = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(higher_purple)
    dictColor['紫'] = color_list

    return dictColor


def color_recog(cvFrame):
    blurValue = 7  # 初始7
    img_hsv = cv2.cvtColor(cvFrame, cv2.COLOR_BGR2HSV)

    color_dict = getColorList()
    resStr = ""
    for d in color_dict:
        mask_color = cv2.inRange(img_hsv, color_dict[d][0], color_dict[d][1])  # 获得绿色部分掩膜
        mask_color = cv2.medianBlur(mask_color, blurValue)  # 中值滤波
        cnts, hierarchy = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        # print(f"d={d}, sum={len(cnts)}")
        resStr = f"{resStr};   {d}{len(cnts)}"
    print(resStr)

def colorRecogFromPaht(path):
    picFrame = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    color_recog(picFrame)


if __name__ == "__main__":
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_864_低电量黄色.png"
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-11_740.png"  # 青+灰-》
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_485_电量100.png"  # 青，ok
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_110_电量80.png"  # 青+灰-》
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-53-47_941_充电报警图标.png"
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-14-30_336_前雾灯.png"  # 绿色ok
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-14-56_558_远光灯.png"  # 黑色5，蓝色1
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-10-55_753_手刹车与制动系统.png"  # 红2，紫2
    tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-21-46_808_门开-后盖.png"  # 红2，紫2
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-15-05_595_ABS.png"
    # E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-19-15_545_ICA-黄色.png
    icoFrame = cv2.imdecode(np.fromfile(tmpIco, dtype=np.uint8), cv2.IMREAD_COLOR)
    # color_recog(icoFrame)
    print("青+灰：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_110_电量80.png")
    print("青：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_485_电量100.png")
    print("橙：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_864_低电量黄色.png")
    print("红：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-13_625_低电量红色.png")
    print("灰：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-14_810_电量0.png")
    print("青50：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_17-49-11_408_电量50.png")
    print("青20：")
    colorRecogFromPaht(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_17-49-10_576_电量20.png")
