# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/1 14:55
@File : serial_main.py
@Desc : pip install pyside2 -i https://pypi.douban.com/simple/
"""
import sys

from PySide2.QtWidgets import QApplication, QWidget

from examples.gui.serial_gui.serial_gui_use001 import Ui_MainForm

if __name__ == "__main__":
    app = QApplication([])
    main_win = QWidget()
    form = Ui_MainForm()
    form.setupUi(main_win)
    main_win.show()
    sys.exit(app.exec_())
