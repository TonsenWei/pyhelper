# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'serial_gui.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        if not MainForm.objectName():
            MainForm.setObjectName(u"MainForm")
        MainForm.resize(967, 750)
        self.gridLayout_4 = QGridLayout(MainForm)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayoutLeft = QGridLayout()
        self.gridLayoutLeft.setObjectName(u"gridLayoutLeft")
        self.gridLayout_2ShotCmd = QGridLayout()
        self.gridLayout_2ShotCmd.setObjectName(u"gridLayout_2ShotCmd")
        self.btnF01 = QPushButton(MainForm)
        self.btnF01.setObjectName(u"btnF01")

        self.gridLayout_2ShotCmd.addWidget(self.btnF01, 0, 0, 1, 1)

        self.lineEditF01 = QLineEdit(MainForm)
        self.lineEditF01.setObjectName(u"lineEditF01")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF01, 0, 1, 1, 1)

        self.btnF02 = QPushButton(MainForm)
        self.btnF02.setObjectName(u"btnF02")

        self.gridLayout_2ShotCmd.addWidget(self.btnF02, 1, 0, 1, 1)

        self.lineEditF02 = QLineEdit(MainForm)
        self.lineEditF02.setObjectName(u"lineEditF02")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF02, 1, 1, 1, 1)

        self.btnF03 = QPushButton(MainForm)
        self.btnF03.setObjectName(u"btnF03")

        self.gridLayout_2ShotCmd.addWidget(self.btnF03, 2, 0, 1, 1)

        self.lineEditF03 = QLineEdit(MainForm)
        self.lineEditF03.setObjectName(u"lineEditF03")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF03, 2, 1, 1, 1)

        self.btnF04 = QPushButton(MainForm)
        self.btnF04.setObjectName(u"btnF04")

        self.gridLayout_2ShotCmd.addWidget(self.btnF04, 3, 0, 1, 1)

        self.lineEditF04 = QLineEdit(MainForm)
        self.lineEditF04.setObjectName(u"lineEditF04")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF04, 3, 1, 1, 1)

        self.btnF05 = QPushButton(MainForm)
        self.btnF05.setObjectName(u"btnF05")

        self.gridLayout_2ShotCmd.addWidget(self.btnF05, 4, 0, 1, 1)

        self.lineEditF05 = QLineEdit(MainForm)
        self.lineEditF05.setObjectName(u"lineEditF05")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF05, 4, 1, 1, 1)

        self.btnF06 = QPushButton(MainForm)
        self.btnF06.setObjectName(u"btnF06")

        self.gridLayout_2ShotCmd.addWidget(self.btnF06, 5, 0, 1, 1)

        self.lineEditF06 = QLineEdit(MainForm)
        self.lineEditF06.setObjectName(u"lineEditF06")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF06, 5, 1, 1, 1)

        self.btnF07 = QPushButton(MainForm)
        self.btnF07.setObjectName(u"btnF07")

        self.gridLayout_2ShotCmd.addWidget(self.btnF07, 6, 0, 1, 1)

        self.lineEditF07 = QLineEdit(MainForm)
        self.lineEditF07.setObjectName(u"lineEditF07")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF07, 6, 1, 1, 1)

        self.btnF08 = QPushButton(MainForm)
        self.btnF08.setObjectName(u"btnF08")

        self.gridLayout_2ShotCmd.addWidget(self.btnF08, 7, 0, 1, 1)

        self.lineEditF08 = QLineEdit(MainForm)
        self.lineEditF08.setObjectName(u"lineEditF08")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF08, 7, 1, 1, 1)

        self.btnF09 = QPushButton(MainForm)
        self.btnF09.setObjectName(u"btnF09")

        self.gridLayout_2ShotCmd.addWidget(self.btnF09, 8, 0, 1, 1)

        self.lineEditF09 = QLineEdit(MainForm)
        self.lineEditF09.setObjectName(u"lineEditF09")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF09, 8, 1, 1, 1)

        self.btnF10 = QPushButton(MainForm)
        self.btnF10.setObjectName(u"btnF10")

        self.gridLayout_2ShotCmd.addWidget(self.btnF10, 9, 0, 1, 1)

        self.lineEditF10 = QLineEdit(MainForm)
        self.lineEditF10.setObjectName(u"lineEditF10")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF10, 9, 1, 1, 1)

        self.btnF11 = QPushButton(MainForm)
        self.btnF11.setObjectName(u"btnF11")

        self.gridLayout_2ShotCmd.addWidget(self.btnF11, 10, 0, 1, 1)

        self.lineEditF11 = QLineEdit(MainForm)
        self.lineEditF11.setObjectName(u"lineEditF11")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF11, 10, 1, 1, 1)

        self.btnF12 = QPushButton(MainForm)
        self.btnF12.setObjectName(u"btnF12")

        self.gridLayout_2ShotCmd.addWidget(self.btnF12, 11, 0, 1, 1)

        self.lineEditF12 = QLineEdit(MainForm)
        self.lineEditF12.setObjectName(u"lineEditF12")

        self.gridLayout_2ShotCmd.addWidget(self.lineEditF12, 11, 1, 1, 1)


        self.gridLayoutLeft.addLayout(self.gridLayout_2ShotCmd, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayoutLeft.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.gridLayoutInit = QGridLayout()
        self.gridLayoutInit.setObjectName(u"gridLayoutInit")
        self.label1Port = QLabel(MainForm)
        self.label1Port.setObjectName(u"label1Port")

        self.gridLayoutInit.addWidget(self.label1Port, 0, 0, 1, 1)

        self.comboBox1Port = QComboBox(MainForm)
        self.comboBox1Port.setObjectName(u"comboBox1Port")

        self.gridLayoutInit.addWidget(self.comboBox1Port, 0, 1, 1, 1)

        self.comboBox2Baudrate = QComboBox(MainForm)
        self.comboBox2Baudrate.setObjectName(u"comboBox2Baudrate")

        self.gridLayoutInit.addWidget(self.comboBox2Baudrate, 1, 1, 1, 1)

        self.label2Baudrate = QLabel(MainForm)
        self.label2Baudrate.setObjectName(u"label2Baudrate")

        self.gridLayoutInit.addWidget(self.label2Baudrate, 1, 0, 1, 1)

        self.label_4Parity = QLabel(MainForm)
        self.label_4Parity.setObjectName(u"label_4Parity")

        self.gridLayoutInit.addWidget(self.label_4Parity, 3, 0, 1, 1)

        self.label_5StopBit = QLabel(MainForm)
        self.label_5StopBit.setObjectName(u"label_5StopBit")

        self.gridLayoutInit.addWidget(self.label_5StopBit, 4, 0, 1, 1)

        self.comboBox5StopBit = QComboBox(MainForm)
        self.comboBox5StopBit.setObjectName(u"comboBox5StopBit")

        self.gridLayoutInit.addWidget(self.comboBox5StopBit, 4, 1, 1, 1)

        self.pushButton_2OpenSerial = QPushButton(MainForm)
        self.pushButton_2OpenSerial.setObjectName(u"pushButton_2OpenSerial")

        self.gridLayoutInit.addWidget(self.pushButton_2OpenSerial, 5, 0, 1, 1)

        self.pushButton_2CloseSerial = QPushButton(MainForm)
        self.pushButton_2CloseSerial.setObjectName(u"pushButton_2CloseSerial")

        self.gridLayoutInit.addWidget(self.pushButton_2CloseSerial, 5, 1, 1, 1)

        self.label3DataBit = QLabel(MainForm)
        self.label3DataBit.setObjectName(u"label3DataBit")

        self.gridLayoutInit.addWidget(self.label3DataBit, 2, 0, 1, 1)

        self.comboBox3DataBit = QComboBox(MainForm)
        self.comboBox3DataBit.setObjectName(u"comboBox3DataBit")

        self.gridLayoutInit.addWidget(self.comboBox3DataBit, 2, 1, 1, 1)

        self.comboBox4Parity = QComboBox(MainForm)
        self.comboBox4Parity.setObjectName(u"comboBox4Parity")

        self.gridLayoutInit.addWidget(self.comboBox4Parity, 3, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayoutInit.addItem(self.horizontalSpacer, 0, 2, 1, 1)


        self.gridLayoutLeft.addLayout(self.gridLayoutInit, 0, 0, 1, 1)

        self.btnMark = QPushButton(MainForm)
        self.btnMark.setObjectName(u"btnMark")

        self.gridLayoutLeft.addWidget(self.btnMark, 2, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutLeft, 0, 0, 1, 1)

        self.gridLayoutRight = QGridLayout()
        self.gridLayoutRight.setObjectName(u"gridLayoutRight")
        self.gridLayoutRight.setVerticalSpacing(5)
        self.tabWidgetSerialTrace = QTabWidget(MainForm)
        self.tabWidgetSerialTrace.setObjectName(u"tabWidgetSerialTrace")
        self.tabUnfilter = QWidget()
        self.tabUnfilter.setObjectName(u"tabUnfilter")
        self.gridLayout_3 = QGridLayout(self.tabUnfilter)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.textEditTraceUnfilter = QTextEdit(self.tabUnfilter)
        self.textEditTraceUnfilter.setObjectName(u"textEditTraceUnfilter")

        self.gridLayout_3.addWidget(self.textEditTraceUnfilter, 0, 0, 1, 1)

        self.tabWidgetSerialTrace.addTab(self.tabUnfilter, "")
        self.tabFilter = QWidget()
        self.tabFilter.setObjectName(u"tabFilter")
        self.gridLayout = QGridLayout(self.tabFilter)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.cbFilterKeyword = QComboBox(self.tabFilter)
        self.cbFilterKeyword.setObjectName(u"cbFilterKeyword")

        self.gridLayout.addWidget(self.cbFilterKeyword, 0, 0, 1, 1)

        self.checkBoxUseRe = QCheckBox(self.tabFilter)
        self.checkBoxUseRe.setObjectName(u"checkBoxUseRe")

        self.gridLayout.addWidget(self.checkBoxUseRe, 0, 1, 1, 1)

        self.textEditTraceFilter = QTextEdit(self.tabFilter)
        self.textEditTraceFilter.setObjectName(u"textEditTraceFilter")

        self.gridLayout.addWidget(self.textEditTraceFilter, 1, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.tabWidgetSerialTrace.addTab(self.tabFilter, "")

        self.gridLayoutRight.addWidget(self.tabWidgetSerialTrace, 0, 0, 1, 1)

        self.cbInputCmd = QComboBox(MainForm)
        self.cbInputCmd.setObjectName(u"cbInputCmd")

        self.gridLayoutRight.addWidget(self.cbInputCmd, 1, 0, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayoutRight, 0, 1, 1, 1)


        self.retranslateUi(MainForm)

        self.tabWidgetSerialTrace.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainForm)
    # setupUi

    def retranslateUi(self, MainForm):
        MainForm.setWindowTitle(QCoreApplication.translate("MainForm", u"Form", None))
        self.btnF01.setText(QCoreApplication.translate("MainForm", u"F1", None))
        self.btnF02.setText(QCoreApplication.translate("MainForm", u"F2", None))
        self.btnF03.setText(QCoreApplication.translate("MainForm", u"F3", None))
        self.btnF04.setText(QCoreApplication.translate("MainForm", u"F4", None))
        self.btnF05.setText(QCoreApplication.translate("MainForm", u"F5", None))
        self.btnF06.setText(QCoreApplication.translate("MainForm", u"F6", None))
        self.btnF07.setText(QCoreApplication.translate("MainForm", u"F7", None))
        self.btnF08.setText(QCoreApplication.translate("MainForm", u"F8", None))
        self.btnF09.setText(QCoreApplication.translate("MainForm", u"F9", None))
        self.btnF10.setText(QCoreApplication.translate("MainForm", u"F10", None))
        self.btnF11.setText(QCoreApplication.translate("MainForm", u"F11", None))
        self.btnF12.setText(QCoreApplication.translate("MainForm", u"F12", None))
        self.label1Port.setText(QCoreApplication.translate("MainForm", u"\u7aef\u53e3:", None))
        self.label2Baudrate.setText(QCoreApplication.translate("MainForm", u"\u6ce2\u7279\u7387:", None))
        self.label_4Parity.setText(QCoreApplication.translate("MainForm", u"\u5947\u5076\u6821\u9a8c:", None))
        self.label_5StopBit.setText(QCoreApplication.translate("MainForm", u"\u505c\u6b62\u4f4d:", None))
        self.pushButton_2OpenSerial.setText(QCoreApplication.translate("MainForm", u"\u6253\u5f00\u4e32\u53e3", None))
        self.pushButton_2CloseSerial.setText(QCoreApplication.translate("MainForm", u"\u5173\u95ed\u4e32\u53e3", None))
        self.label3DataBit.setText(QCoreApplication.translate("MainForm", u"\u6570\u636e\u4f4d:", None))
        self.btnMark.setText(QCoreApplication.translate("MainForm", u"Mark(Ctrl+M)", None))
        self.tabWidgetSerialTrace.setTabText(self.tabWidgetSerialTrace.indexOf(self.tabUnfilter), QCoreApplication.translate("MainForm", u"unfiltered", None))
        self.checkBoxUseRe.setText(QCoreApplication.translate("MainForm", u"\u4f7f\u7528\u6b63\u5219\u8868\u8fbe\u5f0f", None))
        self.tabWidgetSerialTrace.setTabText(self.tabWidgetSerialTrace.indexOf(self.tabFilter), QCoreApplication.translate("MainForm", u"Filtered", None))
    # retranslateUi

