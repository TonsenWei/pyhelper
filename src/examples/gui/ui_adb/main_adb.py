# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/1 14:55
@File : serial_main.py
@Desc : pip install pyside2 -i https://pypi.douban.com/simple/
"""
import atexit
import os
import subprocess
import sys
import threading

from PySide2.QtGui import QTextCursor, Qt
from PySide2.QtWidgets import QApplication, QWidget, QPlainTextEdit

from examples.gui.ui_adb.device_monitor import DeviceMonitorThread
from examples.gui.ui_adb.qt_signals import MY_SIGNALS
from examples.gui.ui_adb.ui_adb import Ui_MainForm
from adbutils import adb

keepGetLogcat = True
logcatRead = None


def getLogcat():
    global keepGetLogcat
    # cmd = "adb logcat -v threadtime long"
    exePath = r"D:\projects\python\pylearning\examples\gui\ui_adb\adb_exe\adb.exe"
    cmd = "logcat"
    cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    obj = subprocess.Popen(f"{exePath} {cmd}",
                           cwd=cwd,
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           startupinfo=startupinfo  # 开启静默模式
                           )
    while obj.poll() is None and keepGetLogcat is True:
        line = obj.stdout.readline().decode("utf-8", "replace")
        if line is not None and line.strip() != "":
            resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
            # print(resLine)
            MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
    # excute_cmd_result = obj.wait()
    # if excute_cmd_result != 0:
    #     print(str(excute_cmd_result) + "=" + cmd)
    # else:
    #     print(str(excute_cmd_result) + "=" + cmd)
    print("kill")
    obj.kill()
    print("killed")


def adbUtilsGetLogcat():
    # for d in adb.device_list():
    #     print(d.serial)
    d = adb.device()
    stream = d.shell("logcat -v threadtime long", stream=True)
    with stream:
        f = stream.conn.makefile()
        while keepGetLogcat:
            line = f.readline()
            if line != "":
                print(f"logcat: {line.rstrip()}")
        f.close()


class GetLogcatThead(threading.Thread):
    """
    实时获取logcat线程
    """

    def __init__(self, deviceSn=""):
        threading.Thread.__init__(self)
        self.keepGetLogcat = True
        self.ret = None
        self.deviceSn = deviceSn

    def run(self) -> None:
        exePath = r"D:\projects\python\pylearning\examples\gui\ui_adb\adb_exe\adb.exe"
        cmd = "logcat -v threadtime"
        cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        if self.deviceSn is not None and self.deviceSn != "":
            getCmd = f"{exePath} -s {self.deviceSn} {cmd}"
        else:
            getCmd = f"{exePath} {cmd}"
        self.ret = subprocess.Popen(getCmd,
                                    cwd=cwd,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    startupinfo=startupinfo  # 开启静默模式
                                    )
        atexit.register(self.stop)  # 注册程序终止时执行强制停止子进程
        while self.ret.poll() is None and self.keepGetLogcat is True:
            line = self.ret.stdout.readline().decode("utf-8", "replace")
            if line is not None and line.strip() != "":
                resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                # print(resLine)
                # if resLine.__contains__("MiuiGallery2_BatteryMonitor"):
                #     MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
                MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
        exit_result = self.ret.wait()
        print(f"exit_result={exit_result}")
        print("kill")
        self.ret.kill()
        print("killed")

    def stop(self):
        try:
            self.ret.stdin.write(f"^C".encode())
            self.ret.stdin.flush()
        except Exception as e:
            print(e)
        self.keepGetLogcat = False
        self.ret.kill()

    def __del__(self):
        try:
            self.stop()
            atexit.unregister(self.stop)  # 移除退出处理
            print('GetLogcatThead API 析构！')
        except Exception as e:
            print(f"{e}")


class ThreadSendCmd(threading.Thread):

    def __init__(self, cmd):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.keepReadStream = True

    def run(self) -> None:
        print("send cmd thread start")
        exePath = r"D:\projects\python\pylearning\examples\gui\ui_adb\adb_exe\adb.exe"
        # self.cmd = ""
        # cmd = "logcat -v threadtime"
        cwd = os.path.abspath(os.path.join(exePath, os.pardir))  # 获取exe父文件夹
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        # allCmd = f"{exePath} {self.cmd}\n"
        # allCmd = f"adb {self.cmd}\n"
        # print(f"allCmd={allCmd}")
        try:
            self.ret = subprocess.Popen(self.cmd.split(),
                                        cwd=cwd,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        startupinfo=startupinfo  # 开启静默模式
                                        )
            print("before register")
            atexit.register(self.stop)  # 注册程序终止时执行强制停止子进程
            print("after register")
            while self.ret.poll() is None and self.keepReadStream is True:
                line = self.ret.stdout.readline().decode("utf-8", "replace")
                if line is not None and line.strip() != "":
                    resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                    # print(resLine)
                    print(f"stdout={resLine}")
                    # if resLine.__contains__("MiuiGallery2_BatteryMonitor"):
                    #     MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
                    MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
            while self.ret.poll() is None and self.keepReadStream is True:
                line = self.ret.stderr.readline().decode("utf-8", "replace")
                if line is not None and line.strip() != "":
                    resLine = line.rstrip("\n").rstrip("\r").lstrip("\r")
                    print(f"stderr={resLine}")
                    # if resLine.__contains__("MiuiGallery2_BatteryMonitor"):
                    #     MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
                    MY_SIGNALS.sigAndroidLogcatLine.emit(resLine)
            exit_result = self.ret.wait()
            print(f"exit_result={exit_result}")
            print("kill")
            self.ret.kill()
            print("killed")
        except Exception as e:
            print(e)
            MY_SIGNALS.sigAndroidLogcatLine.emit(f"{e}")

    def send(self, cmd):
        try:
            print(f"send = {cmd}")
            self.ret.stdin.write(f"{cmd}".encode())
            self.ret.stdin.flush()
        except Exception as e:
            print("send error")
            print(e)

    def stop(self):
        try:
            self.ret.stdin.write(f"^C".encode())
            self.ret.stdin.flush()
        except Exception as e:
            print("stop write error")
            print(e)
        self.keepReadStream = False
        try:
            self.ret.kill()
        except Exception as e:
            print("kill error")
            print(e)


def startGetLogcat():
    keepGetLogcat = True
    th = GetLogcatThead()
    th.setDaemon(True)
    th.start()
    # global logcatRead
    # if logcatRead is None:
    #     logcatRead = LogcatReader()


def stopGetLogcat():
    global keepGetLogcat
    keepGetLogcat = False
    # global logcatRead
    # if logcatRead is not None:
    #     logcatRead.stop()


currentDevice = ""

if __name__ == "__main__":
    th = None
    app = QApplication([])
    main_win = QWidget()
    form = Ui_MainForm()
    form.setupUi(main_win)
    form.splitter.setSizes([100, 500])
    form.textEditLogcat.setLineWrapMode(QPlainTextEdit.NoWrap)  # 不换行，超过宽度后会出现水平滚动条
    # self.serialGui.textEditTraceUnfilter.setLineWrapMode(QTextEdit.NoWrap)  # 不换行，超过宽度后会出现水平滚动条
    form.checkBoxFilter.setCheckState(Qt.Checked)
    currentKeywords = form.comboBoxKeywords.currentText()

    devicesSnList = []
    thSendCmd = None


    def onOffLine(sn, onOffLine):
        # form.comboBoxDeivce.findText(sn)  # 查找某文字对应的index
        form.comboBoxDeivce.clear()
        if onOffLine == "online":  # 设备上线，检查是否是已选择的设备上线，是则开启日志读取
            print(f"onOffLine = {onOffLine}")
            devicesSnList.append(sn)
            form.comboBoxDeivce.addItems(devicesSnList)
            print(f"currentDevice={currentDevice}, sn={sn}")
            if sn == currentDevice:  # 上线的是之前选择的设备
                print("上线的是之前选择的设备")
                form.comboBoxDeivce.setCurrentText(currentDevice)
        else:  # 设备离线
            currentDeivce = form.comboBoxDeivce.currentText()
            if currentDeivce == sn:  # 离线的是当前选中的设备，则需要停止当前设备的检测
                devicesSnList.remove(sn)
                form.comboBoxDeivce.addItems(devicesSnList)
            else:  # 离线的不是当前设备，则当前设备检测不改变
                devicesSnList.remove(sn)
                form.comboBoxDeivce.addItems(devicesSnList)
                form.comboBoxDeivce.setCurrentText(currentDeivce)


    def appendLogcat(line):
        form.textEditLogcat.appendPlainText(line)
        if form.textEditLogcat.hasFocus() is False:
            form.textEditLogcat.moveCursor(QTextCursor.End)
            form.textEditLogcat.moveCursor(QTextCursor.StartOfLine)


    def start_logcat_get():
        global th
        if th is not None and th.is_alive() is True:
            print("已有日志获取线程执行中")
        else:
            currentDevice = form.comboBoxDeivce.currentText()
            th = GetLogcatThead(currentDevice)
            th.setDaemon(True)
            th.start()


    def stop_logcat_get():
        global th
        th.stop()

    def cmdSend(cmd):
        global thSendCmd
        print(f"send = {cmd}")
        # thSendCmd = ThreadSendCmd(cmd)
        if thSendCmd is not None and thSendCmd.is_alive() is True:
            print("已有发送线程在运行")
            if cmd == chr(3):
                thSendCmd.stop()
            else:
                thSendCmd.send(cmd)
        else:
            thSendCmd = ThreadSendCmd(cmd)
            thSendCmd.setDaemon(True)
            thSendCmd.start()
        form.cbInputCmd.setCurrentText("")

    form.btnStartGetLogcat.clicked.connect(start_logcat_get)
    form.btnStopGetLogcat.clicked.connect(stop_logcat_get)

    MY_SIGNALS.sigAndroidOnOffLine.connect(onOffLine)
    MY_SIGNALS.sigAndroidLogcatLine.connect(appendLogcat)
    MY_SIGNALS.sigAdbSendCmd.connect(cmdSend)
    main_win.show()
    print("showed")
    thMonitor = DeviceMonitorThread()
    thMonitor.setDaemon(True)
    thMonitor.start()
    sys.exit(app.exec_())

