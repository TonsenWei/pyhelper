# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/28 17:53
@File : main_panel.py
@Desc : 
"""
import sys

from PySide2.QtWidgets import QApplication

from src.my_app import MyApp, APP_VERSION, VERSION_DATE
from src.myutils.log_util import logger


if __name__ == "__main__":
    app = QApplication([])
    main_win = MyApp()
    # main_win.statusBar().hide()
    logger.info(f"Version: {APP_VERSION}, date: {VERSION_DATE}")
    main_win.show()
    sys.exit(app.exec_())
