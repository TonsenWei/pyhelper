# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/29 11:51
@File : my_app.py
@Desc : 
"""
import os
import sys
import threading

from PySide2 import QtCore
from PySide2.QtCore import Qt, Signal, QSettings, QRect
from PySide2.QtWidgets import QMainWindow, QComboBox, QWidget, QGridLayout, QScrollArea, QSizePolicy, QSpacerItem, \
    QMessageBox, QFileDialog, QApplication, QLabel, QMenuBar, QMenu, QAction, QStatusBar
from bs4 import BeautifulSoup

from src.my_line_widget import MyLineWidget
from src.myutils.excel_util import ExcelUtil
from src.myutils.simu import SIMU
from src.qt_signals import MY_SIGNALS
from src.test_panel import Ui_PanelTool

APP_VERSION = "1.0.3"
VERSION_DATE = "2023-01-03_01"
VERSION_INFO = f"版本：V{APP_VERSION} \n日期：{VERSION_DATE}" \
               f"\n有问题或建议请联系：怿星科技STD部门 胡建忠\nEmail: hujianzhong@eptcom.com"

workspace_dir = os.path.dirname(os.path.realpath(sys.argv[0]))  # 软件根目录
CURRENT_SETTINGS_FILE = f"{workspace_dir}{os.path.sep}settings.ini"
CURRENT_INI_SETTING = QSettings(CURRENT_SETTINGS_FILE, QSettings.IniFormat)

NODE_DATASOURCE = "datasource"
NODE_DATAGROUP = "datagroup"
NODE_SOURCE = "source"
ATTR_NAME = "name"
ATTR_TYPE = "type"
ATTR_VALUE = "value"
qssStyle = '''
        QWidget:hover {
            background-color: lightgreen;
        }
        '''


class V3Xml:

    def __init__(self):
        self.xmlPath = ""
        self.xml_tree = None

    def load(self, xmlPath):
        self.xmlPath = xmlPath
        content_str = ""  # 字符串保存xml内容
        with open(self.xmlPath, "r", encoding="utf8") as f:  # 返回一个文件对象,这里打开masterxml
            line = f.readline()  # 调用readline，一次读一行
            content_str = content_str + line
            while line:
                line = f.readline()
                content_str += line
        self.xml_tree = BeautifulSoup(content_str, "lxml-xml")  # 字符串读取为bs4的xml对象
        return self.xml_tree

    def getDataSrcNames(self):
        dataSrcsStrs = []
        if self.xml_tree:
            dataSrcs = self.xml_tree.findAll(NODE_DATASOURCE)
            for i, item in enumerate(dataSrcs):
                try:
                    name = item[ATTR_NAME]
                    dataSrcsStrs.append(name)
                except Exception as e:
                    pass
        return dataSrcsStrs

    def getDataGrpNames(self, dataSrcName):
        dataGroupsStrs = []
        if self.xml_tree:
            dataSrcs = self.xml_tree.findAll(NODE_DATASOURCE)
            for i, itemDataSrc in enumerate(dataSrcs):
                try:
                    name = itemDataSrc[ATTR_NAME]
                    if name == dataSrcName:
                        targetDataGroups = itemDataSrc.findAll(NODE_DATAGROUP)
                        for dgIndex, itemDataGroup in enumerate(targetDataGroups):
                            dataGrpName = itemDataGroup[ATTR_NAME]
                            dataGroupsStrs.append(dataGrpName)
                        # break
                except Exception as e:
                    pass
        return dataGroupsStrs

    def getSourceNames(self, dataSrcName, targetDataGrpName):
        srcNames = []
        if self.xml_tree:
            dataSrcs = self.xml_tree.findAll(NODE_DATASOURCE)
            for i, itemDataSrc in enumerate(dataSrcs):
                try:
                    name = itemDataSrc[ATTR_NAME]
                    if name == dataSrcName:
                        targetDataGroups = itemDataSrc.findAll(NODE_DATAGROUP)
                        for dgIndex, itemDataGroup in enumerate(targetDataGroups):
                            dataGrpName = itemDataGroup[ATTR_NAME]
                            if dataGrpName == targetDataGrpName:
                                targetSrc = itemDataGroup.findAll(NODE_SOURCE)
                                for srcIndex, itemSrc in enumerate(targetSrc):
                                    targetSrcName = itemSrc[ATTR_NAME]
                                    srcNames.append(targetSrcName)
                except Exception as e:
                    pass
        return srcNames


class MyApp(QMainWindow):
    sigLoadPanel = Signal(str, str, object)
    SETTINGS_PANEL_PATH = "Panel/PanelFilePath"

    def __init__(self):
        super(MyApp, self).__init__()

        self.form = Ui_PanelTool()
        self.form.setupUi(self)
        # self.setStyleSheet(''' font-size: 25px; ''')
        self.form.radioButtonNet.setChecked(True)
        # form.radioButtonNet.setCheckState(Qt.Checked)
        self.form.cbDoubleComaConnector.setCheckState(Qt.Checked)
        self.form.cbDoubleComaConnector.stateChanged.connect(self.onDoubleComaConnectStateChanged)
        self.form.cbAtConnector.stateChanged.connect(self.onCbAtConnectorStateChanged)
        fileList = MyApp.get_files_path_list(workspace_dir, ".xlsx")
        xmlList = MyApp.get_files_path_list(workspace_dir, ".xml")
        self.form.comboBoxPanelPath.addItem("")
        self.form.comboBoxPanelPath.addItems(fileList)
        self.form.comboBoxPanelPath.addItems(xmlList)
        panelPathDefault = CURRENT_INI_SETTING.value(self.SETTINGS_PANEL_PATH, "", str)
        if os.path.exists(panelPathDefault) is True:
            self.form.comboBoxPanelPath.setCurrentText(panelPathDefault)
        else:
            self.form.comboBoxPanelPath.setCurrentText("")
        self.form.btnSelPanel.clicked.connect(self.onSelPanelFile)
        self.form.comboBoxPanelPath.currentIndexChanged.connect(self.onPanelSelChanged)
        self.onPanelSelChanged()

        # 获取显示器分辨率
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.screenheight = self.screenRect.height()
        self.screenwidth = self.screenRect.width()
        self.height = int(self.screenheight * 0.8)  # 显示区域为屏幕大小的0.8
        self.width = int(self.screenwidth * 0.8)
        # self.height = int(self.screenheight)
        # self.width = int(self.screenwidth)
        self.resize(self.width, self.height)

        tabCounter = self.form.tabWidget.count()
        for i in range(tabCounter):
            self.form.tabWidget.removeTab(0)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 870, 22))
        self.menuHelp = QMenu(self.menubar)  # 帮助菜单加入到menubar
        self.menubar.setObjectName(u"menubar")
        self.menuHelp.setObjectName(u"menuHelp")
        self.actionAbout = QAction(self)
        self.actionAbout.setText("关于")
        self.menuHelp.addAction(self.actionAbout)
        self.actionAbout.triggered.connect(self.on_action_about)
        self.menuHelp.setTitle("帮助")
        self.setMenuBar(self.menubar)
        self.menubar.addAction(self.menuHelp.menuAction())

        # status bar
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)
        self.initSignal()

    def initSignal(self):
        MY_SIGNALS.sigEnterSend.connect(self.send)
        MY_SIGNALS.sigUpdateSendAddr.connect(self.updateStatuBarContent)

    def updateStatuBarContent(self, res, addr):
        self.statusbar.showMessage(f"{res}, {addr}", timeout=300000)

    def send(self, sigName, dataType, value):
        self.sendTestCmd(sigName, dataType, value)

    def onClickButton(self, object):
        sender = self.sender()
        sigNameObj = self.findChild(QLabel, f"lblSigName_{sender.objectName()}")
        dataTypeObj = self.findChild(QLabel, f"lblDataType_{sender.objectName()}")
        valueObj = self.findChild(QComboBox, f"combobox_{sender.objectName()}")
        sigName = sigNameObj.text()
        dataType = dataTypeObj.text()
        value = valueObj.currentText()
        self.sendTestCmd(sigName, dataType, value)

    def sendTestCmd(self, sigName, dataType, value):
        if self.form.radioButtonNet.isChecked() is True:  # 网络发送
            tabIndex = self.form.tabWidget.currentIndex()
            tabName = self.form.tabWidget.tabText(tabIndex)
            sConnector = "::"
            if self.form.cbAtConnector.checkState() == Qt.Checked:
                sConnector = "@"
            baseUrl = self.form.comboBoxBaseUrl.currentText()
            netPort = self.form.comboBoxNetPort.currentText()
            SIMU.sConnector = sConnector
            SIMU.baseUrl = baseUrl
            SIMU.port = netPort

            setUrl = f"{baseUrl}:{netPort}/simu?"
            paramsSent = {"name": f"{tabName}{sConnector}{sigName}", "type": dataType, "value": value}
            addr = f"{setUrl}/{paramsSent}"
            MY_SIGNALS.sigUpdateSendAddr.emit("正在发送...  ", f"发送地址:{addr}")
            th = threading.Thread(target=SIMU.set, args=[[tabName, sigName, dataType, value]])
            th.setDaemon(True)
            th.start()
            # SIMU.set([tabName, sigName, dataType, value])
        else:
            pass

    def onSelPanelFile(self):
        filepath, fileType = QFileDialog.getOpenFileName(self, "选择面板数据文件", "",
                                                         "xlsx (*.xlsx);; xml (*.xml);")
        if filepath is not None and os.path.exists(filepath):
            self.form.comboBoxPanelPath.setCurrentText(filepath)
            self.onPanelSelChanged()

    def updatePanel(self, panelDataList, fileFmt):
        tabCounter = self.form.tabWidget.count()
        for i in range(tabCounter):
            self.form.tabWidget.removeTab(0)
        if fileFmt == "xml":
            if panelDataList is not None:
                allDataList = []
                dataSrcs = panelDataList.findAll(NODE_DATASOURCE)
                for i, itemDataSrc in enumerate(dataSrcs):
                    try:
                        name = itemDataSrc[ATTR_NAME]
                        targetDataGroups = itemDataSrc.findAll(NODE_DATAGROUP)
                        for dgIndex, itemDataGroup in enumerate(targetDataGroups):
                            dataList = []
                            dataGrpName = itemDataGroup[ATTR_NAME]
                            targetSrc = itemDataGroup.findAll(NODE_SOURCE)
                            for srcIndex, itemSrc in enumerate(targetSrc):
                                targetSrcName = itemSrc[ATTR_NAME]
                                dataList.append({"funcName": targetSrcName,
                                                 "sigName": targetSrcName,
                                                 "sigDesc": targetSrcName,
                                                 "dataType": itemSrc[ATTR_TYPE]})
                            allData = {"sheetname": dataGrpName, "dataList": dataList}
                            allDataList.append(allData)
                    except Exception as e:
                        pass
                panelDataList = allDataList
        for i, panel in enumerate(panelDataList):
            sheetName = panel["sheetname"]  # [{"sheetname":"adas", "dataList":[]}]
            dataList = panel["dataList"]

            contentWidget = QWidget()  # tab中的面板
            contentWidget.setObjectName(f"{sheetName}")
            gridlayout = QGridLayout(contentWidget)
            gridlayout.setObjectName(f"gridLayout_{sheetName}")

            scrollArea = QScrollArea(contentWidget)  # 滚动部件放到QWidget
            scrollArea.setMinimumSize(QtCore.QSize(10, 10))
            scrollArea.setWidgetResizable(True)
            scrollArea.setObjectName("scrollArea")

            scrollAreaWidgetContents = QWidget()
            scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

            gridLayoutScroll = QGridLayout(scrollAreaWidgetContents)
            gridLayoutScroll.setObjectName(f"scrollGl_{sheetName}")
            gridLayoutScroll.setContentsMargins(10, 10, 10, 10)
            gridLayoutScroll.setVerticalSpacing(0)

            for lineCounter, lineData in enumerate(dataList):
                funcName = lineData["funcName"]
                sigName = lineData["sigName"]
                sigDesc = lineData["sigDesc"]
                dataType = lineData["dataType"]

                lineWidgetOut = QWidget(scrollAreaWidgetContents)  # 每行数据
                lineWidgetOut.setObjectName("lineWidgetOut")
                gridLayoutOut = QGridLayout(lineWidgetOut)
                gridLayoutOut.setObjectName(f"gridLayoutOut_{sheetName}")
                gridLayoutOut.setContentsMargins(0, 0, 0, 0)
                gridLayoutOut.setVerticalSpacing(0)

                lineWidget = MyLineWidget(lineWidgetOut)  # 每行数据
                lineWidgetOut.setStyleSheet(qssStyle)
                lineWidget.setObjectName(f"{funcName}")
                # lineWidget.setMinimumHeight(30)
                # lineUi = Ui_Form()
                # lineUi.setupUi(lineWidget)
                # lineWidget.setStyleSheet(qssStyle)

                lineWidget.lblFuncName.setText(funcName)
                lineWidget.lblFuncName.setToolTip(sigDesc)
                lineWidget.lblSigName.setText(sigName)
                lineWidget.lblDataType.setText(dataType)
                lineWidget.comboBoxInput.setToolTip(sigDesc)
                lineWidget.btnSend.setToolTip(sigDesc)
                lineWidget.btnSend.setObjectName(f"btnSend_{sheetName}_{lineCounter}")
                lineWidget.comboBoxInput.setObjectName(f"combobox_btnSend_{sheetName}_{lineCounter}")
                lineWidget.lblSigName.setObjectName(f"lblSigName_btnSend_{sheetName}_{lineCounter}")
                lineWidget.lblDataType.setObjectName(f"lblDataType_btnSend_{sheetName}_{lineCounter}")
                if dataType == "bool" or dataType == "float" or dataType == "int":
                    lineWidget.comboBoxInput.addItems(["", "0", "1"])
                # print(lineUi.comboBoxInput.objectName())
                gridLayoutOut.addWidget(lineWidget, 0, 0, 1, 1)
                gridLayoutScroll.addWidget(lineWidgetOut, lineCounter, 0, 1, 1)
                lineWidget.btnSend.clicked.connect(self.onClickButton)

            verticalSpacer = QSpacerItem(20, 85, QSizePolicy.Minimum, QSizePolicy.Expanding)
            gridLayoutScroll.addItem(verticalSpacer)

            scrollArea.setWidget(scrollAreaWidgetContents)
            gridlayout.addWidget(scrollArea, 0, 0, 1, 1)
            gridlayout.setContentsMargins(0, 0, 0, 0)
            self.form.tabWidget.addTab(contentWidget, sheetName)

    def loadFromXlsx(self, path):
        if path.endswith(".xml"):
            xmlObject = V3Xml()
            xmlTree = xmlObject.load(path)
            self.sigLoadPanel.emit("101", "", xmlTree)
        else:
            panelData = ExcelUtil.getPanelData(path)
            if len(panelData) == 0:
                self.sigLoadPanel.emit("error", "解析不到数据", None)
            else:
                self.sigLoadPanel.emit("100", "", panelData)

    def onPanelSelChanged(self):
        path = self.form.comboBoxPanelPath.currentText()
        if os.path.exists(path) is True:
            CURRENT_INI_SETTING.setValue(self.SETTINGS_PANEL_PATH, path)

            def loadPanelData(code, msg, panelData):
                if code == "100":
                    self.updatePanel(panelData, "xlsx")
                elif code == "101":
                    self.updatePanel(panelData, "xml")
                else:
                    QMessageBox.critical(self, '加载失败', code + ': ' + msg,
                                         QMessageBox.Yes, QMessageBox.Yes)
                self.sigLoadPanel.disconnect(loadPanelData)

            self.sigLoadPanel.connect(loadPanelData)
            th = threading.Thread(target=self.loadFromXlsx, args=[path])
            th.setDaemon(True)
            th.start()

    def onDoubleComaConnectStateChanged(self, state):
        if state == Qt.Checked:
            self.form.cbAtConnector.setChecked(False)
        else:
            self.form.cbAtConnector.setChecked(True)

    def onCbAtConnectorStateChanged(self, state):
        if state == Qt.Checked:
            self.form.cbDoubleComaConnector.setChecked(False)
        else:
            self.form.cbDoubleComaConnector.setChecked(True)

    @staticmethod
    def get_files_path_list(dir_path, suffix=""):
        """
        获取某个目录下所有后缀为 suffix 的文件的路径
        FileUtil.get_files_path_list(r"D:\Projects\gitee\pylearning\files\wav_report", ".wav")
        :param dir_path: 查找文件所在目录
        :param suffix: 后缀名，如 .wav， 如果为空则匹配所有文件
        :return: 文件路径列表
        """
        info_list = []
        for i, j, k in os.walk(dir_path):
            for file in k:
                if suffix is not None and suffix != "":
                    if file.endswith(suffix):
                        info_list.append(os.path.join(i, file))
                else:
                    info_list.append(os.path.join(i, file))
        return info_list

    def on_action_about(self):
        QMessageBox.information(
            self,
            '关于',
            VERSION_INFO)
