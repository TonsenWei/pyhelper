# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/6 11:51
@File : download_image.py
@Desc : 
"""
import os
import numpy as np

import cv2
import requests


class DownloadImage:

    @staticmethod
    def data_to_cv2(img_data):
        """将图片二进制流转为CV2格式"""
        buf = np.asarray(bytearray(img_data), dtype="uint8")
        return cv2.imdecode(buf, cv2.IMREAD_COLOR)

    @staticmethod
    def getImageFromWebDemo():
        # 确认数据链接状态
        url = "https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

        # stream=True 获取到的类似生成器 stream=False 获取到的类似列表,一般是用来读取大量数据的,使用列表内存可能不足
        # 下载视频，或者图片时通常会使用这个选项，读取一张照片不需要这个选项

        # response = requests.get(url, headers=header, stream=True)
        response = requests.get(url, headers=header)  # 图片是二进制数据，二进制数据没有编码

        # 字符串切割，找到图片类型
        img = url.split('/')[-1]
        print(f"img={img}")
        with open(img, "wb") as file:
            # 写入图片，视频、音乐时需要用字节流的形式写入
            file.write(response.content)
            frame = DownloadImage.data_to_cv2(response.content)
            cv2.namedWindow("image")  # 创建一个image的窗口
            cv2.imshow("image", frame)  # 显示图像
            cv2.waitKey()  # 默认为0，无限等待
            cv2.destroyAllWindows()  # 释放所有窗口

    @staticmethod
    def getImageFromAdbCurlDemo():
        """
        通过adb访问图片地址获取图片数据
        Returns:

        """
        file = os.popen("adb shell curl -s \"https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png""\"")

        rdata = file.buffer.read()  # 读取图片数据
        # 不进行替换内容会有问题： error: (-215:Assertion failed) size.width>0 && size.height>0 in function 'cv::imshow'
        data = rdata.replace(b"\r\n", b"\n")
        frame = DownloadImage.data_to_cv2(data)  # error: (-215:Assertion failed) !buf.empty() in function 'cv::imdecode_'
        # frame = WebCamUtil.data_to_cv2(rdata)
        cv2.namedWindow("image")  # 创建一个image的窗口
        # 显示图像，图片内容有问题时： error: (-215:Assertion failed) size.width>0 && size.height>0 in function 'cv::imshow'
        cv2.imshow("image", frame)
        cv2.waitKey()  # 默认为0，无限等待
        cv2.destroyAllWindows()  # 释放所有窗口


if __name__ == "__main__":
    # DownloadImage.getImageFromWebDemo()
    DownloadImage.getImageFromAdbCurlDemo()
