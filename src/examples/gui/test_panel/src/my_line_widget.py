# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/3 17:03
@File : my_line_widget.py
@Desc : 
"""
from PySide2.QtCore import Qt, QMetaObject, QCoreApplication, QSize
from PySide2.QtGui import QKeyEvent
from PySide2.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QGridLayout

from src.myutils.log_util import logger
from src.qt_signals import MY_SIGNALS

qssStyle = '''
        MyLineWidget:hover {
            background-color: lightgreen;
        }
        '''


class MyLineWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi()
        # self.setStyleSheet(qssStyle)

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Form")
        self.resize(762, 65)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lblSigName = QLabel(self)
        self.lblSigName.setObjectName(u"lblSigName")
        self.lblSigName.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.lblSigName, 0, 1, 1, 1)

        self.lblDataType = QLabel(self)
        self.lblDataType.setObjectName(u"lblDataType")
        self.lblDataType.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.lblDataType, 0, 2, 1, 1)

        self.btnSend = QPushButton(self)
        self.btnSend.setObjectName(u"btnSend")
        self.btnSend.setMinimumSize(QSize(0, 35))
        self.btnSend.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.btnSend, 0, 4, 1, 1)

        self.comboBoxInput = QComboBox(self)
        self.comboBoxInput.setObjectName(u"comboBoxInput")
        self.comboBoxInput.setMinimumSize(QSize(0, 30))
        self.comboBoxInput.setMaximumSize(QSize(16777215, 16777215))
        self.comboBoxInput.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxInput, 0, 3, 1, 1)

        self.lblFuncName = QLabel(self)
        self.lblFuncName.setObjectName(u"lblFuncName")
        self.lblFuncName.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.lblFuncName, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 6)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

        # self.setStyleSheet(qssStyle)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblSigName.setText(QCoreApplication.translate("Form", u"speed_limit_value", None))
        self.lblDataType.setText(QCoreApplication.translate("Form", u"int", None))
        self.btnSend.setText(QCoreApplication.translate("Form", u"Send", None))
        self.lblFuncName.setText(QCoreApplication.translate("Form", u"\u9650\u901f\u6807\u5fd7", None))

    # retranslateUi

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super(MyLineWidget, self).keyPressEvent(event)  # 不中断父类事件的处理
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            sigName = self.lblSigName.text()
            dataType = self.lblDataType.text()
            value = self.comboBoxInput.currentText()
            logger.info(f"sigName={sigName}, dataType={dataType}, value={value}")
            MY_SIGNALS.sigEnterSend.emit(sigName, dataType, value)
            pass
