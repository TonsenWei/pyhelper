# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/16 18:05
@File : meter_001.py
@Desc : 
"""
import copy
import math
import time

import cv2
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from math import cos, pi, sin

# from 计算刻度值 import get_rad_val
from utils.time_util import TimeUtil

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
method = cv2.TM_CCOEFF

def isinpolygon(point, vertex_lst: list, contain_boundary=True):
    # 检测点是否位于区域外接矩形内
    lngaxis, lataxis = zip(*vertex_lst)
    minlng, maxlng = min(lngaxis), max(lngaxis)
    minlat, maxlat = min(lataxis), max(lataxis)
    lng, lat = point
    if contain_boundary:
        isin = (minlng <= lng <= maxlng) & (minlat <= lat <= maxlat)
    else:
        isin = (minlng < lng < maxlng) & (minlat < lat < maxlat)
    return isin


def isintersect(poi, spoi, epoi):
    # 输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    # 射线为向东的纬线
    # 可能存在的bug，当区域横跨本初子午线或180度经线的时候可能有问题
    lng, lat = poi
    slng, slat = spoi
    elng, elat = epoi
    if poi == spoi:
        # print("在顶点上")
        return None
    if slat == elat:  # 排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if slat > lat and elat > lat:  # 线段在射线上边
        return False
    if slat < lat and elat < lat:  # 线段在射线下边
        return False
    if slat == lat and elat > lat:  # 交点为下端点，对应spoint
        return False
    if elat == lat and slat > lat:  # 交点为下端点，对应epoint
        return False
    if slng < lng and elat < lat:  # 线段在射线左边
        return False
    # 求交点
    xseg = elng - (elng - slng) * (elat - lat) / (elat - slat)
    if xseg == lng:
        # print("点在多边形的边上")
        return None
    if xseg < lng:  # 交点在射线起点的左侧
        return False
    return True  # 排除上述情况之后


def isin_multipolygon(poi, vertex_lst, contain_boundary=True):
    # 判断是否在外包矩形内，如果不在，直接返回false
    if not isinpolygon(poi, vertex_lst, contain_boundary):
        return False
    sinsc = 0
    for spoi, epoi in zip(vertex_lst[:-1], vertex_lst[1::]):
        intersect = isintersect(poi, spoi, epoi)
        if intersect is None:
            return (False, True)[contain_boundary]
        elif intersect:
            sinsc += 1
    return sinsc % 2 == 1

def get_match_rect(template, img, method):
    '''获取模板匹配的矩形的左上角和右下角的坐标'''
    w, h = template.shape[1], template.shape[0]
    res = cv2.matchTemplate(img, template, method)
    mn_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # 使用不同的方法，对结果的解释不同
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return top_left, bottom_right


def get_center_point(top_left, bottom_right):
    '''传入左上角和右下角坐标，获取中心点'''
    c_x, c_y = ((np.array(top_left) + np.array(bottom_right)) / 2).astype(np.int64)
    return c_x, c_y


def get_circle_field_color(img, center, r, thickness):
    '''获取中心圆形区域的色值集'''
    temp = img.copy().astype(np.int)
    cv2.circle(temp, center, r, -100, thickness=thickness)
    return img[temp == -100]


def v2_by_center_circle(img, colors):
    '''二值化通过中心圆的颜色集合'''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            a = img[i, j]
            if a in colors:
                img[i, j] = 0
            else:
                img[i, j] = 255


def v2_by_k_means(img):
    '''使用k-means二值化'''
    original_img = np.array(img, dtype=np.float64)
    src = original_img.copy()
    delta_y = int(original_img.shape[0] * (0.4))
    delta_x = int(original_img.shape[1] * (0.4))
    original_img = original_img[delta_y:-delta_y, delta_x:-delta_x]
    h, w, d = src.shape
    print(w, h, d)
    dts = min([w, h])
    print(dts)
    r2 = (dts / 2) ** 2
    c_x, c_y = w / 2, h / 2
    a: np.ndarray = original_img[:, :, 0:3].astype(np.uint8)
    # 获取尺寸(宽度、长度、深度)
    height, width = original_img.shape[0], original_img.shape[1]
    depth = 3
    print(depth)
    image_flattened = np.reshape(original_img, (width * height, depth))
    '''
    用K-Means算法在颜色样本中建立2个类。
    '''
    image_array_sample = shuffle(image_flattened, random_state=0)
    estimator = KMeans(n_clusters=2, random_state=0)
    estimator.fit(image_array_sample)
    '''
    我们为原始图片的每个像素进行类的分配。
    '''
    src_shape = src.shape
    new_img_flattened = np.reshape(src, (src_shape[0] * src_shape[1], depth))
    cluster_assignments = estimator.predict(new_img_flattened)
    compressed_palette = estimator.cluster_centers_
    print(compressed_palette)
    a = np.apply_along_axis(func1d=lambda x: np.uint8(compressed_palette[x]), arr=cluster_assignments, axis=0)
    img = a.reshape(src_shape[0], src_shape[1], depth)
    print(compressed_palette[0, 0])
    threshold = (compressed_palette[0, 0] + compressed_palette[1, 0]) / 2
    img[img[:, :, 0] > threshold] = 255
    img[img[:, :, 0] < threshold] = 0
    cv2.imshow('sd0', img)
    for x in range(w):
        for y in range(h):
            distance = ((x - c_x) ** 2 + (y - c_y) ** 2)
            if distance > r2:
                img[y, x] = (255, 255, 255)
    cv2.imshow('sd', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img


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
    # print(f"distance={distance}")
    return distance


def get_pointer_rad(img):
    '''获取角度'''
    shape = img.shape
    c_y, c_x, depth = int(shape[0] / 2), int(shape[1] / 2), shape[2]  # 中心点，深度
    # 实际中心点
    c_y, c_x = 409, 406
    x1 = c_x + c_x * 0.8
    src = img.copy()
    freq_list = []
    # 顺时针
    # pointTarget = [213, 585]  # 0 角度=136, 圆心(402, 404), 线的点(170.66032021108973, 627.4021319396135), dis=1.0899281554545146
    # pointTarget = [205, 465]  # 20 角度=162, 圆心(402, 404), 线的点(96.14022435947862, 503.3798653909831), dis=2.8619003978603166
    pointTarget = [579,
                   595]  # 160 角度=47, 圆心(402, 404), 线的点(621.3306725960995, 639.2033504407252), dis=0.8120815853439651
    # 全部刻度 角度数 = 360 - （136 - 47） = 360 - 89 = 271
    # 每角度刻度值 = 160/271 = 0.5904059
    # 角度162对应的值 = （162-136）* 0.5904059 = 26*0.5904059 =
    for i in range(361):
        x = (x1 - c_x) * cos(i * pi / 180) + c_x
        y = (x1 - c_x) * sin(i * pi / 180) + c_y
        # print(f"角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y})")
        temp = src.copy()
        dis = getDist_P2L(pointTarget, [c_x, c_y], [x, y])
        if abs(dis) < 3:
            print(f"角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), dis={dis}")
        cv2.line(temp, (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)  # 画线
        t1 = img.copy()
        t1[temp[:, :, 2] == 255] = 255
        c = img[temp[:, :, 2] == 255]
        # print(f"type(c) = {type(c)}")  # numpy.ndarray
        points = c[c == 0]
        # print(f"points= {points}")
        freq_list.append((len(points), i))
        cv2.imshow('d', temp)
        cv2.imshow('d1', t1)
        cv2.waitKey(1)
        if i == 0:
            print(freq_list[0])
    print('当前角度：', max(freq_list, key=lambda x: x[0]), '度')  # 当前角度： (3546, 139) 度
    cv2.destroyAllWindows()
    rad = max(freq_list, key=lambda x: x[0])
    return rad


def get_meter_value_bak(img, center, pointZero, pointMax, pointTarget, maxValue):
    """
    获取某点对应的数值
    :param img: 图片，模板匹配后从测试图中截取出的图片
    :param center: 中心点
    :param pointZero: 0值坐标
    :param pointMax: 最大值坐标
    :param pointTarget: 目标值坐标
    :param maxValue: 刻度值范围
    :return:
    """
    '''获取角度'''
    shape = img.shape
    c_y, c_x, depth = int(shape[0] / 2), int(shape[1] / 2), shape[2]  # 中心点，深度
    # 实际中心点
    c_y, c_x = center[1], center[0]
    degreeZeroValue = 0
    degreeMaxValue = 0
    degreeTargetValue = 0
    zeroFound = False
    targetFound = False
    maxFound = False
    x1 = c_x + c_x * 0.8
    src = img.copy()
    freq_list = []
    # 顺时针
    # pointTarget = [213, 585]  # 0 角度=136, 圆心(402, 404), 线的点(170.66032021108973, 627.4021319396135), dis=1.0899281554545146
    # pointTarget = [205, 465]  # 20 角度=162, 圆心(402, 404), 线的点(96.14022435947862, 503.3798653909831), dis=2.8619003978603166
    # pointTarget = [579, 595]  # 160 角度=47, 圆心(402, 404), 线的点(621.3306725960995, 639.2033504407252), dis=0.8120815853439651
    # 全部刻度 角度数 = 360 - （136 - 47） = 360 - 89 = 271
    # 每角度刻度值 = 160/271 = 0.5904059
    # 角度162对应的值 = （162-136）* 0.5904059 = 26*0.5904059 =
    for i in range(361):
        x = (x1 - c_x) * cos(i * pi / 180) + c_x
        y = (x1 - c_x) * sin(i * pi / 180) + c_y
        # print(f"角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y})")
        temp = src.copy()
        offset = 3
        lineRect = [[int(c_x), int(c_y)], [int(x), int(y)], [int(c_x+offset), int(c_y+offset)],  [int(x+offset), int(y+offset)]]
        res = isin_multipolygon(pointZero, copy.deepcopy(lineRect), contain_boundary=True)
        resMax = isin_multipolygon(pointMax, copy.deepcopy(lineRect), contain_boundary=True)
        resTarget = isin_multipolygon(pointTarget, copy.deepcopy(lineRect), contain_boundary=True)
        if res is True and zeroFound is False:
            zeroFound = True
            degreeZeroValue = i
            print(f"0值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeZeroValue={degreeZeroValue}")
        if resMax is True and maxFound is False:
            maxFound = True
            degreeMaxValue = i
            print(f"最大值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeMaxValue={degreeMaxValue}")
        if resTarget is True and targetFound is False:
            targetFound = True
            degreeTargetValue = i
            print(f"目标值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeTargetValue={degreeTargetValue}")
        cv2.line(temp, (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)  # 画线
        t1 = img.copy()
        t1[temp[:, :, 2] == 255] = 255
        c = img[temp[:, :, 2] == 255]
        # print(f"type(c) = {type(c)}")  # numpy.ndarray
        points = c[c == 0]
        # print(f"points= {points}")
        freq_list.append((len(points), i))
        cv2.imshow('d', temp)
        cv2.imshow('d1', t1)
        cv2.waitKey(1)
    print('当前角度：', max(freq_list, key=lambda x: x[0]), '度')  # 当前角度： (3546, 139) 度
    cv2.destroyAllWindows()
    rad = max(freq_list, key=lambda x: x[0])
    print(f"0值角度={degreeZeroValue}, 最大值角度={degreeMaxValue}, 目标值角度={degreeTargetValue}")
    # 一般情况，degreeMaxValue < degreeZeroValue < degreeTargetValue
    if degreeMaxValue < degreeZeroValue < degreeTargetValue:
        # 先到最大刻度，再到0刻度，再到目标刻度
        valueDegrees = 360 - (degreeZeroValue - degreeMaxValue)  # 有效刻度所占的所有角度值 = 360 - 无效角度
        perDegreeValue = maxValue / valueDegrees  # 每个角度占的值
        targetValue = (degreeTargetValue - degreeZeroValue) * perDegreeValue  # 目标角度对应的值
    elif degreeZeroValue < degreeTargetValue < degreeMaxValue:
        # 先找到0刻度，再到目标刻度，再到最大刻度
        valueDegrees = degreeMaxValue - degreeZeroValue  # 有效刻度所占的所有角度值 = 360 - 无效角度
        perDegreeValue = maxValue / valueDegrees  # 每个角度占的值
        targetValue = (degreeTargetValue - degreeZeroValue) * perDegreeValue  # 目标角度对应的值
    elif degreeTargetValue < degreeMaxValue < degreeZeroValue:
        # 先找到目标刻度，再到最大刻度，再到0刻度
        valueDegrees = 360 - (degreeZeroValue - degreeMaxValue)  # 有效刻度所占的所有角度值 = 360 - 无效角度
        leftDegree = degreeMaxValue - degreeTargetValue  # 目标刻度到最大刻度之差
        realTargetDegree = valueDegrees - leftDegree  # 目标刻度总角度
        perDegreeValue = maxValue / valueDegrees  # 每个角度占的值
        targetValue = realTargetDegree * perDegreeValue  # 目标角度对应的值
    elif degreeTargetValue == degreeZeroValue:
        targetValue = 0
    elif degreeTargetValue == degreeTargetValue:
        targetValue = maxValue
    if targetValue > maxValue:
        targetValue = maxValue
    print(f"targetValue = {round(targetValue, 1)}")
    return rad


def get_meter_value(center, pointZero, pointMax, pointTarget, maxValue):
    """
    获取某点对应的数值
    :param center: 中心点
    :param pointZero: 0值坐标
    :param pointMax: 最大值坐标
    :param pointTarget: 目标值坐标
    :param maxValue: 刻度值范围
    :return:
    """
    '''获取角度'''
    # 实际中心点
    c_y, c_x = center[1], center[0]
    degreeZeroValue = 0
    degreeMaxValue = 0
    degreeTargetValue = 0
    zeroFound = False
    targetFound = False
    maxFound = False
    x1 = c_x + c_x * 0.8
    targetValue = 0
    for i in range(361):
        x = (x1 - c_x) * cos(i * pi / 180) + c_x
        y = (x1 - c_x) * sin(i * pi / 180) + c_y
        # print(f"角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y})")
        offset = 3
        lineRect = [[int(c_x), int(c_y)], [int(x), int(y)], [int(c_x+offset), int(c_y+offset)],  [int(x+offset), int(y+offset)]]
        res = isin_multipolygon(pointZero, copy.deepcopy(lineRect), contain_boundary=True)
        resMax = isin_multipolygon(pointMax, copy.deepcopy(lineRect), contain_boundary=True)
        resTarget = isin_multipolygon(pointTarget, copy.deepcopy(lineRect), contain_boundary=True)
        if res is True and zeroFound is False:
            zeroFound = True
            degreeZeroValue = i
            print(f"0值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeZeroValue={degreeZeroValue}")
        if resMax is True and maxFound is False:
            maxFound = True
            degreeMaxValue = i
            print(f"最大值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeMaxValue={degreeMaxValue}")
        if resTarget is True and targetFound is False:
            targetFound = True
            degreeTargetValue = i
            print(f"目标值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeTargetValue={degreeTargetValue}")
    print(f"0值角度={degreeZeroValue}, 最大值角度={degreeMaxValue}, 目标值角度={degreeTargetValue}")
    # 一般情况，degreeMaxValue < degreeZeroValue < degreeTargetValue
    if degreeMaxValue < degreeZeroValue < degreeTargetValue:
        # 先到最大刻度，再到0刻度，再到目标刻度
        valueDegrees = 360 - (degreeZeroValue - degreeMaxValue)  # 有效刻度所占的所有角度值 = 360 - 无效角度
        perDegreeValue = maxValue / valueDegrees  # 每个角度占的值
        targetValue = (degreeTargetValue - degreeZeroValue) * perDegreeValue  # 目标角度对应的值
    elif degreeZeroValue < degreeTargetValue < degreeMaxValue:
        # 先找到0刻度，再到目标刻度，再到最大刻度
        valueDegrees = degreeMaxValue - degreeZeroValue  # 有效刻度所占的所有角度值 = 360 - 无效角度
        perDegreeValue = maxValue / valueDegrees  # 每个角度占的值
        targetValue = (degreeTargetValue - degreeZeroValue) * perDegreeValue  # 目标角度对应的值
    elif degreeTargetValue < degreeMaxValue < degreeZeroValue:
        # 先找到目标刻度，再到最大刻度，再到0刻度
        valueDegrees = 360 - (degreeZeroValue - degreeMaxValue)  # 有效刻度所占的所有角度值 = 360 - 无效角度
        leftDegree = degreeMaxValue - degreeTargetValue  # 目标刻度到最大刻度之差
        realTargetDegree = valueDegrees - leftDegree  # 目标刻度总角度
        perDegreeValue = maxValue / valueDegrees  # 每个角度占的值
        targetValue = realTargetDegree * perDegreeValue  # 目标角度对应的值
    elif degreeTargetValue == degreeZeroValue:
        targetValue = 0
    elif degreeTargetValue == degreeTargetValue:
        targetValue = maxValue
    if targetValue > maxValue:
        targetValue = maxValue
    print(f"targetValue = {round(targetValue, 1)}")
    return targetValue


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

def line_detect(imagePath, center):
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
    targetPoint = []
    if lines is not None:
        if len(lines) >= 2:
            line1x1, line1y1, line1x2, line1y2 = lines[0][0]
            line2x1, line2y1, line2x2, line2y2 = lines[1][0]
            line1 = [line1x1, line1y1, line1x2, line1y2]
            line2 = [line2x1, line2y1, line2x2, line2y2]
            targetPoint = cross_point(line1, line2)
            print(f"point = {targetPoint}")
        elif len(lines) == 1:
            line1x1, line1y1, line1x2, line1y2 = lines[0][0]
            disP1 = math.sqrt(pow(center[0]-line1x1, 2) + pow(center[1]-line1y1, 2))
            disP2 = math.sqrt(pow(center[0]-line1x2, 2) + pow(center[1]-line1y2, 2))
            print(f"disP1 = {disP1}, disP2={disP2}")
            if disP1 >= disP2:
                targetPoint = [line1x1, line1y1]
            else:
                targetPoint = [line1x2, line1y2]
            print(f"targetPoint={targetPoint}")
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
                # print("直线倾斜角度为：" + str(result) + "度")
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
    return targetPoint

if __name__ == '__main__':
    # 获取测试图像
    # testPicPath = r'D:\projects\python\pylearning\files\pics\meter\002.jpg'  # (3546, 139) 度
    # testPicPath = r'D:\projects\python\pylearning\files\pics\meter\002_tmp_ori.png'  # (3546, 139) 度
    # tmpPicPath = r'D:\projects\python\pylearning\files\pics\meter\002_tmp_ori.png'
    # testPicPath = r'D:\projects\python\pylearning\files\pics\meter\ico_0c.png'  # (3546, 139) 度
    # tmpPicPath = r'D:\projects\python\pylearning\files\pics\meter\ico_0c.png'
    # testPicPath = r'D:\projects\python\pylearning\files\pics\meter\meter_0c.png'  # rad = (1125, 124)
    # tmpPicPath = r'D:\projects\python\pylearning\files\pics\meter\ico_0c.png'
    # img_s = cv2.imread(testPicPath)
    # img = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
    # template = cv2.imread(tmpPicPath)
    # template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    # # 匹配并返回矩形坐标
    # top_left, bottom_right = get_match_rect(template, img, method)
    # c_x, c_y = get_center_point(top_left, bottom_right)
    # print(c_x, c_y)
    # # 绘制矩形
    # cv2.rectangle(img_s, top_left, bottom_right, 255, 2)
    # cv2.imshow('img', cv2.resize(img_s, (int(img.shape[1] * 0.5), int(img.shape[0] * 0.5))))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # #################################################################
    # new = img_s[top_left[1]:bottom_right[1] + 1, top_left[0]:bottom_right[0] + 1]
    # template = cv2.imread(tmpPicPath)
    # top_left, bottom_right = get_match_rect(template, new, method=method)
    # new_ = new[top_left[1]:bottom_right[1] + 1, top_left[0]:bottom_right[0] + 1]
    # # 二值化图像
    # cv2.imshow('ererss', new_)
    # img = v2_by_k_means(new_)
    # print("start get_pointer_rad")
    # rad = get_pointer_rad(img)
    #################################################################
    # print(get_rad_val(rad[1]), '对应刻度')
    # pointTarget = [213, 585]  # 0 角度=136, 圆心(402, 404), 线的点(170.66032021108973, 627.4021319396135), dis=1.0899281554545146
    # pointTarget = [205, 465]  # 20 角度=162, 圆心(402, 404), 线的点(96.14022435947862, 503.3798653909831), dis=2.8619003978603166
    # pointTarget = [579, 595]  # 160 角度=47, 圆心(402, 404), 线的点(621.3306725960995, 639.2033504407252), dis=0.8120815853439651
    # 全部刻度 角度数 = 360 - （136 - 47） = 360 - 89 = 271
    # 每角度刻度值 = 160/271 = 0.5904059
    # 角度162对应的值 = （162-136）* 0.5904059 = 26*0.5904059 =
    # pointZero = [213, 585]
    # # pointMax = [579, 595]
    # pointMax = [547, 557]
    # # pointTarget = [155, 477]  # 20
    # # pointTarget = [406, 153]  # 80
    # pointTarget = [522, 243]  # 80

    # imagePath = r"D:\projects\python\pylearning\files\pics\meter\002_tmp_ori.png"
    # imagePath = r"D:\projects\python\pylearning\files\pics\meter\ico_0c.png"
    imagePath = r"D:\projects\python\pylearning\files\pics\meter\ico_38c.png"

    # # ico_0c
    # center = [462, 454]  # 80
    # pointZero = [149, 627]
    # pointMax = [700, 598]
    # # pointTarget = [291, 142]  # 39
    # # pointTarget = [471, 101]  # 50
    # # pointTarget = [805, 459]  # 88
    # pointTarget = [int(targetPoint[0]), int(targetPoint[1])]  # 88
    # maxValue = 100
    # get_meter_value(center, pointZero, pointMax, pointTarget, maxValue)

    # ico_38c
    center = [313, 301]  # 80
    targetPoint = line_detect(imagePath, center)
    pointZero = [145, 392]
    pointMax = [505, 412]
    # pointTarget = [291, 142]  # 39
    # pointTarget = [471, 101]  # 50
    # pointTarget = [805, 459]  # 88
    pointTarget = [int(targetPoint[0]), int(targetPoint[1])]  # 88
    maxValue = 100
    get_meter_value(center, pointZero, pointMax, pointTarget, maxValue)

    # center = [408, 408]  # 80
    # pointZero = [213, 588]
    # pointMax = [580, 598]
    # pointTarget = [targetPoint[0], targetPoint[1]]  # 39
    # # pointTarget = [291, 142]  # 39
    # # pointTarget = [406, 153]  #
    # # pointTarget = [628, 538]  # 150
    # # pointTarget = [662, 404]  # 135
    # # pointTarget = [675, 595]  # 160
    # maxValue = 160
    # # get_meter_value(img, center, pointZero, pointMax, pointTarget, maxValue)
    # get_meter_value(center, pointZero, pointMax, pointTarget, maxValue)
