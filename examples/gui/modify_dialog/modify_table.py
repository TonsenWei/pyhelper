# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/29 17:00
@File : modify_table.py
@Desc :
"""
from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QListView

from src.final_data import dat
from src.final_data.dat import CropType, ITECH_SET_VOLT, ITECH_SET_CURR
from src.myutils.log_util import logger
from src.mywidgets.combobox.combobox_sel import ComboBoxSel
from src.mywidgets.combobox.my_combobox import MyComboBox


class ModifyTable(QTableWidget):
    """
    QTableWidget，可以重写一些事件
    """

    def __init__(self, parent=None):
        QTableWidget.__init__(self, parent)
        self.currentStepType = "延时"
        HEADER_STEP = ['参数名称', '修改后的值']
        self.setColumnCount(len(HEADER_STEP))
        self.setHorizontalHeaderLabels(HEADER_STEP)
        # self.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许右键产生子菜单
        # self.customContextMenuRequested.connect(self.generate_table_menu)  # 右键菜单
        self.doubleClicked.connect(self.on_cell_double_clicked)
        # self.currentCellChanged.connect(self.on_current_changed)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        # self.verticalHeader().sectionClicked.connect(self.on_ver_header_clicked)  # 竖排表头单击信号
        # self.verticalHeader().sectionDoubleClicked.connect(self.on_ver_header_double_clicked)  # 竖排表头双击信号
        # self.tableWidget.horizontalHeader().sectionClicked.connect(self.HorSectionClicked)  # 横排表头单击信号
        # table_model = self.model()
        # table_model.dataChanged.connect(self.on_data_changed)  # 数据表改变则修改对应的任务和用例对象和文件的内容
        # self.clicked.connect(self.onClicked)
        # self.setColumnWidth(0, 60)
        self.horizontalHeader().setStretchLastSection(True)  # 设置表格最后一列自适应拉伸

        for i, perStr in enumerate(dat.HEADER_STEP[1:]):
            # item_content = perStep[dat.STEP_ITEM[i]]
            self.insertRow(i)
            item_table = QTableWidgetItem(perStr)
            # item_table_value = QTableWidgetItem(str(i))
            item_table_value = QTableWidgetItem("")
            self.setItem(i, 0, item_table)
            self.setItem(i, 1, item_table_value)
            item_table.setCheckState(Qt.Unchecked)

    def comboBoxTooltip(self, comboBox, titlesSet):
        """
        设置comboBox内容，并设置Tooltip
        :param comboBox: 要设置的ComboBox
        :param titlesSet: 选项列表
        :return:
        """
        model = QStandardItemModel(self)
        itemListView = QListView(self)
        for i, perTitle in enumerate(list(titlesSet)):
            item = QStandardItem(perTitle)
            item.setToolTip(perTitle)
            model.appendRow(item)
        comboBox.clear()
        comboBox.setView(itemListView)
        comboBox.setModel(model)

    def on_cell_double_clicked(self, item):
        """
        双击单元格进行编辑
        :param item:
        :return:
        """
        print("double ...")
        current_type = self.currentStepType
        self.old_type = str(item.data())  # 双击的单元格内容
        if self.old_type == "None":
            self.old_type = ""
        if item.row() == 0:  # 参数1, 返回键，HOME
            print("0 ...")
            self.para1_drop_select(current_type, item)
        elif item.row() == 1:  # 参数2,
            self.para2_drop_select(current_type, item)
        elif item.row() == 2:
            self.para3_drop_select(current_type, item)
        elif item.row() == 3:
            self.para4_drop_select(current_type, item)
        elif item.row() == 4:
            self.para5_drop_select(current_type, item)

    def para1_drop_select(self, current_type, item):
        """
        参数1下拉选择配置
        :param current_type: 当前步骤类型
        :param item: 当前双击的item
        :return:
        """
        row = item.row()
        col = 1
        if current_type.lower() == dat.STEP_TYPE_ANDROID.lower():  # Android步骤
            com_step_type = MyComboBox()
            com_step_type.setEditable(True)
            self.comboBoxTooltip(com_step_type, dat.ANDROID_PARAM1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_LOG_DETECT:  # 日志检测
            com_step_type = MyComboBox()
            self.comboBoxTooltip(com_step_type, dat.LOG_DETECT_PARA1)
            self.setCellWidget(row, col, com_step_type)
        elif current_type == dat.STEP_TYPE_CAMERA_DETECT:  # 摄像头
            com_step_type = MyComboBox()
            self.comboBoxTooltip(com_step_type, dat.IMAGE_DETECT_PARA1)
            self.setCellWidget(row, col, com_step_type)
        elif current_type == dat.STEP_TYPE_CAMERA_OCR or current_type == dat.STEP_TYPE_PC_APP_CATURE_OCR:  # 摄像头OCR
            com_step_type = MyComboBox()
            self.comboBoxTooltip(com_step_type, dat.OCR_PARA1)
            com_step_type.setCurrentText(self.old_type)
            self.setCellWidget(row, col, com_step_type)
        elif current_type == dat.STEP_TYPE_PC_APP_CATURE:
            com_step_type = MyComboBox()
            self.comboBoxTooltip(com_step_type, dat.IMAGE_DETECT_PARA1)
            self.setCellWidget(row, col, com_step_type)
        elif current_type == dat.STEP_TYPE_TS_CAN:  # TS_CAN  同星CAN工具
            if self.old_type == dat.PICK_FROM_DBC:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.TS_CAN_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_START_EXE:
            if self.old_type in dat.APP_PARA1:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.APP_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_STOP_EXE:
            if self.old_type in dat.APP_PARA1:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.APP_PARA1)
            # com_step_type.addItems(dat.APP_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_SIMU_SET:
            if self.old_type == dat.SIMU_PICK_FROM_XML or self.old_type == dat.INPUT_PARAMS:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SIMU_SET_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_SIMU_GET:
            if self.old_type == dat.SIMU_PICK_FROM_XML or self.old_type == dat.INPUT_PARAMS:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SIMU_GET_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_IT_POWER:  # IT程控电源
            com_step_type = MyComboBox()
            self.comboBoxTooltip(com_step_type, dat.ITECH_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_DELAY:  # 延时
            com_step_type = MyComboBox()
            if self.old_type == dat.TIMEOUT_DELAY[0]:
                com_step_type.setCurrentText("")
            self.comboBoxTooltip(com_step_type, dat.TIMEOUT_DELAY)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_CMD:  # 延时
            com_step_type = MyComboBox()
            self.comboBoxTooltip(com_step_type, ["", "输入CMD命令"])
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_SERIAL:
            if self.old_type in dat.SERIAL_PARA1:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SERIAL_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_NEPTUNE:
            # if self.old_type in dat.NEPTUNE_PARA1:
            #     self.old_type = ""
            para1 = self.item(row, col).setText("")
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.NEPTUNE_PARA1)
            self.setCellWidget(row, col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容

    def para2_drop_select(self, current_type, item):
        """
        参数2下拉选择配置
        :param current_type: 当前步骤类型
        :param item: 当前双击的item
        :return:
        """
        row = item.row()
        col = 1
        item_para1_text = ""  # 参数1内容
        if self.item(item.row(), 1) is not None:
            item_para1_text = self.item(1, 1).text()
        if current_type.lower() == dat.STEP_TYPE_ANDROID.lower():  # 参数2, 返回键，HOME
            com_step_type = MyComboBox()
            com_step_type.setEditable(True)
            self.comboBoxTooltip(com_step_type, ["输入控件或文字信息"])
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_CAMERA_DETECT:  # 摄像头
            com_step_type = ComboBoxSel()
            self.comboBoxTooltip(com_step_type, dat.CAMERA_DETECT_PARA2)
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_CAMERA_OCR:
            if self.old_type in dat.CAMERA_OCR_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel(actionType=CropType.AREA)
            self.comboBoxTooltip(com_step_type, dat.CAMERA_OCR_PARA2)
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_PC_APP_CATURE:
            if self.old_type in dat.IMAGE_DETECT_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel()
            self.comboBoxTooltip(com_step_type, dat.IMAGE_DETECT_PARA2)
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_PC_APP_CATURE_OCR:
            if self.old_type in dat.IMAGE_OCR_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel(actionType=CropType.AREA)
            self.comboBoxTooltip(com_step_type, dat.IMAGE_OCR_PARA2)
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_TS_CAN:  # TSCAN
            if item_para1_text == dat.TS_CAN_ACTIVE_MSG or item_para1_text == dat.TS_CAN_ACTIVE_MSG_CANCEL:
                com_step_type = ComboBoxSel(active=True)
                self.comboBoxTooltip(com_step_type, dat.TS_ACTIVE_PARA2)
                self.setCellWidget(item.row(), col, com_step_type)
                com_step_type.setCurrentText(self.old_type)
            else:
                com_step_type = ComboBoxSel()
                self.comboBoxTooltip(com_step_type, dat.TS_CAN_PARA2)
                self.setCellWidget(item.row(), col, com_step_type)
                com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_IT_POWER:  # IT电源
            current_action = self.item(item.row(), 1).text()  # 电源参数1，判断是设置电压还是电流
            com_step_type = MyComboBox()
            if current_action == ITECH_SET_VOLT:
                self.comboBoxTooltip(com_step_type, dat.ITECH_PARA2_VOLT)
            elif current_action == ITECH_SET_CURR:
                self.comboBoxTooltip(com_step_type, dat.ITECH_PARA2_CURR)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_START_EXE:
            if self.old_type in dat.APP_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.APP_PARA2)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_STOP_EXE:
            if self.old_type == dat.APP_INPUT_TITLE_NAME:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.APP_PARA2)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_SIMU_SET:
            if self.old_type == dat.INPUT_VALUE:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SIMU_SET_GET_PARA2)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_SIMU_GET:
            if self.old_type == dat.INPUT_VALUE:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SIMU_SET_GET_PARA2)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_SERIAL:
            if self.old_type in dat.SERIAL_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SERIAL_PARA2)
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容
        elif current_type == dat.STEP_TYPE_NEPTUNE:
            if self.old_type == "编辑参数":
                self.old_type = ""
            com_step_type = ComboBoxSel(preview_text=self.old_type, actionType=item_para1_text)
            self.comboBoxTooltip(com_step_type, [self.old_type, "编辑参数"])
            self.setCellWidget(item.row(), col, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容

    def timeoutEditor(self, item):
        """
        超时时间编辑
        :param item:
        :return:
        """
        com_step_type = MyComboBox()
        com_step_type.setEditable(True)
        self.comboBoxTooltip(com_step_type, dat.TIMEOUT_PARA3)  # 设置带提示的comboBox
        self.setCellWidget(item.row(), self.valueColumn, com_step_type)
        com_step_type.setCurrentText(self.old_type)

    def para3_drop_select(self, current_type, item):
        """
        参数3, 超时时间
        :param current_type:
        :param item:
        :return:
        """
        if current_type == dat.STEP_TYPE_CAMERA_DETECT:
            self.timeoutEditor(item)
        elif current_type == dat.STEP_TYPE_ANDROID:
            self.timeoutEditor(item)
        elif current_type == dat.STEP_TYPE_PC_APP_CATURE:
            self.timeoutEditor(item)
        elif current_type == dat.STEP_TYPE_CAMERA_OCR:
            self.timeoutEditor(item)
        elif current_type == dat.STEP_TYPE_PC_APP_CATURE_OCR:
            self.timeoutEditor(item)
        elif current_type == dat.STEP_TYPE_SERIAL:
            self.timeoutEditor(item)

    def para4_drop_select(self, current_type, item):
        """
        参数4，测试配置
        :param current_type:
        :param item:
        :return:
        """
        if current_type.lower() == dat.STEP_TYPE_CAMERA_DETECT.lower():
            com_step_type = MyComboBox()
            com_step_type.setEditable(True)
            self.comboBoxTooltip(com_step_type, dat.IMAGE_PARA4)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), self.valueColumn, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type.lower() == dat.STEP_TYPE_PC_APP_CATURE.lower():
            com_step_type = MyComboBox()
            com_step_type.setEditable(True)
            self.comboBoxTooltip(com_step_type, dat.IMAGE_PARA4)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), self.valueColumn, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_SIMU_SET or current_type == dat.STEP_TYPE_SIMU_GET:
            com_step_type = MyComboBox()
            com_step_type.setEditable(True)
            self.comboBoxTooltip(com_step_type, dat.SIMU_PARA4_BASEURL)  # 设置带提示的comboBox
            self.setCellWidget(item.row(), self.valueColumn, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_SERIAL:
            com_step_type = ComboBoxSel(preview_text=self.old_type)
            self.comboBoxTooltip(com_step_type, dat.SERIAL_PARA4)
            self.setCellWidget(item.row(), self.valueColumn, com_step_type)
            com_step_type.setCurrentText(self.old_type)  # 双击编辑的时候，如果表格原来有内容，则默认显示原有内容

    def para5_drop_select(self, current_type, item):
        """
        参数5，设备选择
        :param current_type:
        :param item:
        :return:
        """
        if current_type == dat.STEP_TYPE_CAMERA_DETECT:
            if self.old_type in dat.CAMERA_OCR_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel(actionType=CropType.AREA)
            self.comboBoxTooltip(com_step_type, dat.CAMERA_OCR_PARA2)
            self.setCellWidget(item.row(), self.valueColumn, com_step_type)
            com_step_type.setCurrentText(self.old_type)
        elif current_type == dat.STEP_TYPE_PC_APP_CATURE:
            if self.old_type in dat.IMAGE_OCR_PARA2:
                self.old_type = ""
            com_step_type = ComboBoxSel(actionType=CropType.AREA)
            self.comboBoxTooltip(com_step_type, dat.IMAGE_OCR_PARA2)
            self.setCellWidget(item.row(), self.valueColumn, com_step_type)
            com_step_type.setCurrentText(self.old_type)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:  # 左键按下
            modelIndex = self.indexAt(event.pos())
            if modelIndex.isValid() is False:
                self.setCurrentIndex(modelIndex)  # 设置不选中,会自动完成当前编辑
        super(ModifyTable, self).mousePressEvent(event)  # 不中断父类事件的处理
