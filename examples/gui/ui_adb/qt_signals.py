# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/9 16:16
@File : qt_signals.py
@Desc : 
"""
from PySide2.QtCore import QObject, Signal


class QtSignals(QObject):
    sigAndroidOnOffLine = Signal(str, str)
    sigAndroidLogcatLine = Signal(str)
    sigAdbSendCmd = Signal(str)


MY_SIGNALS = QtSignals()
