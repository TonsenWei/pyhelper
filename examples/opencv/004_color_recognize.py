# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/5 14:31
@File : 004_color_recognize.py
@Desc : 
"""
# @Time : 2021/12/28 17:07
# @Author : ZY
# @Site :
# @File : colorList.py
# @Software: PyCharm
import cv2
import numpy as np
import collections


# 定义字典存放颜色分量上下限
# 例如：{颜色: [min分量, max分量]}
# {'red': [array([160,  43,  46]), array([179, 255, 255])]}

def getColorList():
    dict = collections.defaultdict(list)

    # 黑色
    lower_black = np.array([0, 0, 0])
    higher_black = np.array([25, 35, 46])
    color_list = []
    color_list.append(lower_black)
    color_list.append(higher_black)
    dict['黑'] = color_list

    # 灰色
    lower_gray = np.array([0, 0, 46])
    higher_gray = np.array([180, 43, 220])
    color_list = []
    color_list.append(lower_gray)
    color_list.append(higher_gray)
    dict['灰'] = color_list

    # 白色
    lower_white = np.array([0, 0, 221])
    higher_white = np.array([180, 30, 255])
    color_list = []
    color_list.append(lower_white)
    color_list.append(higher_white)
    dict['白'] = color_list

    # 红色
    lower_red = np.array([0, 150, 150])
    higher_red = np.array([10, 255, 255])
    color_list = []
    color_list.append(lower_red)
    color_list.append(higher_red)
    dict["红"] = color_list

    # 橙色
    lower_orange = np.array([11, 43, 46])
    higher_orange = np.array([25, 255, 255])
    color_list = []
    color_list.append(lower_orange)
    color_list.append(higher_orange)
    dict["橙"] = color_list

    # 黄
    lower_yellow = np.array([26, 43, 46])
    higher_yellow = np.array([34, 255, 255])
    color_list = []
    color_list.append(lower_yellow)
    color_list.append(higher_yellow)
    dict["黄"] = color_list

    # 绿
    lower_green = np.array([35, 43, 46])
    higher_green = np.array([77, 255, 255])
    color_list = []
    color_list.append(lower_green)
    color_list.append(higher_green)
    dict["绿"] = color_list

    # 青
    lower_qing = np.array([78, 43, 46])
    higher_qing = np.array([99, 255, 255])
    color_list = []
    color_list.append(lower_qing)
    color_list.append(higher_qing)
    dict["绿"] = color_list

    # 蓝
    lower_blue = np.array([100, 43, 46])
    higher_blue = np.array([124, 255, 255])
    color_list = []
    color_list.append(lower_blue)
    color_list.append(higher_blue)
    dict['蓝'] = color_list

    # 紫色
    lower_purple = np.array([125, 43, 46])
    higher_purple = np.array([180, 255, 255])
    color_list = []
    color_list.append(lower_purple)
    color_list.append(higher_purple)
    dict['紫'] = color_list

    return dict


def get_color(frame):
    # print('go in get_color')
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    maxsum = -100
    color = None
    color_dict = getColorList()
    for d in color_dict:
        mask = cv2.inRange(hsv, color_dict[d][0], color_dict[d][1])
        # cv2.imwrite(d + '.jpg', mask)
        binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        binary = cv2.dilate(binary, None, iterations=2)
        cnts, hiera = cv2.findContours(binary.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        sum = 0
        for c in cnts:
            sum += cv2.contourArea(c)
            print(f"d={d}")
        if sum > maxsum:
            maxsum = sum
            color = d

    return color


if __name__ == '__main__':
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-02-40_203_充电报警图标.png"  # 红，ok
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-14-25_595_前雾灯.png"  # 绿
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-16-15_532_EPB-绿色.png"  #
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-15-37_491_ESP OFF.png"  # 识别出红，ok
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\images\2023-01-04_18-19-58_228_NDA-蓝色.png"  # 蓝色ok
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_864_低电量黄色.png"  # 橙色ok
    tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_110_电量80.png"  # 橙色ok
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_485_电量100.png"  # 识别出绿，应为青
    # tmpIco = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-14_810_电量0.png"  # 灰色，ok
    icoFrame = cv2.imdecode(np.fromfile(tmpIco, dtype=np.uint8), cv2.IMREAD_COLOR)
    Color = get_color(icoFrame)
    print(Color)
