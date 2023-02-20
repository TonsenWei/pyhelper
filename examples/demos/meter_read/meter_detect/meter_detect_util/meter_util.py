# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/7 18:04
@File : meter_detect_util.py
@Desc : 
"""
import math

import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from math import cos, pi, sin
from fuzzywuzzy import fuzz

'''
图片匹配算法
'''
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
method = cv2.TM_CCOEFF


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
    temp = img.copy().astype(np.int64)
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
    """使用k-means二值化"""
    original_img = np.array(img, dtype=np.float64)
    src = original_img.copy()
    delta_y = int(original_img.shape[0] * (0.4))
    delta_x = int(original_img.shape[1] * (0.4))
    original_img = original_img[delta_y:-delta_y, delta_x:-delta_x]
    h, w, d = src.shape
    dts = min([w, h])
    r2 = (dts / 2) ** 2
    c_x, c_y = w / 2, h / 2
    a: np.ndarray = original_img[:, :, 0:3].astype(np.uint8)
    # 获取尺寸(宽度、长度、深度)
    height, width = original_img.shape[0], original_img.shape[1]
    depth = 3
    image_flattened = np.reshape(original_img, (width * height, depth))
    '''
    用K-Means算法在随机中选择1000个颜色样本中建立64个类。
    每个类都可能是压缩调色板中的一种颜色。
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
    '''
    我们建立通过压缩调色板和类分配结果创建压缩后的图片
    '''
    compressed_palette = estimator.cluster_centers_
    # print(compressed_palette)
    a = np.apply_along_axis(func1d=lambda x: np.uint8(compressed_palette[x]), arr=cluster_assignments, axis=0)
    img = a.reshape(src_shape[0], src_shape[1], depth)
    # print(compressed_palette[0, 0])
    threshold = (compressed_palette[0, 0] + compressed_palette[1, 0]) / 2
    img[img[:, :, 0] > threshold] = 255
    img[img[:, :, 0] < threshold] = 0
    # cv2.imshow('sd0', img)
    for x in range(w):
        for y in range(h):
            distance = ((x - c_x) ** 2 + (y - c_y) ** 2)
            if distance > r2:
                img[y, x] = (255, 255, 255)
    # cv2.imshow('sd', img)
    # cv2.waitKey(10)
    # if cv2.waitKey(100)==27:
    #     print("sd关闭")

    cv2.destroyAllWindows()
    return img


def get_pointer_rad(img, c_x, c_y):
    """获取角度"""
    shape = img.shape

    # *******kai******
    # 中心
    c_y, c_x, depth = int(shape[0] / 2), int(shape[1] / 2), shape[2]
    print('c_y, c_x: ', c_y, c_x)
    # *******kai******

    x1 = c_x + c_x * 0.8
    src = img.copy()

    freq_list = []

    for i in range(361):
        x = (x1 - c_x) * cos(i * pi / 180) + c_x
        y = (x1 - c_x) * sin(i * pi / 180) + c_y

        temp = src.copy()

        cv2.line(temp, (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)  # 在temp中画一条（c_x,c_y）到点（x，y）的红色的直线

        t1 = img.copy()
        t1[temp[:, :, 2] == 255] = 255  # 如果某个刻度值对应点的红色通道灰度值为255，则将t1中同样位置的该点的颜色置为255（白色）
        c = img[temp[:, :, 2] == 255]  # 将temp中红色通道为白色（255）的位置置为True，其他为false
        points = c[c == 0]  # 将C中等于0的点位置坐标传给points
        freq_list.append((len(points), i))  # freq_list 保存points的长度和此时的角度i
        # cv2.line(temp, (c_x,c_y),(155,565), (255, 0, 0), thickness=3)  # 刻度值蓝色的直线
        # print("freq_list：",freq_list)
        # cv2.imshow('red line', temp)
        # cv2.imshow('line cover', t1)

        # 绘制坐标点！！！！！！！！！！！！！！！
        # point_list=[
        #             (220,265),
        #             (110,367), (100,300),(105,230),(125,160),(195,130),
        #             (270,130),(325,180),(360,250),(340,320),(320,350)]
        #
        #
        # for point in point_list:
        #     cv2.circle(t1, point, 3, (0, 0, 255),thickness=3)

        # cv2.imshow('img', t1)

        # cv2.waitKey(1)
        # cv2.waitKey(0)

    print('当前角度：', max(freq_list, key=lambda x: x[0]), '度')  # 取长度最大，即指针覆盖面积最大的点（位置）

    cv2.destroyAllWindows()

    return max(freq_list, key=lambda x: x[0])


def get_pointer_rad_2(img, c_x, c_y):
    """
    获取角度
    无用方法，不能使用模板匹配得到的中心坐标
    """
    shape = img.shape

    # *******kai******
    # 中心
    c_y0, c_x0, depth = int(shape[0] / 2), int(shape[1] / 2), shape[2]
    print('c_y, c_x: ', c_y, c_x)
    # *******kai******

    x1 = c_x + c_x * 0.8
    src = img.copy()

    freq_list = []

    for i in range(361):
        x = (x1 - c_x) * cos(i * pi / 180) + c_x
        y = (x1 - c_x) * sin(i * pi / 180) + c_y

        temp = src.copy()

        cv2.line(temp, (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)  # 在temp中画一条（c_x,c_y）到点（x，y）的红色的直线

        t1 = img.copy()
        t1[temp[:, :, 2] == 255] = 255  # 如果某个刻度值对应点的红色通道灰度值为255，则将t1中同样位置的该点的颜色置为255（白色）
        c = img[temp[:, :, 2] == 255]  # 将temp中红色通道为白色（255）的位置置为True，其他为false
        points = c[c == 0]  # 将C中等于0的点位置坐标传给points
        freq_list.append((len(points), i))  # freq_list 保存points的长度和此时的角度i
        # cv2.line(temp, (c_x,c_y),(155,565), (255, 0, 0), thickness=3)  # 刻度值蓝色的直线
        # print("freq_list：",freq_list)
        # cv2.imshow('red line', temp)
        # cv2.imshow('line cover', t1)

        # 绘制坐标点！！！！！！！！！！！！！！！
        # point_list=[
        #             (220,265),
        #             (110,367), (100,300),(105,230),(125,160),(195,130),
        #             (270,130),(325,180),(360,250),(340,320),(320,350)]
        #
        #
        # for point in point_list:
        #     cv2.circle(t1, point, 3, (0, 0, 255),thickness=3)

        # cv2.imshow('img', t1)

        # cv2.waitKey(1)
        # cv2.waitKey(0)

    print('当前角度：', max(freq_list, key=lambda x: x[0]), '度')  # 取长度最大，即指针覆盖面积最大的点（位置）

    cv2.destroyAllWindows()

    return max(freq_list, key=lambda x: x[0])


def get_rad_val(rad, c_x, c_y, a, maxd, fir_d, sec_d, scale):
    # 计算角度
    center = [c_x, c_y]
    count = 0
    result = {}

    # *************确定zc值**************
    zc_list = {}
    for i in range(1, 10):
        zc_list[i] = dict()

    # *************确定zc值**************
    for k, v in a.items():
        r = math.acos((v[0] - center[0]) / ((v[0] - center[0]) ** 2 + (v[1] - center[1]) ** 2) ** 0.5)
        r = r * 180 / math.pi
        a[k] = r
        for i in range(1, 10):
            t_r = r
            if count >= i and k != maxd:  # 可修改，视每个表的情况而定，保证lst中递增排序
                t_r = 360 - t_r
            zc_list[i][k] = t_r
        count += 1

    new_lst = {}
    zero_lst = {}
    for i in range(1, 10):
        d = 360 - zc_list[i][fir_d] + zc_list[i][sec_d]
        d1 = 360 - zc_list[i][fir_d]
        t = fir_d + scale * (d1 / d)  # t=92，刻度为92就是0度的起始位置
        zero_lst[i] = t
        zc_list[i][t] = 0
        result_list = zc_list[i].items()
        # 匿名函数lambda：是指一类无需定义标识符（函数名）的函数或子程序。
        # lambda 函数可以接收任意多个参数 (包括可选参数) 并且返回单个表达式的值。
        # key=lambda x:x[1]
        # print(key)
        lst = sorted(result_list, key=lambda x: x[1])
        new_lst[i] = lst
    for i in range(1, 10):
        result = zc_list[i]
        lst = new_lst[i]
        t = 1
        zero = zero_lst[i]
        for k, v in lst:
            if k == zero:
                pre_key = k
                continue
            if k > pre_key and k > zero:
                if v > 90:
                    t = 0
            elif k > pre_key:
                if v < 90:
                    t = 0
            if k < pre_key and k < zero:
                if v < 90:
                    t = 0
            if k < pre_key < zero and k < zero:
                t = 0
            pre_key = k
        if t == 1:
            break
    print('result: ', result)
    print('lst: ', lst)

    # 计算读数
    old = None
    for k, v in lst:
        # print(k,v)
        if rad > v:
            old = k
    r = result[old]
    d = rad - r
    nx = get_next(old, lst)
    ttt = old + scale * abs(d / (nx[1] - r))  # 第三组
    # if(ttt>maxd):
    #     ttt=ttt-old-d
    # print("刻度:",scale)
    return ttt


def get_next(c, lst):
    l = len(lst)
    n = 0
    for i in range(len(lst)):
        if lst[i][0] == c:
            n = i + 1
            if n == l:
                n = 0
            break
    return lst[n]


class MeterUtil:

    @staticmethod
    def img_rec_result(testPicPath, templatePicPath, tempInfo):
        """
        开始读数，实际图和模板图路径，模板图片信息
        :param testPicPath: 测试图
        :param templatePicPath: 模板图片
        :param tempInfo: 模板图片信息对象
        :return: 指针仪表读数结果
        """
        img_result = 0.0
        img_s = cv2.imread(testPicPath)  # 读取测试图片
        print(f"测试图片：{testPicPath}")
        print(f"模板图片：{templatePicPath}")
        template1 = cv2.imread(templatePicPath)  # 读取测试图片对应的模板图片
        template2 = cv2.imread(templatePicPath)  # 读取测试图片对应的模板图片

        c_x = float(tempInfo.c_x)
        c_y = float(tempInfo.c_y)
        # eval这个函数会把里面的字符串参数的引号去掉，把中间的内容当成Python的代码，eval函数会执行这段代码并且返回执行结果
        # a = eval(tempInfo.a)  # #刻度坐标点
        a = tempInfo.value  # #刻度坐标点
        maxd = float(tempInfo.maxd)  # 最大刻度
        fir_d = float(tempInfo.fir_d)  # 骤然变化最小点
        sec_d = float(tempInfo.sec_d)  # 骤然变化最大点
        scale = float(tempInfo.scale)  # 一格刻度

        img = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)  # 测试图片 转灰度
        template1 = cv2.cvtColor(template1, cv2.COLOR_BGR2GRAY)  # 模板图片转灰度
        # 匹配并返回矩形坐标
        top_left, bottom_right = get_match_rect(template1, img, method)  # 模板匹配 获取测试图片上仪表的左上角和右下角坐标
        c_x0, c_y0 = get_center_point(top_left, bottom_right)  # 计算测试图片中指针仪表的中心点

        # 绘制矩形
        cv2.rectangle(img_s, top_left, bottom_right, 255, 2)
        # cv2.imencode(".png", img_s)[1].tofile(r"E:\Tonsen\testtttttttt.png")
        # cv2.imshow('img', cv2.resize(img_s, (int(img.shape[1] * 0.5), int(img.shape[0] * 0.5))))
        # cv2.waitKey(10)
        # cv2.destroyAllWindows()
        #################################################################
        new = img_s[top_left[1]:bottom_right[1] + 1, top_left[0]:bottom_right[0] + 1]  # 这句话没弄懂在干嘛
        # template2 = cv2.imread('temp3-2.jpg')
        top_left, bottom_right = get_match_rect(template2, new, method=method)  # 模板匹配 获取测试图片上仪表的左上角和右下角坐标
        new_ = new[top_left[1]:bottom_right[1] + 1, top_left[0]:bottom_right[0] + 1]
        # 二值化图像
        # cv2.imshow('二值化图像', new_)
        img = v2_by_k_means(new_)
        rad = get_pointer_rad(img, c_x0, c_y0)  # 获取角度
        # rad = get_pointer_rad_2(img, c_x0, c_y0)
        # cv2.waitKey(0)
        #################################################################

        # print('对应刻度', get_rad_val(rad[1], c_x, c_y, a, zc, maxd, fir_d, sec_d, scale))
        img_result = get_rad_val(rad[1], c_x, c_y, a, maxd, fir_d, sec_d, scale)
        print('对应刻度', img_result)  # 对应刻度 0.11503240573944025
        print('\n**************************************************')
        return img_result
