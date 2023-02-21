# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @Administrator
@Time : 2023/1/17 8:40
@File : 034_reboot_check.py
@Desc :
"""
import atexit
import os
import subprocess
import time


class RebootCheck:

    def __init__(self, serial_num=None, adbPath=None):
        if adbPath is None or adbPath == "":
            self.exePath = "adb"
        else:
            self.exePath = adbPath
        # self.cwd = os.path.abspath(os.path.join(self.exePath, os.pardir))
        self.ret = None
        self.serialNum = serial_num

    def checkDeviceOnline(self):
        isOnline = False
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        try:
            cmd = f"{self.exePath} devices"
            args = cmd.split()
            self.ret = subprocess.Popen(args,
                                        # cwd=self.cwd,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        startupinfo=startupinfo
                                        )
            atexit.register(self.stop)
            while self.ret.poll() is None:
                line = self.ret.stdout.readline().decode("utf-8", "replace")
                if line is not None and line.strip() != "":
                    resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                    if resLine.__contains__("device"):
                        deviceSn = resLine.split()
                        if self.serialNum is None or self.serialNum == "":
                            isOnline = True
                        elif deviceSn[0] == self.serialNum:
                            isOnline = True
            # while self.ret.poll() is None:
            #     line = self.ret.stderr.readline().decode("utf-8", "replace")
            #     if line is not None and line.strip() != "":
            #         resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
            #         print(resLine)
            exit_result = self.ret.wait()
            print(f"exit_result={exit_result}")
            # self.ret.kill()
        except Exception as e:
            print(str(e))
        if isOnline is True:
            print("设备在线！pass")
        else:
            print("设备不在线fail")
        return isOnline

    def reboot(self):
        rebootOk = False
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        try:
            cmd = f"{self.exePath} reboot"
            args = cmd.split()
            self.ret = subprocess.Popen(args,
                                        # cwd=self.cwd,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        startupinfo=startupinfo
                                        )
            atexit.register(self.stop)
            while self.ret.poll() is None:
                line = self.ret.stdout.readline().decode("utf-8", "replace")
                if line is not None and line.strip() != "":
                    resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                    print(resLine)
            while self.ret.poll() is None:
                line = self.ret.stderr.readline().decode("utf-8", "replace")
                if line is not None and line.strip() != "":
                    resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                    print(resLine)
            exit_result = self.ret.wait()
            if exit_result == 0:
                print("重启命令执行成功")
                rebootOk = True
            else:
                print("重启失败")
            # self.ret.kill()
        except Exception as e:
            print(str(e))
        return rebootOk

    def stop(self):
        try:
            self.ret.stdin.write(f"^C".encode())
            self.ret.stdin.flush()
        except Exception as e:
            print(str(e))
        try:
            self.ret.kill()
        except Exception as e:
            print(str(e))

    def reboot_once(self, timeout=300):
        """重启，然后不断执行adb devices检测设备是否上线，上线则pass"""
        testPass = False
        rebootRet = self.reboot()
        assert rebootRet == True
        time.sleep(1)
        keepCheck = True
        start_time = time.time()
        while keepCheck:
            isOnline = self.checkDeviceOnline()
            if isOnline is True:
                testPass = True
                keepCheck = False
            elif time.time() - start_time >= timeout:
                keepCheck = False
                print("测试失败：设备超时未上线！")
            else:
                time.sleep(1)
        return testPass

    def reboot_test(self, timeout=300):
        assert self.reboot_once(timeout) == True

    def reboot_delay_once(self, delayTime=300):
        testPass = False
        rebootRet = self.reboot()
        assert rebootRet is True
        time.sleep(delayTime)
        isOnline = self.checkDeviceOnline()
        if isOnline is True:
            testPass = True
        return testPass

    def reboot_loop_test(self, testTimes=1000, delayTime=60, stopWhileFail=True):
        testCounter = 0
        passCounter = 0
        failCounter = 0
        keepTest = True
        while keepTest:
            testCounter += 1
            print(f"正在测试第{testCounter}次, 已pass: {passCounter}次， 已fail: {failCounter}")
            ret = self.reboot_delay_once(delayTime)
            if ret is True:
                passCounter += 1
            else:
                failCounter += 1
                if stopWhileFail is True:
                    keepTest = False
            if testCounter >= testTimes:
                keepTest = False
            print(f"已测试：{testCounter}次, pass: {passCounter}次， fail: {failCounter}")


if __name__ == "__main__":
    # check = RebootCheck(serial_num="12345678")  # 当有多个设备，需要传入设备串号当参数
    check = RebootCheck()  # 仅有一个设备，可以不传串号
    """
    testTimes: 测试次数
    delayTime: 重启后延时多长时间再使用adb devices检测设备是否上线，单位秒 5分钟=5*60=300秒
    stopWhileFail: 当有失败时是否停止测试
    """
    check.reboot_loop_test(testTimes=1000, delayTime=300, stopWhileFail=True)
