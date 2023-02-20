# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/3 16:53
@File : my_combo_box.py
@Desc : 
"""
from PySide2.QtCore import Qt
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QComboBox

from src.myutils.log_util import logger
from src.qt_signals import MY_SIGNALS


class MyComboBox(QComboBox):

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
        self.setEditable(True)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super(MyComboBox, self).keyPressEvent(event)  # 不中断父类事件的处理
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            text = self.currentText()
            logger.info(f"text={text}")
            MY_SIGNALS.sigEnterSend.emit(text)
            pass

