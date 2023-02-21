# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/5 10:24
@File : main_color_dialog.py
@Desc : 
"""

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QColorDialogDemo(QWidget):
    def __init__(self):
        super(QColorDialogDemo, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Color Dialog 例子')
        layout = QVBoxLayout()
        self.colorButton = QPushButton('设置颜色')
        self.colorButton.clicked.connect(self.getColor)
        layout.addWidget(self.colorButton)

        self.colorButton1 = QPushButton('设置背景颜色')
        self.colorButton1.clicked.connect(self.getBGColor)
        layout.addWidget(self.colorButton1)

        self.colorLabel = QLabel('Hello, 测试颜色例子')
        layout.addWidget(self.colorLabel)

        self.setLayout(layout)

    def getColor(self):
        color = QColorDialog.getColor()  # PyQt5.QtGui.QColor
        mCol = QColor(color.name())
        print(f"mCol.name() = {mCol.name()}")
        print(f"color.name() = {color.name()}")
        p = QPalette()
        # p.setColor(QPalette.WindowText, color)
        p.setColor(QPalette.WindowText, mCol)
        self.colorLabel.setPalette(p)

    def getBGColor(self):
        color = QColorDialog.getColor()
        p = QPalette()
        p.setColor(QPalette.Window, color)
        self.colorLabel.setAutoFillBackground(True)
        self.colorLabel.setPalette(p)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = QColorDialogDemo()
    main.show()
    sys.exit(app.exec_())
