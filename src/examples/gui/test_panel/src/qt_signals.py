# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/3 16:55
@File : qt_signals.py
@Desc : 
"""
from PySide2.QtCore import QObject, Signal


class QtSignals(QObject):
    sigEnterSend = Signal(str, str, str)  # sigName, dataType, value
    sigUpdateSendAddr = Signal(str, str)


MY_SIGNALS = QtSignals()
