# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/12/2 13:57
@File : highlight.py
@Desc : 
"""
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTextEdit, QVBoxLayout,
                             QPushButton)
def revise():
    html = ' '.join(('<p>This is', mark[mode], 'text with HTML</p>'))
    edit.setHtml(html)

def button_clicked():
    global mode
    mode = 1 - mode
    revise()

mode = 0
mark = ['not-highlight','<b>highlight</b>']

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

ui = QWidget()
ui.setWindowTitle('Example')
ui.resize(300, 100)

edit = QTextEdit()
button = QPushButton('Highlight')

layout = QVBoxLayout()
layout.addWidget(edit)
layout.addWidget(button)
ui.setLayout(layout)
button.clicked.connect(button_clicked)

revise()
ui.show()
sys.exit(app.exec_())