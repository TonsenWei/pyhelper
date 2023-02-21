# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/9 15:38
@File : device_monitor.py
@Desc : 
"""
import copy
import operator
import threading
import time

from adbutils import adb

from examples.gui.ui_adb.qt_signals import MY_SIGNALS


class DeviceMonitorThread(threading.Thread):

    def __init__(self, adbPath=""):
        threading.Thread.__init__(self)
        self.adbPath = adbPath
        self.keepMonitor = True
        self.deviceSnList = []

    def run(self) -> None:
        while self.keepMonitor:
            try:
                devices = adb.device_list()
                devicesSn = [x.serial for x in devices]
                devicesSn.sort()
                if operator.eq(self.deviceSnList, devicesSn) is False:
                    offlineDevices = list(set(self.deviceSnList).difference(set(devicesSn)))
                    if len(offlineDevices) > 0:  # 下线设备
                        # 发送下线设备信号
                        print(f"下线设备：{[x for x in offlineDevices]}")
                        [MY_SIGNALS.sigAndroidOnOffLine.emit(x, "offline") for x in onlineDevices]
                    else:
                        onlineDevices = list(set(devicesSn).difference(set(self.deviceSnList)))
                        print(f"上线设备：{[x for x in onlineDevices]}")
                        [MY_SIGNALS.sigAndroidOnOffLine.emit(x, "online") for x in onlineDevices]
                    self.deviceSnList = copy.deepcopy(devicesSn)
                else:
                    time.sleep(1)
            except Exception as e:
                print(str(e))
                time.sleep(1)

    def stopMonitor(self):
        self.keepMonitor = False


if __name__ == "__main__":
    th = DeviceMonitorThread()
    th.setDaemon(True)
    th.start()
    while True:
        pass