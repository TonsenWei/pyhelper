# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/2/22 18:14
@File : main_get_meter_tmp.py
@Desc : 
"""
import sys

from PySide2.QtWidgets import QApplication, QWidget

from examples.gui.meter_gui.get_meter_tmp_gui import Ui_meterSampleGui


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.meterGui = Ui_meterSampleGui()
        self.meterGui.setupUi(self)
        self.initSignal()

    def initSignal(self):
        pass
        # self.meterGui.btnSetValue.clicked.connect(self.setValue)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MainWidget()
    # demo = Ui_meterGui()
    # demo.setupUi(widget)
    # gridLy = QGridLayout(demo.widget)
    # meterWidget = Dashboard()
    # gridLy.addWidget(meterWidget)
    widget.show()
    # demo.setValue(55)  # 设置指针指向
    # demo.setTitle("疲劳指数")  # 设置图标题
    sys.exit(app.exec_())
