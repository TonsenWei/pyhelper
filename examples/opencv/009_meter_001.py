# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/9 16:36
@File : 009_meter_001.py
@Desc :
https://blog.csdn.net/qq_44781688/article/details/118400263
"""
import cv2
import numpy as np
from PIL import Image, ImageChops


def removePointer():
    # 两图像求最亮去除指针
    # 用Image库求最亮去除指针，保存方便下一步去除表盘
    im = ImageChops.lighter(Image.open(r'D:\tmp\my_meter_temp.png'), Image.open(r'D:\tmp\my_meter_temp_50.png'))
    im.save("noPointer.png")


def pointer():
    im = Image.open(r'D:\tmp\my_meter_temp.png')
    im_none = Image.open("noPointer.png")
    im1 = ImageChops.difference(im_none, im)
    im1.save("pointer.png")
    im = cv2.imread("pointer.png")
    return im


def centre(filepath, judge=False):
    org = cv2.imread(filepath, 1)
    img = org
    img_gray = cv2.cvtColor(org, cv2.COLOR_BGR2GRAY)
    # 低通滤波进行平滑图像
    img_gray = cv2.medianBlur(img_gray, 5)
    cimg = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    # 提取圆形
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, 10, param1=10, param2=10, minRadius=465, maxRadius=485)

    # if circles is not None:
    circles = np.uint16(np.around(circles))
    x = 0
    y = 0
    j = 0
    for i in circles[0, :]:
        # draw the outer circle
        cv2.circle(img, (i[0], i[1]), i[2], (0, 0, 255), 10)
        x = (x * j + i[0]) / (j + 1)
        y = (y * j + i[1]) / (j + 1)
        j = j + 1
        # draw the center of the circle
        if judge:
            y = y + 8
            x = x + 1
            cv2.circle(img, (int(x), int(y)), 2, (0, 0, 255), 5)  # 刻度不同图像不同偏差不同
        else:
            x = x - 8
            y = y - 4
            cv2.circle(img, (int(x), int(y)), 2, (0, 0, 255), 5)

    # 显示原图和处理后的图像
    # cv2.imshow("org",org)
    cv2.imshow("processed", img)
    # print("中心为：", i[0] - 8, i[1] - 4)
    cv2.waitKey(0)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # return img, int(x), int(y)


# 在一张图片上检测圆
import cv2
import os
import numpy as np


def detect_circle(img):
    """在一张图片上检测圆
    img: 必须是二值化的图
    """
    # img = img * 255
    img_bgr = np.stack([img, img, img], axis=-1)
    img = cv2.medianBlur(img, 5)
    # param2越小，检测到的圆越多
    circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=10, param2=10, minRadius=10, maxRadius=70)
    # print(circles)
    circles = np.uint16(np.around(circles))
    # 因为我这里只检测一个圆，需要检测多个圆的话，就遍历circles
    assert len(circles) == 1, f'{circles},not qualify only a circle!'
    (x, y, r) = circles[0][0]
    print(f"len(circles) = {len(circles)}")
    # input(circles[0,:])
    show = True
    if show == True:
        cv2.circle(img_bgr, (x, y), r, (0, 0, 255), 2)
        # 圆心
        cv2.circle(img_bgr, (x, y), 2, (0, 255, 0), 3)
        cv2.imshow('w', img_bgr)
        cv2.waitKey(0)
    # 这里的x对应w,y对应d
    return (x, y, r), img_bgr  # 返回横纵坐标和半径、rgb图


if __name__ == '__main__':
    file_path = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\TemplateLib\004.jpg"
    img = cv2.imread(file_path, 0)
    # 灰度化
    # img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 二值化
    ret, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    # print(np.unique(img))
    detect_circle(img)

#
#
# if __name__ == "__main__":
#     # removePointer()
#     # pointer()
#     centre(r'D:\tmp\ori.png')
