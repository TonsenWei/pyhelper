# -*- coding: utf-8 -*-
"""
Author: Wei Dongcheng
Date: 2022/9/5 7:50
LastEditTime: 2022/9/5 7:50
LastEditors: Wei Dongcheng
File: pc_capture.py
Description:
https://zhuanlan.zhihu.com/p/361569101
1、很详细的贴文，赞。另外，某些游戏截出来是透明的，或者全黑的，可能是用了directx。可以试试用d3dshot这个库来截。
2、另外有个问题 我同时开了2个game ,标题名都是一样的 实测会拿到第一个.有办法可以区分这两个吗
答：可以通过别的方式获取句柄，比如进程号，或者结合鼠标，通过获取鼠标所在位置句柄，或者将游戏窗口放在顶层，获取最顶层窗口句柄
3、你好 大佬 我直接copy代码 把进程标题 改成 计算器 截图是 全黑的 这是啥情况， 别的进程我也试了 也是全黑的
答：你截图的是UWP的计算器吧？这个计算器用GDI的方式，是截不到图的。

最小化后是借不到图的，需要把窗口显示为最大化或Normal，只要不最小化，放在后台也是可以截图到图的。
"""
import time
from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import cv2
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



def get_window_list(my_debug=False):
    """
    获取窗口列表
    :param my_debug: 是否debug模式，True则打印窗口列表信息
    :return: 窗口列表
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
    if my_debug:
        for i in range(len(titles)):
            print(titles[i])

    return titles


def capture(handle: HWND):
    """
    窗口客户区截图
    Args:
        handle (HWND): 要截图的窗口句柄
    Returns:
        numpy.ndarray: 截图数据
    """
    # 获取窗口客户区的大小
    r = RECT()
    GetClientRect(handle, byref(r))
    width, height = r.right, r.bottom
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
    return np.frombuffer(buffer, dtype=np.uint8).reshape(height, width, 4)


if __name__ == "__main__":

    get_window_list(my_debug=True)
    handle = windll.user32.FindWindowW(None, "Kanzi")  # OK, 在后台时截图失败
    print(handle)
    print(type(handle))
    if win32gui.IsIconic(handle):
        win32gui.ShowWindow(handle, win32con.SW_SHOWNORMAL)
        win32gui.SetForegroundWindow(1836510)  # 设置前置窗口
        # win32gui.SetFocus(handle)  # 设置聚焦窗口, 报错：pywintypes.error: (5, 'SetFocus', '拒绝访问。')
    # else:
    #     win32gui.ShowWindow(handle, win32con.SW_SHOWMINIMIZED)
    # handle = windll.user32.FindWindowW(None, "std_autotest – web_cam_util.py")  # OK
    # # handle = windll.user32.FindWindowW(None, "计算器")  # UWP程序截图为黑屏
    # # handle = windll.user32.FindWindowW(None, "pylearning – pc_capture.py")
    # # handle = windll.user32.FindWindowW(262836, 'Microsoft Store')  # OSError: exception: access violation reading 0x00000000000402B4
    start_time = time.time()
    image = capture(handle)
    print("cost time = " + str(round(time.time() - start_time, 3)))
    cv2.imwrite("test.png", image)
    cv2.imshow("Capture Test", image)  # 0.007
    cv2.waitKey()
