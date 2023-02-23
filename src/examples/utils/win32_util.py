# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/16 16:41
@File : win32_util.py
@Desc : win api util
"""
import time
from ctypes import windll, c_ubyte, byref
from ctypes.wintypes import HWND, RECT

import cv2
import numpy
import numpy as np
import win32con
import win32gui

GetDC = windll.user32.GetDC
CreateCompatibleDC = windll.gdi32.CreateCompatibleDC
GetClientRect = windll.user32.GetClientRect
CreateCompatibleBitmap = windll.gdi32.CreateCompatibleBitmap
SelectObject = windll.gdi32.SelectObject
BitBlt = windll.gdi32.BitBlt
SRCCOPY = 0x00CC0020
GetBitmapBits = windll.gdi32.GetBitmapBits
DeleteObject = windll.gdi32.DeleteObject
ReleaseDC = windll.user32.ReleaseDC

# 排除缩放干扰
windll.user32.SetProcessDPIAware()


class Win32Util:

    @staticmethod
    def getWindowList():
        """
        获取窗口列表
        :return: 窗口列表 (hwnd, windows title)
        如：(65800, '')
            (6490684, 'pylearning – pc_capture.py')
        """
        titles = []

        def foreach_window(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                titles.append((hwnd, title))
            return True

        win32gui.EnumWindows(foreach_window, 0)

        return titles

    @staticmethod
    def getWindowTitleList():
        """
        获取窗口标题列表
        :return: 窗口标题列表 ["name1", "name2", ...]
        """
        titles = []

        def foreach_window(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                titles.append(title)
            return True

        win32gui.EnumWindows(foreach_window, 0)

        return titles

    @staticmethod
    def windowExists(name):
        """
        判断窗口标题名称为name的程序是否存在
        :return: bool
        """
        titles = []

        def foreach_window(hwnd, lParam):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title == name:
                    titles.append((hwnd, title))
            return True

        win32gui.EnumWindows(foreach_window, 0)
        if len(titles) > 0:
            return True
        else:
            return False

    @staticmethod
    def capture(handle: HWND):
        """
        窗口客户区截图
        Args:
            handle (HWND): 要截图的窗口句柄
        Returns:
            numpy.ndarray: 截图数据（opencv格式）
        """
        # 获取窗口客户区的大小
        r = RECT()
        GetClientRect(handle, byref(r))
        # rect = win32gui.GetWindowRect(handle)
        # logger.info(f"width={rect[2] - rect[0]}, height={rect[3] - rect[1]}")
        width, height = r.right, r.bottom
        # logger.info(f"窗口客户区width={width}, 窗口客户区height={height}")
        # 开始截图
        dc = GetDC(handle)
        cdc = CreateCompatibleDC(dc)
        bitmap = CreateCompatibleBitmap(dc, width, height)
        SelectObject(cdc, bitmap)
        BitBlt(cdc, 0, 0, width, height, dc, 0, 0, SRCCOPY)
        # 截图是BGRA排列，因此总元素个数需要乘以4
        total_bytes = width * height * 4
        buffer = bytearray(total_bytes)
        byte_array = c_ubyte * total_bytes
        GetBitmapBits(bitmap, total_bytes, byte_array.from_buffer(buffer))
        DeleteObject(bitmap)
        DeleteObject(cdc)
        ReleaseDC(handle, dc)
        # 返回截图数据为numpy.ndarray
        # frame = np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        # frame = np.frombuffer(buffer, dtype=np.uint8)
        # logger.info(f"frame.ndim={frame.ndim}")
        # cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)
        # return frame

    @staticmethod
    def captureByTitleName(name: str, showNormal=True):
        """
        通过应用窗口标题名称截图，如果有多个窗口标题名称相同，则返回多个截图
        :param name: 应用窗口标题名称
        :param showNormal: 是否使窗口显示到正常状态(最小化状态截不到图，显示到正常状态才可以)
        :return: 截图列表（可能有多个名称相同的应用窗口标题）
        """
        targetHwnd = []

        def foreach_window(hwnd, lParam):
            isIconic = False  # 是否最小化
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title == name:
                    targetHwnd.append(hwnd)
                    if win32gui.IsIconic(hwnd) and showNormal:  # 如果窗口是最小化
                        isIconic = True
                        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
            if isIconic:
                time.sleep(0.1)  # 延时，防止截到白屏
            return True

        win32gui.EnumWindows(foreach_window, 0)
        frames = []  # pics
        for perHwnd in targetHwnd:
            frame = Win32Util.capture(perHwnd)
            frames.append(frame)
            # screen = QApplication.primaryScreen()
            # img = screen.grabWindow(perHwnd).toImage()
            # frames.append(Win32Util.qImage2CvImg(img))
            # frames.append(img)
        # if len(targetHwnd) > 0:
        #     screen = QApplication.primaryScreen()
        #     img = screen.grabWindow(targetHwnd[0]).toImage()
        #     f = Win32Util.qImage2CvImg(img)
        #     # img.save(f"test_{time.time()}_0.png")
        #     # cv2.imencode(".png", frames[0])[1].tofile(f"test_{time.time()}.png")
        #     strImg = Win32Util.cvImg2Base64(f)
        #     frames.append(Win32Util.base64ToCvImg(strImg))
        return frames  # 返回的是列表，可以判断列表大小来判断是否截到图片


if __name__ == "__main__":
    """
    如果先将frame保存到列表，最后再计算帧率，然后遍历列表保持到视频，会出现内存错误，所以改为读一帧写一帧。
    """
    fps = 60  # 视频帧率
    size = (1920, 720)  # 需要转为视频的图片的尺寸
    # video = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
    video = cv2.VideoWriter("output.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, size)

    win_list = Win32Util.getWindowList()
    for i, item in enumerate(win_list):  # 遍历窗口
        print(item)
    start_time = time.time()
    fpsCounter = 0
    fps30time = time.time()
    while time.time() - start_time < 15:
        images = Win32Util.captureByTitleName("Kanzi")
        if len(images) > 0:
            # 如果没有这句，图片尺寸与设置的分辨率不一样输出的视频为0k
            # frame = cv2.resize(images[0], size, interpolation=cv2.INTER_CUBIC)  # 确保图片尺寸的情况下可以不用
            # ok,windows截图后的排列是BGRA，需要转BGR，否则视频合成失败视频文件为1k
            frame = cv2.cvtColor(images[0], cv2.COLOR_BGRA2BGR)
            # print(type(frame)) <class 'numpy.ndarray'>
            # fpsStr = str(fpsCounter).zfill(5)  # 数字5位数，不够则使用0填充，如00001，00002
            # cv2.imwrite(f"imgs/fpsCounter{fpsStr}.png", frame)
            video.write(frame)
            fpsCounter += 1
            del images[0]
            del frame
    video.release()
    cv2.destroyAllWindows()
    print(f"cost_time = {time.time() - start_time}, fps={fpsCounter/15}")

