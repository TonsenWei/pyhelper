# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/7 18:04
@File : meter_detect_util.py
@Desc : 
"""
import base64
import math

import cv2
import numpy as np
from math import cos, pi, sin

from PySide2.QtCore import QSettings

from src.myutils.airtest.core.cv import Template, TemplateCv2


class ImgUtil:

    @staticmethod
    def cvImg2Base64(frame, fmt=".png"):
        """
        opencv图片转base64字符串
        :param frame: opencv图片
        :param fmt: 图片原格式
        :return: base64图片字符串
        """
        image = cv2.imencode(fmt, frame)[1]
        image_code = str(base64.b64encode(image))[2:-1]
        return image_code

    @staticmethod
    def base64ToCvImg(base64_code):
        """
        base64图片字符串转opencv图片
        :param base64_code: base64编码
        :return: opencv图片
        """
        # base64解码
        img_data = base64.b64decode(base64_code)
        # 转换为np数组
        # img_array = np.fromstring(img_data, np.uint8)  # is deprecated
        img_array = np.frombuffer(img_data, np.uint8)
        # 转换成opencv可用格式
        img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
        return img

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
        # 转换成灰度图
        height, width = image.shape[:2]  # 测试图片高度和宽度
        # image = cv2.resize(image, (500, 500), interpolation=cv2.INTER_CUBIC)
        scale = 1
        centerX = center[0]
        centerY = center[1]
        widthMax = 600
        if width > widthMax:  # 宽度大于400的图片，进行缩放
            scale = widthMax/width
            print(f"scale = {scale}")
            height = (height*widthMax)/width
            width = width*scale
            image = cv2.resize(image, (widthMax, int(height)), interpolation=cv2.INTER_CUBIC)
            centerX = center[0]*scale
            centerY = center[1]*scale
        cX = centerX
        cY = centerY
        xLeft = width - cX  # 指针旋转点 到 右边的距离
        yLeft = height - cY  # 指针旋转点 到 底部的距离
        minValue = min([cX, cY, xLeft, yLeft])
        rValue = minValue * 0.6  # 指针旋转半径
        print(f"minValue = {minValue}")
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
        maxLineGap:线段上最近两点之间的阈值 线段之间的最大允许间隙，将它们视为一条线
        """
        # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
        # lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=int(width/8), maxLineGap=10)
        # print(int(width/2))
        # 这个系数适用大多数情况，不适用的可以使用 threshold=100，minLineLength=100， maxLineGap=10测试
        threshold = int(width / 8)  # 8  #
        minLineLength = int(width / 8)  # 8
        maxLineGap = int(width / 80)  # 80 待处理宽度小于80时，线段之间的最大允许间隙，将它们视为一条线
        # threshold = 100  # 测试用
        # minLineLength = 100
        # maxLineGap = 10
        print(f"threshold={threshold}, minLineLength={minLineLength}, maxLineGap={maxLineGap}")
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)
        # 遍历
        targetPoint = [0, 0]
        if lines is not None:
            lineInPointer = []
            for lIndex, line in enumerate(lines):
                line1x1, line1y1, line1x2, line1y2 = line[0]
                # 判断线段两个点到指针中心的距离，要至少有一个点在该距离内，否则判断为不是指针的线
                disP1 = math.sqrt(pow(centerX - line1x1, 2) + pow(centerY - line1y1, 2))
                disP2 = math.sqrt(pow(centerX - line1x2, 2) + pow(centerY - line1y2, 2))
                minDistance = minValue*0.4
                if disP1 <= minDistance or disP2 <= minDistance:
                    lineInPointer.append(line)
            lines = lineInPointer
            cv2.imshow("edges", edges)
            print(f"lines len = {len(lines)}")
            if len(lines) >= 2:  # 找到的线大于等于两条
                lineRet = []
                for lIndex, line in enumerate(lines):
                    line1x1, line1y1, line1x2, line1y2 = line[0]
                    lDis = math.sqrt(pow(line1x2 - line1x1, 2) + pow(line1y2 - line1y1, 2))  # 计算线段长度
                    lineRet.append([lIndex, lDis, line])
                lineRet.sort(key=lambda x: x[1], reverse=True)  # 按线段长度排序
                # lines = [lineRet[0][2], lineRet[1][2]]
                line1x1, line1y1, line1x2, line1y2 = lineRet[0][2][0]
                line2x1, line2y1, line2x2, line2y2 = lineRet[1][2][0]
                line1 = [line1x1, line1y1, line1x2, line1y2]
                line2 = [line2x1, line2y1, line2x2, line2y2]
                targetPoint = MeterUtil.cross_point(line1, line2)  # 计算延长线交点
                print(f"targetPoint line > = 2: {targetPoint}")
                if targetPoint is not None:
                    centerToTarDis = math.sqrt(pow(centerX - targetPoint[0], 2) + pow(centerY - targetPoint[1], 2))
                    print(f"centerToTarDis={centerToTarDis}")
                    if targetPoint[0] < 0 or targetPoint[1] < 0 or centerToTarDis > (minValue*0.8):  # 交点为负值或太远
                        centerToTarScale = rValue / centerToTarDis
                        if targetPoint[0] > centerX and targetPoint[1] < centerY:  # 第一象限
                            xOffset = ((targetPoint[0] - centerX) * centerToTarScale)
                            yOffset = ((centerY - targetPoint[1]) * centerToTarScale)
                            targetPoint[0] = centerX + xOffset
                            targetPoint[1] = targetPoint[1] + (centerY - targetPoint[1] - yOffset)
                            print(f"第一象限：（{targetPoint[0]}， {targetPoint[1]}）")
                        elif targetPoint[0] < centerX and targetPoint[1] < centerY:  # 第二象限
                            xOffset = ((centerX - targetPoint[0]) * centerToTarScale)
                            yOffset = ((centerY - targetPoint[1]) * centerToTarScale)
                            targetPoint[0] = targetPoint[0] + (centerX - targetPoint[0] - xOffset)
                            targetPoint[1] = targetPoint[1] + (centerY - targetPoint[1] - yOffset)
                            print(f"第二象限：（{targetPoint[0]}， {targetPoint[1]}）")
                        elif targetPoint[0] < centerX and targetPoint[1] > centerY:  # 第三象限
                            xOffset = ((centerX - targetPoint[0]) * centerToTarScale)
                            yOffset = ((targetPoint[1] - centerY) * centerToTarScale)
                            targetPoint[0] = centerX - xOffset
                            targetPoint[1] = centerY + yOffset
                            print(f"第三象限：（{targetPoint[0]}， {targetPoint[1]}）")
                        elif targetPoint[0] > centerX and targetPoint[1] > center[1]:  # 第四象限
                            xOffset = ((targetPoint[0] - centerX) * centerToTarScale)
                            yOffset = ((targetPoint[1] - centerY) * centerToTarScale)
                            targetPoint[0] = centerX + xOffset
                            targetPoint[1] = centerY + yOffset
                            print(f"第四象限：（{targetPoint[0]}， {targetPoint[1]}）")
                        else:
                            print("无象限")
                    else:
                        print(f"centerToTarDis={centerToTarDis}, minValue*0.8={minValue*0.8}")
                else:
                    line1x1, line1y1, line1x2, line1y2 = lines[0][0]
                    disP1 = math.sqrt(pow(centerX - line1x1, 2) + pow(centerY - line1y1, 2))
                    disP2 = math.sqrt(pow(centerX - line1x2, 2) + pow(centerY - line1y2, 2))
                    if disP1 >= disP2:
                        targetPoint = [line1x1, line1y1]
                    else:
                        targetPoint = [line1x2, line1y2]
                    print(f"targetPoint is none get again: {targetPoint}")
            elif len(lines) == 1:
                line1x1, line1y1, line1x2, line1y2 = lines[0][0]
                disP1 = math.sqrt(pow(centerX - line1x1, 2) + pow(centerY - line1y1, 2))
                disP2 = math.sqrt(pow(centerX - line1x2, 2) + pow(centerY - line1y2, 2))
                if disP1 >= disP2:
                    targetPoint = [line1x1, line1y1]
                else:
                    targetPoint = [line1x2, line1y2]
            for i, line in enumerate(lines):
                # 获取坐标
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), thickness=3)
                cv2.putText(image, str(i), (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        if len(targetPoint) == 2:
            cv2.circle(image, (int(targetPoint[0]), int(targetPoint[1])), 3, (0, 255, 0), -1)
        # cv2.imshow("lines", image)
        # cv2.waitKey(0)
        print(f"targetPoint={targetPoint}")
        return [int(targetPoint[0]), int(targetPoint[1])], image, scale

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
        print(f"targetValue = {targetValue}")
        return targetValue

    @staticmethod
    def readValueFormFrame(frame, centerPos, zeroPos, maxPox, meterMaxValue):
        imageTmp = frame.copy()
        poiPoint, posImg, scale = MeterUtil.get_point_pos(imageTmp, centerPos)  # 获取指针指尖点
        centerX = centerPos[0]*scale
        centerY = centerPos[1]*scale
        newCenter = (centerX, centerY)
        zeroX = zeroPos[0]*scale
        zeroY = zeroPos[1]*scale
        newZero = (zeroX, zeroY)
        maxX = maxPox[0]*scale
        maxY = maxPox[1]*scale
        newMax = (maxX, maxY)
        cv2.circle(posImg, (int(centerX), int(centerY)), 3, (127, 255, 255), -1)
        cv2.circle(posImg, (int(zeroX), int(zeroY)), 3, (255, 0, 0), -1)
        cv2.circle(posImg, (int(maxX), int(maxY)), 3, (255, 255, 85), -1)
        return MeterUtil.get_meter_value(newCenter, newZero, newMax, poiPoint, meterMaxValue), posImg

    @staticmethod
    def demo001():
        # 读数测试
        imagePath = r"D:\projects\python\pylearning\files\pics\meter\ico_50c.png"  # 50
        image = cv2.imread(imagePath)
        center = [303, 307]  # 指针旋转中心点
        pointZero = [95, 425]  # 0值指针坐标
        pointMax = [506, 425]  # 最大值指针坐标
        maxValue = 100  # 刻度值最大值
        MeterUtil.readValueFormFrame(image, center, pointZero, pointMax, maxValue)

    @staticmethod
    def demo002():
        # 读数测试
        imagePath = r"D:\projects\python\pylearning\files\pics\meter\ico_38c_tmp.png"  # 50
        # imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\ico_75c_scale.png"  # 50
        imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\ico_75c_test.png"  # 50
        tmp = Template(imagePath)
        png_frame = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('OriPic', png_frame)
        match_ret = tmp.match_in_result(png_frame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = png_frame.copy()
            cv2.rectangle(png_frame,
                          (startX, startY),  # 左上角坐标
                          (endX, endY),  # 右下角坐标
                          (0, 255, 0),  # 线颜色
                          2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height={height}")

            image = cv2.imread(imagePath)
            tmpHeight, tmpWidht = image.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height={tmpHeight}")
            # 模板图片信息：
            center = [298, 298]  # 指针旋转中心点
            pointZero = [92, 415]  # 0值指针坐标
            pointMax = [503, 414]  # 最大值指针坐标
            maxValue = 100  # 刻度值最大值

            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * center[0]), int(scale * center[1])]
            testZeroPos = [int(scale * pointZero[0]), int(scale * pointZero[1])]
            testMaxPos = [int(scale * pointMax[0]), int(scale * pointMax[1])]
            # xCenter = (width * center[0]) / tmpWidht
            # yCenter = (height * center[1]) / tmpHeight
            # testCenter = [xCenter, yCenter]
            # xZero = (width * center[0]) / tmpWidht
            # yZero = (width * center[0]) / tmpWidht
            value, posImg = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            cv2.imshow("posImg", posImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    @staticmethod
    def demo003():
        # 读数测试
        imagePath = r"D:\projects\python\pylearning\files\pics\meter\002_tmp_ori.png"  # 50
        # imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\ico_75c_scale.png"  # 50
        imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\002_tmp_ori.png"  # 50
        tmp = Template(imagePath)
        png_frame = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('OriPic', png_frame)
        match_ret = tmp.match_in_result(png_frame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = png_frame.copy()
            cv2.rectangle(png_frame,
                          (startX, startY),  # 左上角坐标
                          (endX, endY),  # 右下角坐标
                          (0, 255, 0),  # 线颜色
                          2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height{height}")

            image = cv2.imread(imagePath)
            tmpHeight, tmpWidht = image.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height{tmpHeight}")
            # 模板图片信息：
            center = [410, 408]  # 指针旋转中心点
            pointZero = [206, 576]  # 0值指针坐标
            pointMax = [580, 596]  # 最大值指针坐标
            maxValue = 160  # 刻度值最大值

            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * center[0]), int(scale * center[1])]
            testZeroPos = [int(scale * pointZero[0]), int(scale * pointZero[1])]
            testMaxPos = [int(scale * pointMax[0]), int(scale * pointMax[1])]
            # xCenter = (width * center[0]) / tmpWidht
            # yCenter = (height * center[1]) / tmpHeight
            # testCenter = [xCenter, yCenter]
            # xZero = (width * center[0]) / tmpWidht
            # yZero = (width * center[0]) / tmpWidht
            value, posImg = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            cv2.imshow("posImg", posImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    @staticmethod
    def demo004():
        # 读数测试
        imagePath = r"D:\projects\python\pylearning\files\pics\meter\003_press_meter_tmp_small.png"  # 50
        # imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\003_press_meter1.jpg"  # 50
        imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\003_press_meter2.jpg"  # 50
        # imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\003_press_meter_tmp_small.png"  # 50
        tmp = Template(imagePath)
        png_frame = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('OriPic', png_frame)
        match_ret = tmp.match_in_result(png_frame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = png_frame.copy()
            cv2.rectangle(png_frame,
                          (startX, startY),  # 左上角坐标
                          (endX, endY),  # 右下角坐标
                          (0, 255, 0),  # 线颜色
                          2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height{height}")

            image = cv2.imread(imagePath)
            tmpHeight, tmpWidht = image.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height{tmpHeight}")
            # 模板图片信息：
            center = [95, 93]  # 指针旋转中心点
            pointZero = [34, 134]  # 0值指针坐标
            pointMax = [150, 157]  # 最大值指针坐标
            maxValue = 0.6  # 刻度值最大值

            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * center[0]), int(scale * center[1])]
            testZeroPos = [int(scale * pointZero[0]), int(scale * pointZero[1])]
            testMaxPos = [int(scale * pointMax[0]), int(scale * pointMax[1])]
            # xCenter = (width * center[0]) / tmpWidht
            # yCenter = (height * center[1]) / tmpHeight
            # testCenter = [xCenter, yCenter]
            # xZero = (width * center[0]) / tmpWidht
            # yZero = (width * center[0]) / tmpWidht
            value, posImg = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            cv2.imshow("posImg", posImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("not match")

    @staticmethod
    def demo005():
        # 读数测试
        imagePath = r"D:\projects\python\pylearning\files\pics\meter\speed_meter_temp.png"  # 50
        imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\speed_meter_real.jpg"  # 50
        tmp = Template(imagePath)
        png_frame = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('OriPic', png_frame)
        match_ret = tmp.match_in_result(png_frame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = png_frame.copy()
            cv2.rectangle(png_frame,
                          (startX, startY),  # 左上角坐标
                          (endX, endY),  # 右下角坐标
                          (0, 255, 0),  # 线颜色
                          2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height{height}")

            image = cv2.imread(imagePath)
            tmpHeight, tmpWidht = image.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height{tmpHeight}")
            # 模板图片信息：
            center = [170, 164]  # 指针旋转中心点
            pointZero = [68, 243]  # 0值指针坐标
            pointMax = [269, 251]  # 最大值指针坐标
            maxValue = 260  # 刻度值最大值

            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * center[0]), int(scale * center[1])]
            testZeroPos = [int(scale * pointZero[0]), int(scale * pointZero[1])]
            testMaxPos = [int(scale * pointMax[0]), int(scale * pointMax[1])]
            # xCenter = (width * center[0]) / tmpWidht
            # yCenter = (height * center[1]) / tmpHeight
            # testCenter = [xCenter, yCenter]
            # xZero = (width * center[0]) / tmpWidht
            # yZero = (width * center[0]) / tmpWidht
            value, posImg = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            cv2.imshow("posImg", posImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("not match")

    @staticmethod
    def demo006_001_meter():
        # 读数测试
        imagePath = r"D:\projects\python\pylearning\files\pics\meter\001_meter.png"  # 50
        imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\001_meter.png"  # 50
        tmp = Template(imagePath)
        png_frame = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        cv2.imshow('OriPic', png_frame)
        match_ret = tmp.match_in_result(png_frame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = png_frame.copy()
            cv2.rectangle(png_frame,
                          (startX, startY),  # 左上角坐标
                          (endX, endY),  # 右下角坐标
                          (0, 255, 0),  # 线颜色
                          2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height{height}")

            image = cv2.imread(imagePath)
            tmpHeight, tmpWidht = image.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height{tmpHeight}")
            # 模板图片信息：
            center = [297, 280]  # 指针旋转中心点
            pointZero = [122, 386]  # 0值指针坐标
            pointMax = [478, 386]  # 最大值指针坐标
            maxValue = 260  # 刻度值最大值

            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * center[0]), int(scale * center[1])]
            testZeroPos = [int(scale * pointZero[0]), int(scale * pointZero[1])]
            testMaxPos = [int(scale * pointMax[0]), int(scale * pointMax[1])]
            # xCenter = (width * center[0]) / tmpWidht
            # yCenter = (height * center[1]) / tmpHeight
            # testCenter = [xCenter, yCenter]
            # xZero = (width * center[0]) / tmpWidht
            # yZero = (width * center[0]) / tmpWidht
            value, posImg = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            cv2.imshow("posImg", posImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("not match")

    @staticmethod
    def demo_013_meter():
        # 读数测试
        tmpPath = r"D:\projects\python\pylearning\files\pics\meter\013_meter.png"  # 50
        imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\013_meter.png"  # 50
        testMeterframe = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        # 模板图片信息：
        center = (230, 255)  # 指针旋转中心点
        pointZero = (102, 372)  # 0值指针坐标
        pointMax = (353, 388)  # 最大值指针坐标
        maxValue = 60000  # 刻度值最大值
        meterValue, retImg = MeterUtil.readMeter(testMeterframe, tmpPath, center, pointZero, pointMax, maxValue)
        if meterValue is not None:
            print(f"meter read value is: {meterValue}")
            cv2.imshow("ResultImage", retImg)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("error, read meter failed!")

    @staticmethod
    def readMeter(testFrame, tmpMeterPicPath, centerPoint, zeroPoint, maxPoint, maxValue):
        """
        仪表读数
        :param testFrame: 待读取的仪表图片
        :param tmpMeterPicPath: 模板图片路径
        :param centerPoint: 指针旋转中心点
        :param zeroPoint: 0值刻度坐标
        :param maxPoint: 最大值刻度坐标
        :param maxValue: 数值最大值
        :return: value：读数结果
                image ： 读数过程分析结果图片
        """
        value, image = None, None
        tmp = Template(tmpMeterPicPath)
        match_ret = tmp.match_in_result(testFrame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = testFrame.copy()
            cv2.rectangle(testFrame,
                          (startX, startY),  # 左上角坐标
                          (endX, endY),  # 右下角坐标
                          (0, 255, 0),  # 线颜色
                          2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            # cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height{height}")

            image = cv2.imdecode(np.fromfile(tmpMeterPicPath, dtype=np.uint8), cv2.IMREAD_COLOR)
            tmpHeight, tmpWidht = image.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height{tmpHeight}")
            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * centerPoint[0]), int(scale * centerPoint[1])]
            testZeroPos = [int(scale * zeroPoint[0]), int(scale * zeroPoint[1])]
            testMaxPos = [int(scale * maxPoint[0]), int(scale * maxPoint[1])]
            value, image = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            return value, image
        else:
            print("not match")
            return value, image

    @staticmethod
    def readMeterFrame(testFrame, tmpMeterPicFrame, centerPoint, zeroPoint, maxPoint, maxValue):
        """
        仪表读数
        :param testFrame: 待读取的仪表图片
        :param tmpMeterPicFrame: 模板图片路径
        :param centerPoint: 指针旋转中心点
        :param zeroPoint: 0值刻度坐标
        :param maxPoint: 最大值刻度坐标
        :param maxValue: 数值最大值
        :return: value：读数结果
                image ： 读数过程分析结果图片
        """
        value, image = None, None
        tmp = TemplateCv2(tmpMeterPicFrame)
        match_ret = tmp.match_in_result(testFrame)
        if match_ret is not None:
            startX = match_ret["rectangle"][0][0]
            startY = match_ret["rectangle"][0][1]
            endX = match_ret["rectangle"][2][0]
            endY = match_ret["rectangle"][2][1]
            copyTestFram = testFrame.copy()
            # cv2.rectangle(testFrame,
            #               (startX, startY),  # 左上角坐标
            #               (endX, endY),  # 右下角坐标
            #               (0, 255, 0),  # 线颜色
            #               2)  # 线粗细
            print(match_ret)
            testFrame = copyTestFram[startY:endY, startX:endX]
            # cv2.imshow('testFrame', testFrame)
            height, width = testFrame.shape[:2]  # 测试图片高度和宽度
            print(f"测试图片width={width}, height{height}")

            tmpHeight, tmpWidht = tmpMeterPicFrame.shape[:2]  # 模板图片高度和宽度
            print(f"模板图片width={tmpWidht}, height{tmpHeight}")
            # 测试图片信息
            scale = height / tmpHeight
            testCenter = [int(scale * centerPoint[0]), int(scale * centerPoint[1])]
            testZeroPos = [int(scale * zeroPoint[0]), int(scale * zeroPoint[1])]
            testMaxPos = [int(scale * maxPoint[0]), int(scale * maxPoint[1])]
            value, image = MeterUtil.readValueFormFrame(testFrame, testCenter, testZeroPos, testMaxPos, maxValue)
            return value, image
        else:
            print("not match")
            return value, image

    @staticmethod
    def generateTemplate(tempPicPath, center, pointZero, pointMax, maxValue):
        cvFrame = cv2.imdecode(np.fromfile(tempPicPath, dtype=np.uint8), cv2.IMREAD_COLOR)
        templatePath = "qt_meter_temp.ini"
        METER_TEMPLATE = QSettings(templatePath, QSettings.IniFormat)  # 校准设置,如果替换ini文件，需要重新赋值一次才会更新
        tempPic = "MeterTemplate/temp_pic"
        tempCenterPos = "MeterTemplate/temp_center"
        tempZeroPos = "MeterTemplate/temp_zero"
        tempMaxPos = "MeterTemplate/temp_max_pox"
        tempMaxValue = "MeterTemplate/temp_max_value"

        METER_TEMPLATE.setValue(tempPic, ImgUtil.cvImg2Base64(cvFrame))  # 图片
        METER_TEMPLATE.setValue(tempCenterPos, center)  # 中心点
        METER_TEMPLATE.setValue(tempZeroPos, pointZero)  # 缩放比例
        METER_TEMPLATE.setValue(tempMaxPos, pointMax)  # 画框时的宽度
        METER_TEMPLATE.setValue(tempMaxValue, maxValue)  # 画框时的宽度

    @staticmethod
    def getTemplate():
        templatePath = "meter_qt.ini"
        METER_TEMPLATE = QSettings(templatePath, QSettings.IniFormat)  # 校准设置,如果替换ini文件，需要重新赋值一次才会更新
        tempPic = "MeterTemplate/temp_pic"
        tempCenterPos = "MeterTemplate/temp_center"
        tempZeroPos = "MeterTemplate/temp_zero"
        tempMaxPos = "MeterTemplate/temp_max_pox"
        tempMaxValue = "MeterTemplate/temp_max_value"

        tempPicBase64 = str(METER_TEMPLATE.value(tempPic))  # 图片
        tempFrame = ImgUtil.base64ToCvImg(tempPicBase64)
        getCenter = METER_TEMPLATE.value(tempCenterPos, None)  # 中心点
        getZero = METER_TEMPLATE.value(tempZeroPos, None)  # 缩放比例
        getMaxPos = METER_TEMPLATE.value(tempMaxPos, None)  # 画框时的宽度
        getMaxValue = float(METER_TEMPLATE.value(tempMaxValue, None))  # 画框时的宽度
        print(type(getCenter))
        print(type(getZero))
        print(type(getMaxPos))
        print(type(getMaxValue))
        return tempFrame, getCenter, getZero, getMaxPos, getMaxValue
        # cv2.imshow("ResultImage", tempFrame)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    # MeterUtil.demo002()  # ico_38c_tmp  两种都OK
    # MeterUtil.demo003()  # 识别了多个直线，待增加判断有多少条线经过圆心范围，然后求两条直线交点 002_tmp_ori， 两种都可以
    # MeterUtil.demo004()  # 直线交点为负数，找不到目标指针 003_press_meter  计算ok
    # MeterUtil.demo005()  # speed_meter_temp.png  两种都可以
    # MeterUtil.demo006_001_meter()  # 001_meter.png 两种都可以
    # MeterUtil.demo_013_meter()

    # 生成模板测试
    tempPath = r"D:\projects\python\pylearning\files\pics\meter\qt_meter_temp.png"  # 50
    center = (509, 502)  # 指针旋转中心点
    pointZero = (179, 697)  # 0值指针坐标
    pointMax = (841, 691)  # 最大值指针坐标
    maxValue = 100  # 刻度值最大值
    MeterUtil.generateTemplate(tempPath, center, pointZero, pointMax, maxValue)

    # 读取模板测试
    # imageTestPath = r"D:\projects\python\pylearning\files\pics\meter\003_press_meter_tmp_small.png"  # 50
    # testMeterframe = cv2.imdecode(np.fromfile(imageTestPath, dtype=np.uint8), cv2.IMREAD_COLOR)
    # tempFrame, getCenter, getZero, getMaxPos, getMaxValue = MeterUtil.getTemplate()
    # meterValue, retImg = MeterUtil.readMeterFrame(testMeterframe, tempFrame, getCenter, getZero, getMaxPos, getMaxValue)
    # if meterValue is not None:
    #     print(f"meter read value is: {meterValue}")
    #     cv2.imshow("ResultImage", retImg)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()
    # else:
    #     print("error, read meter failed!")


