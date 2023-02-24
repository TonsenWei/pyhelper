# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/17 14:23
@File : 021_start_exe.py
@Desc : 
"""
import os
import subprocess
import threading
import time
from sys import platform as sysPlatform  # popen静默模式

from utils.file_util import FileUtil

exePath = r"E:\Tonsen\001_Projects\HuaYangV3\bin_20220830_V3.9\bin\V3_Master.exe"
# exePath = r"D:\z\myexe\YY\YY.exe"
cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
print(f"exePath={exePath}, cwd={cwd}")


class RunExeThread(threading.Thread):

    def __init__(self, exePath=""):
        threading.Thread.__init__(self)
        self.exePath = exePath
        self.cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
        self.ret = None

    def run(self) -> None:
        # 设置子进程启用静默模式，不显示控制台窗口
        self.ret = subprocess.run([self.exePath],
                                  cwd=self.cwd,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)


class KillExeThread(threading.Thread):

    def __init__(self, exePath=""):
        threading.Thread.__init__(self)
        self.exePath = exePath
        self.cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
        fpath, fname = os.path.split(exePath)
        self.exeName = fname
        self.ret = None

    def run(self) -> None:
        # 设置子进程启用静默模式，不显示控制台窗口
        cmdList = ["taskkill", "/f", "/im", self.exeName]
        self.ret = subprocess.run(cmdList,
                                  cwd=self.cwd,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        outInfo = str(self.ret.stdout, encoding="gbk")
        errInfo = str(self.ret.stderr, encoding="gbk")
        if outInfo:
            print(outInfo)
        if errInfo:
            print(errInfo)

def start_exe():
    # 设置子进程启用静默模式，不显示控制台窗口
    ret = subprocess.run([exePath],
                         cwd=cwd,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE
                         )
    print("start exe done")
    while True:
        if not ret.poll() is None:
            break
        time.sleep(1)
        print(ret.poll())
    # print(f"ret={ret.wait()}")


def start_cmd_exe():
    cmd = f"start \"test\" /d {cwd} /wait \"V3_Master.exe\" "
    # 设置子进程启用静默模式，不显示控制台窗口
    ret = subprocess.Popen(  # 打开管道
        ["start", "\"test\"", "/d", cwd, "/wait", "\"V3_Master.exe\""],
        # cwd=cwd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    # print(f"ret={ret.wait()}")


def os_sys_start_exe():
    """ ok """
    cmd = f"start \"test\" /d {cwd} /wait \"V3_Master.exe\" "
    os.system(cmd)


if __name__ == "__main__":
    # start_cmd_exe()
    # os_sys_start_exe()
    # th = threading.Thread(target=start_exe)
    # th.setDaemon(True)
    # th.start()

    # start exe
    # th = RunExeThread(exePath)
    # th.setDaemon(True)
    # th.start()

    # kill exe
    killTh = KillExeThread(exePath)
    killTh.setDaemon(True)
    killTh.start()

    counter = 0
    timeout = 3
    while True:
        time.sleep(1)
        counter += 1
        print(f"running {counter} ...")
        if counter == timeout:
            counter = 0
            print("exit")
            break
    print("end")
    # os_sys_start_exe()
