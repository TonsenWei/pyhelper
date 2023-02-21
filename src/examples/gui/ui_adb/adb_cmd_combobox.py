# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/19 10:04
@File : adb_cmd_combobox.py
@Desc : 
"""
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QComboBox, QApplication

from examples.gui.ui_adb.qt_signals import MY_SIGNALS


class AdbCmdComboBox(QComboBox):

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        if QApplication.keyboardModifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_C:
                print("CTRL + C pressed")
                MY_SIGNALS.sigAdbSendCmd.emit(f"{chr(3)}")
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            print("enter or return pressed")
            cmd = self.currentText()
            MY_SIGNALS.sigAdbSendCmd.emit(f"{cmd}\r\n")

