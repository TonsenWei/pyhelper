# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/16 15:35
@File : 020_pyqt5_screencap.py
@Desc : 使用Pyqt5对PC应用进行截图
"""
# -*- coding: utf-8 -*-
import time

from PyQt5.QtWidgets import QApplication
import win32gui
from numpy import array, uint8, ndarray


# 直接写一个类，方便以后使用
class Screen:
    def __init__(self, win_title=None, win_class=None, hwnd=None) -> None:
        self.app = QApplication(['WindowCapture'])
        self.screen = QApplication.primaryScreen()
        self.bind(win_title, win_class, hwnd)

    def bind(self, win_title=None, win_class=None, hwnd=None):
        """可以直接传入句柄，否则就根据class和title来查找，并把句柄做为实例属性 self._hwnd"""
        if not hwnd:
            self._hwnd = win32gui.FindWindow(win_class, win_title)
        else:
            self._hwnd = hwnd

    def capture(self, savename='') -> ndarray:
        """截图方法，在窗口为 1920 x 1080 大小下，最快速度25ms (grabWindow: 17ms, to_cvimg: 8ms)"""

        start_time = time.time()

        def to_cvimg(pix):
            """将self.screen.grabWindow 返回的 Pixmap 转换为 ndarray，方便opencv使用"""
            qimg = pix.toImage()
            temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
            temp_shape += (4,)
            ptr = qimg.bits()
            ptr.setsize(qimg.byteCount())
            result = array(ptr, dtype=uint8).reshape(temp_shape)
            return result[..., :3]

        self.pix = self.screen.grabWindow(self._hwnd)
        print(f"cost_time = {time.time() - start_time}")  # 0.007740974426269531
        self.img = to_cvimg(self.pix)
        if savename:
            self.pix.save(savename)
        return self.img


if __name__ == '__main__':
    screen = Screen(win_title='Kanzi')
    screen.capture('test.png')
