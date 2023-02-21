# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/9 14:51
@File : 008_line_detect.py
@Desc : 
"""
import math

import cv2
import numpy as np
from matplotlib import pyplot as plt

from utils.time_util import TimeUtil


def line_detect(imagePath):
    # 读取图片
    image = cv2.imread(imagePath)
    # 将图片转换为HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 设置阈值
    lowera = np.array([0, 0, 221])
    uppera = np.array([180, 30, 255])
    mask1 = cv2.inRange(hsv, lowera, uppera)
    kernel = np.ones((3, 3), np.uint8)

    # 对得到的图像进行形态学操作（闭运算和开运算）
    mask = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)  # 闭运算：表示先进行膨胀操作，再进行腐蚀操作
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 开运算：表示的是先进行腐蚀，再进行膨胀操作

    # 绘制轮廓
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    # 显示图片
    resPath = r"D:\projects\python\pylearning\files\pics\res_pic\tmp.png"
    cv2.imencode(".png", edges)[1].tofile(resPath)  # 保存
    cv2.imshow("edges", edges)
    # 检测白线  这里是设置检测直线的条件，可以去读一读HoughLinesP()函数，然后根据自己的要求设置检测条件
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength=10, maxLineGap=10)
    print("lines=", lines)
    print("========================================================")
    i = 1
    # 对通过霍夫变换得到的数据进行遍历
    for line in lines:
        # newlines1 = lines[:, 0, :]
        print("line[" + str(i - 1) + "]=", line)
        x1, y1, x2, y2 = line[0]  # 两点确定一条直线，这里就是通过遍历得到的两个点的数据 （x1,y1）(x2,y2)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 在原图上画线
        # 转换为浮点数，计算斜率
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        print("x1=%s,x2=%s,y1=%s,y2=%s" % (x1, x2, y1, y2))
        if x2 - x1 == 0:
            print("直线是竖直的")
            result = 90
        elif y2 - y1 == 0:
            print("直线是水平的")
            result = 0
        else:
            # 计算斜率
            k = -(y2 - y1) / (x2 - x1)
            # 求反正切，再将得到的弧度转换为度
            result = np.arctan(k) * 57.29577
            print("直线倾斜角度为：" + str(result) + "度")
        i = i + 1
    #   显示最后的成果图
    resPath = r"D:\projects\python\pylearning\files\pics\res_pic\res.png"
    cv2.imencode(".png", image)[1].tofile(resPath)  # 保存
    cv2.imshow("line_detect", image)
    return result


def line_detect_001(imagePath):
    # 读取图片
    image = cv2.imread(imagePath)
    image_copy = image.copy()

    # 转换成灰度图
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 边缘检测, Sobel算子大小为3
    edges = cv2.Canny(image_gray, 170, 220, apertureSize=3)

    # 霍夫曼直线检测(标准霍夫线变换)
    """
    参数:
    image:边缘检测的输出图像. 它应该是个灰度图 (但事实上是个二值化图)
    lines:储存着检测到的直线的参数对(r,θ)的容器
    rho:参数极径r以像素值为单位的分辨率. 我们使用1像素.
    theta:参数极角以弧度为单位的分辨率. 我们使用11度(即CV_PI/180)
    theta:要”检测” 一条直线所需最少的的曲线交点
    srn and stn: 参数默认为0.
    """
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 250)

    # 遍历
    for line in lines:
        # 获取rho和theta
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(image_copy, (x1, y1), (x2, y2), (0, 0, 255), thickness=5)

    # 图片展示
    f, ax = plt.subplots(2, 2, figsize=(12, 12))

    # 子图
    ax[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax[0, 1].imshow(image_gray, "gray")
    ax[1, 0].imshow(edges, "gray")
    ax[1, 1].imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))

    # 标题
    ax[0, 0].set_title("original")
    ax[0, 1].set_title("image gray")
    ax[1, 0].set_title("image edge")
    ax[1, 1].set_title("image line")

    plt.show()


def am_run(self):
    while True:
        ret, frame = self.cap.read()
        if frame is None:
            print('video picture is none --continue ')
            continue

        gray = frame.copy()
        # cv2.imshow('origin', gray)

        # 匹配模板 框出匹配区域
        image = gray.copy()
        maxval, t_left, b_right = self.get_match(gray)
        if maxval < 16000000000:  # 对匹配程度做判断
            print("---------------------------------------")
            print('matchTemplate is not enough --continue')
            print("---------------------------------------")
            result = frame
            image = frame
        else:

            cv2.rectangle(image, t_left, b_right, 255, 2)

            # 高斯除噪
            kernel = np.ones((6, 6), np.float32) / 36
            gray_cut_filter2D = cv2.filter2D(image[t_left[1]:t_left[1] + self.h, t_left[0]:t_left[0] + self.w], -1,
                                             kernel)

            # 灰度图 二值化
            gray_img = cv2.cvtColor(gray_cut_filter2D, cv2.COLOR_BGR2GRAY)
            ret, thresh1 = cv2.threshold(gray_img, 180, 255, cv2.THRESH_BINARY)

            # 二值化后 分割主要区域 减小干扰 模板图尺寸371*369
            tm = thresh1.copy()
            test_main = tm[50:319, 50:321]

            # 边缘化检测
            edges = cv2.Canny(test_main, 50, 150, apertureSize=3)

            # 霍夫直线
            lines = cv2.HoughLines(edges, 1, np.pi / 180, 60)
            if lines is None:
                continue
            result = edges.copy()

            for line in lines[0]:
                rho = line[0]  # 第一个元素是距离rho
                theta = line[1]  # 第二个元素是角度theta
                print('distance:' + str(rho), 'theta:' + str(((theta / np.pi) * 180)))
                lbael_text = 'distance:' + str(round(rho)) + 'theta:' + str(round((theta / np.pi) * 180 - 90, 2))
                cv2.putText(image, lbael_text, (t_left[0], t_left[1] - 12), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if (theta > 3 * (np.pi / 3)) or (theta < (np.pi / 2)):  # 从图像边界画出延长直线
                    # 该直线与第一行的交点
                    pt1 = (int(rho / np.cos(theta)), 0)
                    # 该直线与最后一行的焦点
                    pt2 = (int((rho - result.shape[0] * np.sin(theta)) / np.cos(theta)), result.shape[0])
                    # 绘制一条白线
                    cv2.line(result, pt1, pt2, 255, 1)
                    # print('theat >180 theta<90')

                else:  # 水平直线
                    # 该直线与第一列的交点
                    pt1 = (0, int(rho / np.sin(theta)))
                    # 该直线与最后一列的交点
                    pt2 = (result.shape[1], int((rho - result.shape[1] * np.cos(theta)) / np.sin(theta)))
                    # 绘制一条直线
                    cv2.line(result, pt1, pt2, 255, 1)

        cv2.imshow('result', result)
        cv2.imshow('rectangle', image)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break


def cross_point(line1, line2):  # 计算交点函数
    x1 = line1[0]  # 取直线1的第一个点坐标
    y1 = line1[1]
    x2 = line1[2]  # 取直线1的第二个点坐标
    y2 = line1[3]

    x3 = line2[0]  # 取直线2的第一个点坐标
    y3 = line2[1]
    x4 = line2[2]  # 取直线2的第二个点坐标
    y4 = line2[3]

    if x2 - x1 == 0:  # L1 直线斜率不存在
        k1 = None
        b1 = 0
    else:
        k1 = (y2 - y1) * 1.0 / (x2 - x1)  # 计算k1,由于点均为整数，需要进行浮点数转化
        b1 = y1 * 1.0 - x1 * k1 * 1.0  # 整型转浮点型是关键

    if (x4 - x3) == 0:  # L2直线斜率不存在操作
        k2 = None
        b2 = 0
    else:
        k2 = (y4 - y3) * 1.0 / (x4 - x3)  # 斜率存在操作
        b2 = y3 * 1.0 - x3 * k2 * 1.0

    if k1 is None and k2 is None:  # L1与L2直线斜率都不存在，两条直线均与y轴平行
        if x1 == x3:  # 两条直线实际为同一直线
            return [x1, y1]  # 均为交点，返回任意一个点
        else:
            return None  # 平行线无交点
    elif k1 is not None and k2 is None:  # 若L2与y轴平行，L1为一般直线，交点横坐标为L2的x坐标
        x = x3
        y = k1 * x * 1.0 + b1 * 1.0
    elif k1 is None and k2 is not None:  # 若L1与y轴平行，L2为一般直线，交点横坐标为L1的x坐标
        x = x1
        y = k2 * x * 1.0 + b2 * 1.0
    else:  # 两条一般直线
        if k1 == k2:  # 两直线斜率相同
            if b1 == b2:  # 截距相同，说明两直线为同一直线，返回任一点
                return [x1, y1]
            else:  # 截距不同，两直线平行，无交点
                return None
        else:  # 两直线不平行，必然存在交点
            x = (b2 - b1) * 1.0 / (k1 - k2)
            y = k1 * x * 1.0 + b1 * 1.0
    return [x, y]

def line_detect_002(imagePath):
    """
    检测线
    :param imagePath: 图片路径
    :return:
    """
    # 读取图片
    image = cv2.imread(imagePath)
    image_copy = image.copy()

    # 高斯除噪
    # kernel = np.ones((6, 6), np.float32) / 36
    # gray_cut_filter2D = cv2.filter2D(image_copy, -1, kernel)
    # image_gray = cv2.cvtColor(gray_cut_filter2D, cv2.COLOR_BGR2GRAY)

    # 转换成灰度图
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 边缘检测, Sobel算子大小为3
    """
    其中：
    edges 为计算得到的边缘图像。
    image 为 8 位输入图像。
    threshold1 表示处理过程中的第一个阈值。
    threshold2 表示处理过程中的第二个阈值。
    apertureSize 表示 Sobel 算子的孔径大小。
    L2gradient 为计算图像梯度幅度（gradient magnitude）的标识。其默认值为 False。如果为 True，则使用更精确的 L2 范数进行计算（即两个方向的导数的平方和再开方），否则使用 L1 范数（直接将两个方向导数的绝对值相加）。
    """
    edges = cv2.Canny(image_gray, 170, 220, apertureSize=3)
    # edges = cv2.Canny(image_gray, 170, 150, apertureSize=3)

    # 霍夫曼直线检测(统计霍夫变换)
    """
    参数：
    image: 边缘检测的输出图像. 它应该是个灰度图 (但事实上是个二值化图) * 
    lines: 储存着检测到的直线的参数对  的容器，也就是线段两个端点的坐标
    rho : 　参数极径  以像素值为单位的分辨率. 我们使用 1 像素.
    theta: 参数极角  以弧度为单位的分辨率. 我们使用 1度 (即CV_PI/180)
    threshold: 要”检测” 一条直线所需最少的的曲线交点 
    minLinLength: 能组成一条直线的最少点的数量. 点数量不足的直线将被抛弃.线段的最小长度
    maxLineGap:线段上最近两点之间的阈值
    """
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

    # 遍历
    if lines is not None:
        if len(lines) >= 2:
            line1x1, line1y1, line1x2, line1y2 = lines[0][0]
            line2x1, line2y1, line2x2, line2y2 = lines[1][0]
            line1 = [line1x1, line1y1, line1x2, line1y2]
            line2 = [line2x1, line2y1, line2x2, line2y2]
            print(f"point = {cross_point(line1, line2)}")
        for i, line in enumerate(lines):
            # 获取坐标
            x1, y1, x2, y2 = line[0]
            cv2.line(image_copy, (x1, y1), (x2, y2), (0, 0, 255), thickness=3)
            # 转换为浮点数，计算斜率
            x1 = float(x1)
            x2 = float(x2)
            y1 = float(y1)
            y2 = float(y2)
            print(f"line[{i}], 点[({x1}, {y1}), ({x2}, {y2})]")
            if x2 - x1 == 0:
                print("直线是竖直的")
                result = 90
            elif y2 - y1 == 0:
                print("直线是水平的")
                result = 0
            else:
                # 计算斜率
                k = -(y2 - y1) / (x2 - x1)
                # 求反正切，再将得到的弧度转换为度
                result = np.arctan(k) * 57.29577
                print("直线倾斜角度为：" + str(result) + "度")
    # cv2.namedWindow("resultImage", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("resultImage", image_copy)
    # 图片展示
    f, ax = plt.subplots(2, 2, figsize=(12, 12))
    resdir = r"D:\projects\python\pylearning\files\pics\res_pic"
    resPath = f"{resdir}\\{TimeUtil.get_now_time_mill_under()}.png"
    # cv2.imencode(".png", image_copy)[1].tofile(resPath)  # 保存
    # 子图
    ax[0, 0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    ax[0, 1].imshow(image_gray, "gray")
    ax[1, 0].imshow(edges, "gray")
    ax[1, 1].imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))

    # 标题
    ax[0, 0].set_title("original")
    ax[0, 1].set_title("image gray")
    ax[1, 0].set_title("image edge")
    ax[1, 1].set_title("image line")

    plt.show()


def line_detect_003(imagePath):
    image = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), cv2.IMREAD_COLOR)
    # 将图片转换为HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # 设置阈值
    lowera = np.array([0, 0, 221])
    uppera = np.array([180, 30, 255])
    mask1 = cv2.inRange(hsv, lowera, uppera)
    kernel = np.ones((3, 3), np.uint8)

    # 对得到的图像进行形态学操作（闭运算和开运算）
    mask = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernel)  # 闭运算：表示先进行膨胀操作，再进行腐蚀操作
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 开运算：表示的是先进行腐蚀，再进行膨胀操作

    # 绘制轮廓
    edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    # edges = cv2.Canny(mask, 50, 150, apertureSize=3)
    # 显示图片
    cv2.imshow("edges", edges)
    # 检测白线  这里是设置检测直线的条件，可以去读一读HoughLinesP()函数，然后根据自己的要求设置检测条件
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength=10, maxLineGap=10)
    # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, minLineLength=100, maxLineGap=10)
    print(f"lines={lines}")
    print("========================================================")
    i = 1
    # 对通过霍夫变换得到的数据进行遍历
    for line in lines:
        # newlines1 = lines[:, 0, :]
        print("line[" + str(i - 1) + "]=", line)
        x1, y1, x2, y2 = line[0]  # 两点确定一条直线，这里就是通过遍历得到的两个点的数据 （x1,y1）(x2,y2)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)  # 在原图上画线
        # 转换为浮点数，计算斜率
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        print("x1=%s,x2=%s,y1=%s,y2=%s" % (x1, x2, y1, y2))
        if x2 - x1 == 0:
            print("直线是竖直的")
            result = 90
        elif y2 - y1 == 0:
            print("直线是水平的")
            result = 0
        else:
            # 计算斜率
            k = -(y2 - y1) / (x2 - x1)
            # 求反正切，再将得到的弧度转换为度
            result = np.arctan(k) * 57.29577
            print("直线倾斜角度为：" + str(result) + "度")
        i = i + 1
    #   显示最后的成果图
    cv2.imshow("line_detect", image)
    return result


def getDist_P2L(PointP, Pointa, Pointb):
    """
    # ***** 点到直线的距离:P到AB的距离*****
    # P为线外一点，AB为线段两个端点
    计算点到直线的距离
    PointP：定点坐标
    Pointa：直线a点坐标
    Pointb：直线b点坐标
    """
    # 求直线方程
    A = Pointa[1] - Pointb[1]
    B = Pointb[0] - Pointa[0]
    C = Pointa[0] * Pointb[1] - Pointa[1] * Pointb[0]
    # 代入点到直线距离公式
    distance = (A * PointP[0] + B * PointP[1] + C) / math.sqrt(A * A + B * B)
    print(f"distance={distance}")
    return distance


if __name__ == '__main__':
    # imagePath = r"D:\projects\python\pylearning\files\pics\meter\002_tmp_ori.png"
    imagePath = r"D:\projects\python\pylearning\files\pics\meter\ico_0c.png"
    # # 读入图片
    # src = cv2.imread(r"D:\tmp\lines.png")
    # # 设置窗口大小
    # cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
    # # 显示原始图片
    # cv2.imshow("input image", src)
    # # 调用函数
    # line_detect(src)
    # cv2.waitKey(0)
    # line_detect(r"D:\projects\python\pylearning\files\pics\meter\speed_meter_temp.png")
    # line_detect_001(r"D:\projects\python\pylearning\files\pics\meter\speed_meter_temp.png")
    # line_detect_002(r"D:\projects\python\pylearning\files\pics\meter\002.jpg")
    # line_detect_002(r"D:\projects\python\pylearning\files\pics\meter\speed_meter_temp.png")
    line_detect_002(imagePath)
    # line_detect_002(r"D:\projects\python\pylearning\files\pics\meter\tmp_speed.png")
    # line_detect_002(r"C:\Users\tonse\Pictures\tmp\v3_4_20.png")
    # line_detect_002(r"D:\projects\python\pylearning\files\pics\meter\ico_0c.png")
    # line_detect_002(r"D:\projects\python\pylearning\files\pics\meter\001_meter.png")
    # line_detect_002(r"D:\projects\python\pylearning\files\pics\meter\speed_meter_real.jpg")
    # # 读入图片
    # src = cv2.imread(imagePath)
    # # 设置窗口大小
    # cv2.namedWindow("input image", cv2.WINDOW_AUTOSIZE)
    # # 显示原始图片
    # cv2.imshow("input image", src)
    # # 调用函数
    # line_detect_003(imagePath)
    # cv2.waitKey(0)
    # getDist_P2L([565, 404], [200, 404], [720, 404])
