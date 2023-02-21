# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'data_line.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(762, 65)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.lblSigName = QLabel(Form)
        self.lblSigName.setObjectName(u"lblSigName")
        self.lblSigName.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.lblSigName, 0, 1, 1, 1)

        self.lblDataType = QLabel(Form)
        self.lblDataType.setObjectName(u"lblDataType")
        self.lblDataType.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.lblDataType, 0, 2, 1, 1)

        self.btnSend = QPushButton(Form)
        self.btnSend.setObjectName(u"btnSend")
        self.btnSend.setMinimumSize(QSize(0, 35))
        self.btnSend.setMaximumSize(QSize(16777215, 16777215))

        self.gridLayout.addWidget(self.btnSend, 0, 4, 1, 1)

        self.comboBoxInput = QComboBox(Form)
        self.comboBoxInput.setObjectName(u"comboBoxInput")
        self.comboBoxInput.setMinimumSize(QSize(0, 30))
        self.comboBoxInput.setMaximumSize(QSize(16777215, 16777215))
        self.comboBoxInput.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxInput, 0, 3, 1, 1)

        self.lblFuncName = QLabel(Form)
        self.lblFuncName.setObjectName(u"lblFuncName")
        self.lblFuncName.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.lblFuncName, 0, 0, 1, 1)

        self.gridLayout.setColumnStretch(0, 6)
        self.gridLayout.setColumnStretch(1, 6)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout.setColumnStretch(3, 2)
        self.gridLayout.setColumnStretch(4, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lblSigName.setText(QCoreApplication.translate("Form", u"speed_limit_value", None))
        self.lblDataType.setText(QCoreApplication.translate("Form", u"int", None))
        self.btnSend.setText(QCoreApplication.translate("Form", u"Send", None))
        self.lblFuncName.setText(QCoreApplication.translate("Form", u"\u9650\u901f\u6807\u5fd7", None))
    # retranslateUi

