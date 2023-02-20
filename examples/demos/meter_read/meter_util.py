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
# from fuzzywuzzy import fuzz

'''
图片匹配算法
'''
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
method = cv2.TM_CCOEFF


class TemplateBean:

    def __init__(self):
        self.id = "1"
        self.name = "template.jpg"
        self.img_template = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\TemplateLib\template.jpg"
        self.a = "{0.0:(61.5,152.5),0.1:(50.5,109.5),0.2:(61.5,152.5),0.3:(126.0,46.0),0.4:(169.0,70.0),0.5:(188.5,122.0),0.6:(164.0,168.5)}"
        self.c_x = "120.00"
        self.c_y = "114.50"
        self.fir_d = "0.50"
        self.maxd = "0.60"
        self.scale = "0.10"
        self.sec_d = "0.60"


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
                pass
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
        print(f"角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y})")
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


'''无用方法，不能使用模板匹配得到的中心坐标'''


def get_pointer_rad_2(img, c_x, c_y):
    """获取角度"""
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
    center = [c_x, c_y]  # 中心点
    count = 0
    result = {}

    # *************确定zc值**************
    zc_list = {}
    for i in range(1, 10):
        zc_list[i] = dict()

    # *************确定zc值**************
    for k, v in a.items():  # 从每个刻度值及其坐标获取
        # k=0.0, v=(85.0, 233.0)
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
    def cross_point(line1, line2):
        """
        计算两条直线的交点
        :param line1: 第一条直线
        :param line2: 第二条直线
        :return: list : 交点 [x, y]
        """
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

    @staticmethod
    def get_point_pos(image, center):
        """
        霍夫曼直线检测找出直线
        :param imagePath: 图片路径,在该图片上查找指针指尖的点
        :param center: 指针旋转中心
        :return: 指针指尖的点
        """
        # 读取图片
        # image = cv2.imread(imagePath)
        # image_copy = image.copy()

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
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)

        # 遍历
        targetPoint = []
        if lines is not None:
            if len(lines) >= 2:  # 找到的线大于等于两条
                line1x1, line1y1, line1x2, line1y2 = lines[0][0]
                line2x1, line2y1, line2x2, line2y2 = lines[1][0]
                line1 = [line1x1, line1y1, line1x2, line1y2]
                line2 = [line2x1, line2y1, line2x2, line2y2]
                targetPoint = MeterUtil.cross_point(line1, line2)
            elif len(lines) == 1:
                line1x1, line1y1, line1x2, line1y2 = lines[0][0]
                disP1 = math.sqrt(pow(center[0] - line1x1, 2) + pow(center[1] - line1y1, 2))
                disP2 = math.sqrt(pow(center[0] - line1x2, 2) + pow(center[1] - line1y2, 2))
                if disP1 >= disP2:
                    targetPoint = [line1x1, line1y1]
                else:
                    targetPoint = [line1x2, line1y2]
        # image_copy
        return [int(targetPoint[0]), int(targetPoint[1])]

    @staticmethod
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
        # 实际中心点
        c_y, c_x = center[1], center[0]
        degreeZeroValue = 0
        degreeMaxValue = 0
        degreeTargetValue = 0
        zeroFound = False
        targetFound = False
        maxFound = False
        x1 = c_x + c_x
        targetValue = 0

        for i in range(361):
            x = (x1 - c_x) * cos(i * pi / 180) + c_x
            y = (x1 - c_x) * sin(i * pi / 180) + c_y
            xThen = (x1 - c_x) * cos((i + 1) * pi / 180) + c_x
            yThen = (x1 - c_x) * sin((i + 1) * pi / 180) + c_y
            # temp = img.copy()
            # cv2.line(temp, (c_x, c_y), (int(x), int(y)), (0, 0, 255), thickness=3)  # 画线
            # 判断点在多边形上
            pts = np.array([[c_x, c_y], [x, y], [xThen, yThen], [c_x, c_y]], np.int32)  # 数据类型必须为 int32
            pts = pts.reshape((-1, 1, 2))
            # 设置为True时，返回实际距离值。若返回值为正，表示点在多边形内部，返回值为负，表示在多边形外部，返回值为0，表示在多边形上。
            # 设置为False,返回 -1、0、1三个固定值。若返回值为+1，表示点在多边形内部，返回值为-1，表示在多边形外部，返回值为0，表示在多边形上。
            retZero = cv2.pointPolygonTest(pts, (pointZero[0], pointZero[1]), False)
            retMax = cv2.pointPolygonTest(pts, (pointMax[0], pointMax[1]), False)
            retTarget = cv2.pointPolygonTest(pts, (pointTarget[0], pointTarget[1]), False)
            if retTarget >= 0:
                resTarget = True
            if retZero >= 0 and zeroFound is False:
                zeroFound = True
                degreeZeroValue = i
                print(f"0值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeZeroValue={degreeZeroValue}")
                print(f"0值坐标：{pointZero}")
                # cv2.drawContours(temp, [pts], -1, (0, 255, 0), -1)  # 画轮廓
                # cv2.imshow('drawContours', temp)
                # cv2.waitKey(0)
            if retMax >= 0 and maxFound is False:
                maxFound = True
                degreeMaxValue = i
                print(f"最大值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeMaxValue={degreeMaxValue}")
                print(f"最大值坐标：{pointMax}")
                # cv2.drawContours(temp, [pts], -1, (0, 255, 0), -1)  # 画轮廓
                # cv2.imshow('drawContours', temp)
                # cv2.waitKey(0)
            if retTarget >= 0 and targetFound is False:
                targetFound = True
                degreeTargetValue = i
                print(f"目标值的角度={i}, 圆心({c_x}, {c_y}), 线的点({x}, {y}), degreeTargetValue={degreeTargetValue}")
                print(f"目标值坐标：{pointTarget}")
                # cv2.drawContours(temp, [pts], -1, (0, 255, 0), -1)  # 画轮廓
                # cv2.imshow('drawContours', temp)
                # cv2.waitKey(0)
        # cv2.destroyAllWindows()
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
        elif degreeMaxValue < degreeTargetValue < degreeZeroValue:
            # 先找到最大值，再到目标值，再到0值，说明可能因为误差原因，目标在0值之前，直接置0
            targetValue = 0
        elif degreeTargetValue == degreeZeroValue:
            targetValue = 0
        elif degreeTargetValue == degreeTargetValue:
            targetValue = maxValue
        if targetValue > maxValue:
            targetValue = maxValue
        print(f"targetValue = {round(targetValue, 1)}")
        return targetValue

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
        # print(f"测试图片：{testPicPath}")
        # print(f"模板图片：{templatePicPath}")
        template1 = cv2.imread(templatePicPath)  # 读取测试图片对应的模板图片
        template2 = cv2.imread(templatePicPath)  # 读取测试图片对应的模板图片

        c_x = float(tempInfo.c_x)
        c_y = float(tempInfo.c_y)
        # eval这个函数会把里面的字符串参数的引号去掉，把中间的内容当成Python的代码，eval函数会执行这段代码并且返回执行结果
        a = eval(tempInfo.a)  # 各个刻度坐标点
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
        # print('对应刻度', img_result)  # 对应刻度 0.11503240573944025
        # print('\n**************************************************')
        return img_result


