# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'test_panel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_PanelTool(object):
    def setupUi(self, PanelTool):
        if not PanelTool.objectName():
            PanelTool.setObjectName(u"PanelTool")
        PanelTool.resize(762, 790)
        PanelTool.setStyleSheet(u"")
        self.centralwidget = QWidget(PanelTool)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(0)
        self.widgetSettings = QWidget(self.centralwidget)
        self.widgetSettings.setObjectName(u"widgetSettings")
        self.gridLayout_2 = QGridLayout(self.widgetSettings)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBoxSettinigs = QGroupBox(self.widgetSettings)
        self.groupBoxSettinigs.setObjectName(u"groupBoxSettinigs")
        self.gridLayout = QGridLayout(self.groupBoxSettinigs)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblPanelFilePath = QLabel(self.groupBoxSettinigs)
        self.lblPanelFilePath.setObjectName(u"lblPanelFilePath")
        self.lblPanelFilePath.setMinimumSize(QSize(0, 25))

        self.gridLayout.addWidget(self.lblPanelFilePath, 0, 0, 1, 1)

        self.btnSelPanel = QPushButton(self.groupBoxSettinigs)
        self.btnSelPanel.setObjectName(u"btnSelPanel")
        self.btnSelPanel.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.btnSelPanel, 0, 7, 1, 1)

        self.radioButtonNet = QRadioButton(self.groupBoxSettinigs)
        self.radioButtonNet.setObjectName(u"radioButtonNet")
        self.radioButtonNet.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.radioButtonNet, 1, 0, 1, 1)

        self.cbAtConnector = QCheckBox(self.groupBoxSettinigs)
        self.cbAtConnector.setObjectName(u"cbAtConnector")
        self.cbAtConnector.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.cbAtConnector, 1, 1, 1, 1)

        self.cbDoubleComaConnector = QCheckBox(self.groupBoxSettinigs)
        self.cbDoubleComaConnector.setObjectName(u"cbDoubleComaConnector")
        self.cbDoubleComaConnector.setMinimumSize(QSize(0, 30))
        self.cbDoubleComaConnector.setTristate(False)

        self.gridLayout.addWidget(self.cbDoubleComaConnector, 1, 2, 1, 1)

        self.lblBaseUrl = QLabel(self.groupBoxSettinigs)
        self.lblBaseUrl.setObjectName(u"lblBaseUrl")
        self.lblBaseUrl.setMinimumSize(QSize(0, 30))
        self.lblBaseUrl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblBaseUrl, 1, 3, 1, 1)

        self.lblNetPort = QLabel(self.groupBoxSettinigs)
        self.lblNetPort.setObjectName(u"lblNetPort")
        self.lblNetPort.setMinimumSize(QSize(0, 30))
        self.lblNetPort.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblNetPort, 1, 6, 1, 1)

        self.comboBoxNetPort = QComboBox(self.groupBoxSettinigs)
        self.comboBoxNetPort.addItem("")
        self.comboBoxNetPort.addItem("")
        self.comboBoxNetPort.setObjectName(u"comboBoxNetPort")
        self.comboBoxNetPort.setMinimumSize(QSize(0, 30))
        self.comboBoxNetPort.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxNetPort, 1, 7, 1, 1)

        self.radioButtonSerial = QRadioButton(self.groupBoxSettinigs)
        self.radioButtonSerial.setObjectName(u"radioButtonSerial")
        self.radioButtonSerial.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.radioButtonSerial, 2, 0, 1, 1)

        self.lblComPort = QLabel(self.groupBoxSettinigs)
        self.lblComPort.setObjectName(u"lblComPort")
        self.lblComPort.setMinimumSize(QSize(0, 30))
        self.lblComPort.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblComPort, 2, 1, 1, 1)

        self.comboBoxComPort = QComboBox(self.groupBoxSettinigs)
        self.comboBoxComPort.setObjectName(u"comboBoxComPort")
        self.comboBoxComPort.setMinimumSize(QSize(0, 30))
        self.comboBoxComPort.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxComPort, 2, 2, 1, 1)

        self.lblBaudrate = QLabel(self.groupBoxSettinigs)
        self.lblBaudrate.setObjectName(u"lblBaudrate")
        self.lblBaudrate.setMinimumSize(QSize(0, 30))
        self.lblBaudrate.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblBaudrate, 2, 3, 1, 1)

        self.comboBoxBaudrate = QComboBox(self.groupBoxSettinigs)
        self.comboBoxBaudrate.setObjectName(u"comboBoxBaudrate")
        self.comboBoxBaudrate.setMinimumSize(QSize(0, 30))
        self.comboBoxBaudrate.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxBaudrate, 2, 4, 1, 1)

        self.btnOpen = QPushButton(self.groupBoxSettinigs)
        self.btnOpen.setObjectName(u"btnOpen")
        self.btnOpen.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.btnOpen, 2, 5, 1, 1)

        self.btnClose = QPushButton(self.groupBoxSettinigs)
        self.btnClose.setObjectName(u"btnClose")
        self.btnClose.setMinimumSize(QSize(0, 35))

        self.gridLayout.addWidget(self.btnClose, 2, 6, 1, 1)

        self.comboBoxBaseUrl = QComboBox(self.groupBoxSettinigs)
        self.comboBoxBaseUrl.addItem("")
        self.comboBoxBaseUrl.setObjectName(u"comboBoxBaseUrl")
        self.comboBoxBaseUrl.setMinimumSize(QSize(0, 30))
        self.comboBoxBaseUrl.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxBaseUrl, 1, 4, 1, 2)

        self.comboBoxPanelPath = QComboBox(self.groupBoxSettinigs)
        self.comboBoxPanelPath.setObjectName(u"comboBoxPanelPath")
        self.comboBoxPanelPath.setMinimumSize(QSize(0, 30))
        self.comboBoxPanelPath.setEditable(True)

        self.gridLayout.addWidget(self.comboBoxPanelPath, 0, 1, 1, 6)


        self.gridLayout_2.addWidget(self.groupBoxSettinigs, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.widgetSettings, 0, 0, 1, 1)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.general = QWidget()
        self.general.setObjectName(u"general")
        self.gridLayout_4 = QGridLayout(self.general)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setVerticalSpacing(10)
        self.lblFuncDesc = QLabel(self.general)
        self.lblFuncDesc.setObjectName(u"lblFuncDesc")
        self.lblFuncDesc.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lblFuncDesc, 0, 0, 1, 1)

        self.lblSignalName = QLabel(self.general)
        self.lblSignalName.setObjectName(u"lblSignalName")
        self.lblSignalName.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lblSignalName, 0, 1, 1, 1)

        self.lblDataType = QLabel(self.general)
        self.lblDataType.setObjectName(u"lblDataType")
        self.lblDataType.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lblDataType, 0, 2, 1, 1)

        self.lineEditValue = QLineEdit(self.general)
        self.lineEditValue.setObjectName(u"lineEditValue")
        self.lineEditValue.setMinimumSize(QSize(0, 30))

        self.gridLayout_4.addWidget(self.lineEditValue, 0, 3, 1, 1)

        self.btnSend = QPushButton(self.general)
        self.btnSend.setObjectName(u"btnSend")
        self.btnSend.setMinimumSize(QSize(0, 35))

        self.gridLayout_4.addWidget(self.btnSend, 0, 4, 1, 1)

        self.tabWidget.addTab(self.general, "")
        self.alert = QWidget()
        self.alert.setObjectName(u"alert")
        self.tabWidget.addTab(self.alert, "")

        self.gridLayout_3.addWidget(self.tabWidget, 1, 0, 1, 1)

        PanelTool.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(PanelTool)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1076, 26))
        PanelTool.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(PanelTool)
        self.statusbar.setObjectName(u"statusbar")
        PanelTool.setStatusBar(self.statusbar)

        self.retranslateUi(PanelTool)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(PanelTool)
    # setupUi

    def retranslateUi(self, PanelTool):
        PanelTool.setWindowTitle(QCoreApplication.translate("PanelTool", u"PanelTool", None))
        self.groupBoxSettinigs.setTitle(QCoreApplication.translate("PanelTool", u"\u8bbe\u7f6e", None))
        self.lblPanelFilePath.setText(QCoreApplication.translate("PanelTool", u"\u9762\u677f\u6a21\u578b\u6587\u4ef6:", None))
        self.btnSelPanel.setText(QCoreApplication.translate("PanelTool", u"\u9009\u62e9\u6587\u4ef6", None))
        self.radioButtonNet.setText(QCoreApplication.translate("PanelTool", u"\u7f51\u7edc", None))
        self.cbAtConnector.setText(QCoreApplication.translate("PanelTool", u"@\u8fde\u63a5\u7b26", None))
        self.cbDoubleComaConnector.setText(QCoreApplication.translate("PanelTool", u"::\u8fde\u63a5\u7b26", None))
        self.lblBaseUrl.setText(QCoreApplication.translate("PanelTool", u"BaseUrl:", None))
        self.lblNetPort.setText(QCoreApplication.translate("PanelTool", u"\u7f51\u7edc\u7aef\u53e3\u53f7:", None))
        self.comboBoxNetPort.setItemText(0, QCoreApplication.translate("PanelTool", u"12019", None))
        self.comboBoxNetPort.setItemText(1, QCoreApplication.translate("PanelTool", u"12017", None))

        self.radioButtonSerial.setText(QCoreApplication.translate("PanelTool", u"\u4e32\u53e3", None))
        self.lblComPort.setText(QCoreApplication.translate("PanelTool", u"\u7aef\u53e3:", None))
        self.lblBaudrate.setText(QCoreApplication.translate("PanelTool", u"\u6ce2\u7279\u7387:", None))
        self.btnOpen.setText(QCoreApplication.translate("PanelTool", u"\u6253\u5f00", None))
        self.btnClose.setText(QCoreApplication.translate("PanelTool", u"\u5173\u95ed", None))
        self.comboBoxBaseUrl.setItemText(0, QCoreApplication.translate("PanelTool", u"http://127.0.0.1", None))

        self.lblFuncDesc.setText(QCoreApplication.translate("PanelTool", u"\u9650\u901f\u6807\u5fd7", None))
        self.lblSignalName.setText(QCoreApplication.translate("PanelTool", u"speed_limit_value", None))
        self.lblDataType.setText(QCoreApplication.translate("PanelTool", u"int", None))
        self.btnSend.setText(QCoreApplication.translate("PanelTool", u"send", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.general), QCoreApplication.translate("PanelTool", u"Tab 1", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.alert), QCoreApplication.translate("PanelTool", u"Tab 2", None))
    # retranslateUi

