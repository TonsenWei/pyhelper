# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/5 17:23
@File : color_recognize.py
@Desc : 
"""
import collections

import cv2
import numpy as np


class ColorRecognize:

    @staticmethod
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
        # lower_red = np.array([0, 150, 150])
        lower_red = np.array([0, 43, 46])
        higher_red = np.array([10, 255, 255])
        color_list = []
        color_list.append(lower_red)
        color_list.append(higher_red)
        dictColor["红"] = color_list

        # 红红色
        # lower_red = np.array([156, 150, 150])
        lower_red = np.array([156, 43, 46])
        higher_red = np.array([180, 255, 255])
        color_list = []
        color_list.append(lower_red)
        color_list.append(higher_red)
        dictColor["红红"] = color_list

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

    @staticmethod
    def recog(cvFrame):
        blurValue = 7  # 初始7
        img_hsv = cv2.cvtColor(cvFrame, cv2.COLOR_BGR2HSV)

        color_dict = ColorRecognize.getColorList()
        # resStr = ""
        resColor = {}
        redValue = 0
        redRedValue = 0
        for d in color_dict:
            mask_color = cv2.inRange(img_hsv, color_dict[d][0], color_dict[d][1])  # 获得绿色部分掩膜
            mask_color = cv2.medianBlur(mask_color, blurValue)  # 中值滤波
            cnts, hierarchy = cv2.findContours(mask_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # print(f"d={d}, sum={len(cnts)}")
            # resStr = f"{resStr};   {d}{len(cnts)}"
            if d == "红":
                redValue = len(cnts)
            elif d == "红红":
                redRedValue = len(cnts)
            else:
                resColor.setdefault(d, len(cnts))
        redCnts = redValue + redRedValue
        resColor.setdefault("红", redCnts)
        # print(resStr)
        resColor = sorted(resColor.items(), key=lambda x: x[1], reverse=True)
        return resColor

    @staticmethod
    def recogFromPng(path):
        picFrame = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        return ColorRecognize.recog(picFrame)

    @staticmethod
    def getColorNames(colors, cnt):
        """
        返回前cnt个不重复的颜色名称
        :param colors: 已排好序的颜色列表
        :param cnt: 需要找到几个不同颜色，颜色后面的值如果一样会多取颜色，直到值不同
        :return:
        如：
        输入：  [('灰', 1), ('绿', 1), ('青', 1), ('黑', 0), ('白', 0), ('红', 0), ('橙', 0), ('黄', 0), ('蓝', 0), ('紫', 0)]
                2
        输出： ['灰', '绿', '青']
        """
        colorList = []
        tmpValue = 0
        valueCounter = 0
        for index, colorDict in enumerate(colors):
            currColorValue = colors[index][1]
            if currColorValue != 0:  # 该颜色值不为0
                if tmpValue != currColorValue:
                    if valueCounter < cnt:
                        colorList.append(colors[index][0])
                        valueCounter += 1  # 不同值的个数
                        tmpValue = currColorValue
                else:  # 值与上一个值相等，则也加入颜色列表，值相同则不同值的个数不增加
                    colorList.append(colors[index][0])
                    tmpValue = currColorValue
        # print(colorList)
        return colorList

    @staticmethod
    def allInColors(tarCol, oriCol):
        allIn = True
        for i, col in enumerate(tarCol):
            if col not in oriCol:
                allIn = False
                break
        return allIn

    @staticmethod
    def icoColorsIn(icoPng, oriPng):
        icoColors = ColorRecognize.recogFromPng(icoPng)
        icoColorsNames = ColorRecognize.getColorNames(icoColors, 2)
        oriColors = ColorRecognize.recogFromPng(oriPng)
        oriColorsNames = ColorRecognize.getColorNames(oriColors, 2)
        return ColorRecognize.allInColors(icoColorsNames, oriColorsNames)

    @staticmethod
    def icoColorsInFrame(tarFrame, tmpPng):
        """
        判断匹配到的图标颜色，是否包含在模板图片的颜色中
        :param tarFrame: 从摄像头匹配到的
        :param tmpPng:  模板图片（查找的图标原型）
        :return:
        """
        allIn = True
        tarColors = ColorRecognize.recog(tarFrame)
        tarColorsNames = ColorRecognize.getColorNames(tarColors, 2)
        tmpColors = ColorRecognize.recogFromPng(tmpPng)
        tmpColorsNames = ColorRecognize.getColorNames(tmpColors, 2)
        for i, col in enumerate(tarColorsNames):
            if col not in tmpColorsNames:
                allIn = False
                break
        return allIn, tarColors, tmpColors
        # return ColorRecognize.allInColors(tarColorsNames, tmpColorsNames)

    @staticmethod
    def testRedAndGreen():
        picFrame = cv2.imdecode(np.fromfile(r"C:\Users\tonse\Pictures\std\对比度测试图\red.png", dtype=np.uint8),
                                cv2.IMREAD_COLOR)
        # picFrame = cv2.imdecode(np.fromfile(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01
        # -04_17-49-13_625_低电量红色.png", dtype=np.uint8), cv2.IMREAD_COLOR) picFrame = cv2.imdecode(np.fromfile(
        # r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-53-47_941_充电报警图标.png",
        # dtype=np.uint8), cv2.IMREAD_COLOR)
        res = ColorRecognize.icoColorsInFrame(picFrame,
                                              r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01"
                                              r"-04_17-49 "
                                              r"-12_110_电量80.png")
        print(res)

        picFrame = cv2.imdecode(np.fromfile(r"C:\Users\tonse\Pictures\std\对比度测试图\green.png", dtype=np.uint8),
                                cv2.IMREAD_COLOR)
        # picFrame = cv2.imdecode(np.fromfile(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01
        # -04_17-49-13_625_低电量红色.png", dtype=np.uint8), cv2.IMREAD_COLOR) picFrame = cv2.imdecode(np.fromfile(
        # r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-53-47_941_充电报警图标.png",
        # dtype=np.uint8), cv2.IMREAD_COLOR)
        res = ColorRecognize.icoColorsInFrame(picFrame,
                                              r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01"
                                              r"-04_17-49 "
                                              r"-12_110_电量80.png")
        print(res)


def ColorTest():
    allIn = True
    # tarColors = ColorRecognize.recog
    tarColorsTmp = [('蓝', 3), ('青', 1), ('黑', 0), ('灰', 0), ('白', 0), ('红', 0), ('橙', 0), ('黄', 0), ('绿', 0), ('紫', 0)]
    tarColorsNames = ColorRecognize.getColorNames(tarColorsTmp, 2)
    # tmpColors = ColorRecognize.recogFromPng(tmpPng)
    tmpColorsTmp = [('青', 1), ('黑', 0), ('灰', 0), ('白', 0), ('红', 0), ('橙', 0), ('黄', 0), ('绿', 0), ('蓝', 0), ('紫', 0)]
    tmpColorsNames = ColorRecognize.getColorNames(tmpColorsTmp, 2)
    for i, col in enumerate(tarColorsNames):
        if col not in tmpColorsNames:
            allIn = False
            break
    print(f"allIn = {allIn}")
    print(f"tarColorsNames = {tarColorsNames}")
    print(f"tmpColorsNames = {tmpColorsNames}")
    return allIn, tarColors, tmpColors

if __name__ == "__main__":
    # res = ColorRecognize.recogFromPng(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-13_625_低电量红色.png")  # ['绿', '青']
    # res = ColorRecognize.recogFromPng(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\cam_电量条_100.png")  # ['绿', '青']
    # res = ColorRecognize.recogFromPng(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_485_电量100.png") #['青']
    # res = ColorRecognize.recogFromPng(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\cam_电量条_80.png")
    # res = ColorRecognize.recogFromPng(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_110_电量80.png")
    # print(res)
    # ColorRecognize.getColorNames(res, 2)
    # [('蓝', 5), ('灰', 1), ('绿', 1), ('青', 1), ('黑', 0), ('白', 0), ('红', 0), ('橙', 0), ('黄', 0), ('紫', 0)]
    # ['蓝', '灰']

    # [('蓝', 5), ('灰', 1), ('绿', 1), ('青', 1), ('黑', 0), ('白', 0), ('红', 0), ('橙', 0), ('黄', 0), ('紫', 0)]
    # ['蓝', '灰', '绿', '青']
    #     print(ColorRecognize.allInColors(['蓝', '灰', '白'], ['蓝', '灰', '绿', '青']))
    #     print(ColorRecognize.icoColorsIn(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\cam_电量条_80.png",
    #                                      r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49-12_110_电量80.png"))

    png_path = r"E:\Tonsen\Downloads\logs\mafenni\2023-01-13_16-44-43\2023-01-13_16-45-25_175.png"
    picFrame = cv2.imdecode(np.fromfile(png_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    # picFrame = cv2.imdecode(np.fromfile(r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-49
    # -13_625_低电量红色.png", dtype=np.uint8), cv2.IMREAD_COLOR) picFrame = cv2.imdecode(np.fromfile(
    # r"E:\Tonsen\Downloads\logs\mafenni\2023-01-04_17-48-48\电量条\2023-01-04_17-53-47_941_充电报警图标.png",
    # dtype=np.uint8), cv2.IMREAD_COLOR)
    # (119, 444), (119, 467), (238, 467), (238, 444)
    allIn, tarColors, tmpColors = ColorRecognize.icoColorsInFrame(picFrame,
                                          r"E:\Tonsen\Downloads\logs\mafenni\2023-01-13_16-44-43\2023-01-13_16-45-25_534_电量100.png")
    print(allIn)
    print(tarColors)
    print(tmpColors)
    ColorTest()
# [('红', 3), ('橙', 1), ('黑', 0), ('灰', 0), ('白', 0), ('黄', 0), ('绿', 0), ('青', 0), ('蓝', 0), ('紫', 0)]
# 2023-01-04_17-49-12_864_低电量黄色

# [('红', 3), ('橙', 1), ('黑', 0), ('灰', 0), ('白', 0), ('黄', 0), ('绿', 0), ('青', 0), ('蓝', 0), ('紫', 0)]
# 2023-01-04_17-49-13_244_低电量黄色

# [('青', 1), ('黑', 0), ('灰', 0), ('白', 0), ('橙', 0), ('黄', 0), ('绿', 0), ('蓝', 0), ('紫', 0), ('红', 0)]
# cam_电量条_100

# [('青', 1), ('黑', 0), ('灰', 0), ('白', 0), ('橙', 0), ('黄', 0), ('绿', 0), ('蓝', 0), ('紫', 0), ('红', 0)]
# 2023-01-04_17-49-12_485_电量100

# [('红', 4), ('紫', 3), ('黑', 0), ('灰', 0), ('白', 0), ('橙', 0), ('黄', 0), ('绿', 0), ('青', 0), ('蓝', 0)]
# 2023-01-04_17-49-13_625_低电量红色

# [('灰', 1), ('青', 1), ('蓝', 1), ('黑', 0), ('白', 0), ('橙', 0), ('黄', 0), ('绿', 0), ('紫', 0), ('红', 0)]
# 2023-01-04_17-49-14_413_电量0
