# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/16 10:27
@File : main_params_dialog.py
@Desc : 
"""
import sys

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QTableWidgetItem

from examples.gui.params_dialog.params_dialog import Ui_Dialog
from src.myutils.log_util import logger


if __name__ == "__main__":
    app = QApplication([])
    main_win = QDialog()
    main_win.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
    # main_win.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinMaxButtonsHint)
    form = Ui_Dialog()
    form.setupUi(main_win)
    # HEADER_STEP = ['参数名', '参数值']
    # form.treeViewParams.setColumnCount(len(HEADER_STEP))
    # form.treeViewParams.setHorizontalHeaderLabels(HEADER_STEP)

    # main_win.statusBar().hide()
    # logger.info(f"Version: {APP_VERSION}, date: {VERSION_DATE}")
    main_win.show()
    sys.exit(app.exec_())
