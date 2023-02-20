# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/9 16:45
@File : logcat_reader.py
@Desc : 
"""
import atexit
import os
import subprocess

from examples.gui.ui_adb.qt_signals import MY_SIGNALS


class LogcatReader:
    """
    通过adb logcat -v threadtime long命令，读取logcat
    """

    def __init__(self, exePath=""):
        self.keepRead = True
        if exePath is None or exePath == "":
            self.exePath = "adb"
        else:
            self.exePath = exePath
        cwd = os.path.abspath(os.path.join(self.exePath, os.pardir))  # 获取exe父文件夹
        clearCmd = f"{self.exePath} logcat -c && "
        args = f" logcat -v threadtime long"
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        self.ret = subprocess.Popen(  # 打开管道
            f"{clearCmd}{self.exePath}{args}", cwd=cwd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=startupinfo  # 开启静默模式
        )
        print(f"LogcatReader pid={self.ret.pid}")
        atexit.register(self.stop)  # 注册程序终止时执行强制停止子进程
        while self.keepRead is True:
            while self.ret.poll() is None and self.keepRead is True:
                line = self.ret.stdout.readline().decode("utf-8", "replace")
                if line is not None and line.strip() != "":
                    resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                    print(resLine)
                    MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)

    def stop(self):
        print("stop==================================================")
        self.keepRead = False
        try:
            if self.ret.poll() is None:
                print(f"kill pid: {self.ret.pid}")
            self.ret.kill()  # 关闭子进程。误重复调用似乎不会有坏的影响
        except Exception as e:
            print(e)

    def __del__(self):
        try:
            self.stop()
            atexit.unregister(self.stop)  # 移除退出处理
            print('LogcatReader API 析构！')
        except Exception as e:
            print(f"{e}")
