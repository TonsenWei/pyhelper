# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/21 8:58
@File : 010_line_process.py
@Desc : 
"""
import cv2
import numpy as np
from numpy import mean

# 读取图像以及图像的宽和高
img = cv2.imread(r'D:\tmp\img.png')
h = img.shape[0]
w = img.shape[1]

# 求取图像的平均灰度值
img_gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)
all_gray = []
for i in range(h):
    for j in range(w):
        all_gray.append(img_gray[i, j])
print('图像的平均灰度值：', mean(all_gray))

# Canny算子寻找图像的边缘
image_edge = cv2.Canny(img, 200, 200)

# 寻找霍夫直线
lines = cv2.HoughLines(image_edge, 1, np.pi / 180, 180)

# 绘画霍夫直线
if lines is not None:
    for n, line in enumerate(lines):
        # 沿着左上角的原点，作目标直线的垂线得到长度和角度
        rho = line[0][0]  # rho原点到直线的垂直距离
        theta = line[0][1]  #theta是由这条垂直线和逆时针测量的水平轴形成的角度
        # if np.pi / 3 < theta < np.pi * (3 / 4):
        a = np.cos(theta)
        b = np.sin(theta)
        # 得到目标直线上的点
        x0 = a * rho
        y0 = b * rho

        # 延长直线的长度，保证在整幅图像上绘制直线
        x1 = int(x0 + 2000 * (-b))
        y1 = int(y0 + 2000 * (a))
        x2 = int(x0 - 2000 * (-b))
        y2 = int(y0 - 2000 * (a))

        # 连接两点画直线
        # print((x1, y1), (x2, y2))  # (-148, 993) (335, -947)
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)

        # ===============================CAB================================ #
        xDis = x2 - x1  # x的增量
        yDis = y2 - y1  # y的增量
        if (abs(xDis) > abs(yDis)):
            maxstep = abs(xDis)
        else:
            maxstep = abs(yDis)
        xUnitstep = xDis / maxstep  # x每步骤增量
        yUnitstep = yDis / maxstep  # y的每步增量
        x = x1
        y = y1
        average_gray = []
        for k in range(maxstep):
            x = x + xUnitstep
            y = y + yUnitstep
            # print("x: %d, y:%d" % (x, y))
            if 0 < x < h and 0 < y < w:
                # print(img_gray[int(x), int(y)])
                average_gray.append(img[int(x), int(y)])
        print('第{}霍夫直线的平均灰度值：'.format(n), mean(average_gray))  # 平均115，阴影的边界在125以上，堵料的边界在105左右
        # ================================================================== #

    print('直线的数量：', len(lines))
else:
    print('直线的数量：', 0)

# 可视化图像
cv2.imshow('0', img)
cv2.imshow('1', image_edge)
cv2.waitKey(0)
