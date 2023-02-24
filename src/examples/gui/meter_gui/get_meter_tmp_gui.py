# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'get_meter_tmp_gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_meterSampleGui(object):
    def setupUi(self, meterSampleGui):
        if not meterSampleGui.objectName():
            meterSampleGui.setObjectName(u"meterSampleGui")
        meterSampleGui.resize(896, 627)
        self.gridLayout = QGridLayout(meterSampleGui)
        self.gridLayout.setObjectName(u"gridLayout")
        self.groupBox = QGroupBox(meterSampleGui)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lblGetTmpPic = QLabel(self.groupBox)
        self.lblGetTmpPic.setObjectName(u"lblGetTmpPic")

        self.gridLayout_2.addWidget(self.lblGetTmpPic, 0, 0, 1, 2)

        self.lblSetMaxValue = QLabel(self.groupBox)
        self.lblSetMaxValue.setObjectName(u"lblSetMaxValue")

        self.gridLayout_2.addWidget(self.lblSetMaxValue, 1, 0, 1, 2)

        self.lblTips = QLabel(self.groupBox)
        self.lblTips.setObjectName(u"lblTips")
        self.lblTips.setMinimumSize(QSize(0, 0))

        self.gridLayout_2.addWidget(self.lblTips, 2, 0, 1, 5)

        self.lblCurrentTodo = QLabel(self.groupBox)
        self.lblCurrentTodo.setObjectName(u"lblCurrentTodo")

        self.gridLayout_2.addWidget(self.lblCurrentTodo, 3, 0, 1, 1)

        self.lblTodoTip = QLabel(self.groupBox)
        self.lblTodoTip.setObjectName(u"lblTodoTip")

        self.gridLayout_2.addWidget(self.lblTodoTip, 3, 1, 1, 2)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.gridLayout_2.addWidget(self.pushButton, 3, 3, 1, 1)

        self.horizontalSpacer = QSpacerItem(568, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 3, 4, 1, 1)

        self.lblSampleTip = QLabel(self.groupBox)
        self.lblSampleTip.setObjectName(u"lblSampleTip")

        self.gridLayout_2.addWidget(self.lblSampleTip, 4, 0, 1, 1)

        self.lblPleaseEdit = QLabel(self.groupBox)
        self.lblPleaseEdit.setObjectName(u"lblPleaseEdit")

        self.gridLayout_2.addWidget(self.lblPleaseEdit, 4, 3, 1, 1)

        self.comboBoxGetTmpPic = QComboBox(self.groupBox)
        self.comboBoxGetTmpPic.setObjectName(u"comboBoxGetTmpPic")

        self.gridLayout_2.addWidget(self.comboBoxGetTmpPic, 0, 2, 1, 2)

        self.comboBoxMaxValue = QComboBox(self.groupBox)
        self.comboBoxMaxValue.setObjectName(u"comboBoxMaxValue")
        self.comboBoxMaxValue.setEditable(True)

        self.gridLayout_2.addWidget(self.comboBoxMaxValue, 1, 2, 1, 1)

        self.lblSample = QLabel(self.groupBox)
        self.lblSample.setObjectName(u"lblSample")

        self.gridLayout_2.addWidget(self.lblSample, 5, 0, 1, 3)

        self.lblResult = QLabel(self.groupBox)
        self.lblResult.setObjectName(u"lblResult")

        self.gridLayout_2.addWidget(self.lblResult, 5, 3, 1, 2)

        self.gridLayout_2.setRowStretch(0, 1)
        self.gridLayout_2.setRowStretch(1, 1)
        self.gridLayout_2.setRowStretch(2, 1)
        self.gridLayout_2.setRowStretch(3, 1)
        self.gridLayout_2.setRowStretch(4, 1)
        self.gridLayout_2.setRowStretch(5, 100)

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)


        self.retranslateUi(meterSampleGui)

        QMetaObject.connectSlotsByName(meterSampleGui)
    # setupUi

    def retranslateUi(self, meterSampleGui):
        meterSampleGui.setWindowTitle(QCoreApplication.translate("meterSampleGui", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("meterSampleGui", u"\u6a21\u677f\u7f16\u8f91", None))
        self.lblGetTmpPic.setText(QCoreApplication.translate("meterSampleGui", u"\u7b2c\u4e00\u6b65:\u83b7\u53d6\u6a21\u677f\u56fe", None))
        self.lblSetMaxValue.setText(QCoreApplication.translate("meterSampleGui", u"\u7b2c\u4e8c\u6b65:\u8bbe\u7f6e\u523b\u5ea6\u6700\u5927\u503c", None))
        self.lblTips.setText(QCoreApplication.translate("meterSampleGui", u"\u7b2c\u4e09\u6b65:\u4f9d\u6b21\u70b9\u51fb\u4eea\u8868\u6307\u9488\u65cb\u8f6c\u7684\u4e2d\u5fc3\u70b9\u30010\u523b\u5ea6\u503c\u5750\u6807\u3001\u6700\u5927\u503c\u5750\u6807", None))
        self.lblCurrentTodo.setText(QCoreApplication.translate("meterSampleGui", u"\u5f53\u524d\u9700\u8981\u64cd\u4f5c:", None))
        self.lblTodoTip.setText(QCoreApplication.translate("meterSampleGui", u"\u70b9\u51fb\u4eea\u8868\u6307\u9488\u65cb\u8f6c\u7684\u4e2d\u5fc3\u70b9", None))
        self.pushButton.setText(QCoreApplication.translate("meterSampleGui", u"\u4e0a\u4e00\u6b65", None))
        self.lblSampleTip.setText(QCoreApplication.translate("meterSampleGui", u"\u793a\u4f8b:", None))
        self.lblPleaseEdit.setText(QCoreApplication.translate("meterSampleGui", u"\u8bf7\u4f9d\u6b21\u6307\u9488\u65cb\u8f6c\u70b9\u30010\u523b\u5ea6\u3001\u6700\u5927\u523b\u5ea6:", None))
        self.comboBoxMaxValue.setCurrentText(QCoreApplication.translate("meterSampleGui", u"100", None))
        self.lblSample.setText(QCoreApplication.translate("meterSampleGui", u"lblSample", None))
        self.lblResult.setText(QCoreApplication.translate("meterSampleGui", u"lblResult", None))
    # retranslateUi