if __name__ == "__main__":
    # testPicPath = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\img_test_2\1.jpg"
    # testPicPath = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\img_test_2\8.jpg"
    # testPicPath = r"D:\tmp\scale1_5.png"
    # testPicPath = r"D:\tmp\v3_test.png"
    # testPicPath = r"D:\tmp\v3_rpm.png"
    # templatePicPath = r"D:\projects\gits\yibiao_rec\django_yibiao\yibiao_ocr\TemplateLib\template.jpg"
    # templatePicPath = r"D:\tmp\v3_rpm_meter.png"
    # tempInfo = TemplateBean()
    # resultValue = MeterUtil.img_rec_result(testPicPath, templatePicPath, tempInfo)
    # print(f"resultValue={resultValue}")  # resultValue=0.4534627915069202

    # 读数测试
    imagePath = r"D:\projects\python\pylearning\files\pics\meter\ico_50c.png"  # 50
    image = cv2.imread(imagePath)
    image_copy = image.copy()
    center = [303, 307]  # 指针旋转中心点
    pointZero = [95, 425]  # 0值指针坐标
    pointMax = [506, 425]  # 最大值指针坐标
    maxValue = 100  # 刻度值最大值
    targetPoint = MeterUtil.get_point_pos(image_copy, center)  # 获取指针指尖点
    MeterUtil.get_meter_value(center, pointZero, pointMax, targetPoint, maxValue)
