# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2023/1/10 15:29
@File : led.py
@Desc : 按钮模拟LED闪烁
"""
import threading
import time

from PyQt5.Qt import *


class QtSignals(QObject):
    sigLedOnOff = pyqtSignal(bool)


MY_SIGNAL = QtSignals()


class ShowHideThread(threading.Thread):

    def __init__(self, highTime=0.1, lowTime=0.9):
        threading.Thread.__init__(self)
        self.highTime = highTime
        self.lowTime = lowTime
        self.keepRun = True

    def run(self):
        startTime = time.time()
        highOn = True
        while self.keepRun is True:
            if highOn is True:
                if time.time() - startTime >= self.highTime:  # 显示时间结束
                    MY_SIGNAL.sigLedOnOff.emit(False)
                    highOn = False
                    startTime = time.time()
                # else:
                #     time.sleep(0.01)
            else:
                if time.time() - startTime >= self.lowTime:  # 隐藏时间结束
                    MY_SIGNAL.sigLedOnOff.emit(True)
                    highOn = True
                    startTime = time.time()
                # else:
                #     time.sleep(0.01)
        MY_SIGNAL.sigLedOnOff.emit(True)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("layout的学习")
        self.resize(500, 500)
        self.setup_ui()
        self.flag = True
        self.delayTime = 500
        self.flashThread = None

    def setup_ui(self):
        label1 = QLabel()
        label2 = QLabel()
        label3 = QLabel()
        self.freqLine = QLineEdit()
        self.dutyLine = QLineEdit()
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3

        btn1 = QPushButton('开启')
        btnClose = QPushButton('关闭')

        gl = QFormLayout()
        self.setLayout(gl)

        gl.addRow(QLabel("图标亮的时间(秒)"), self.freqLine)
        gl.addRow(QLabel("图标灭的时间(秒)"), self.dutyLine)
        self.freqLine.setText("0.5")
        self.dutyLine.setText("0.5")
        gl.addRow(label1, btn1)
        gl.addRow(label1, btnClose)
        gl.addRow(label2, )
        gl.addRow(label3)
        # gl.setSpacing(50)
        label1.resize(100, 100)
        label1.setPicture(self.pic())
        label3.setPicture(self.pic(color='yellow'))
        # btn1.clicked.connect(self.time_start)
        btn1.clicked.connect(self.startThread)
        btnClose.clicked.connect(self.stopThread)
        label1.hide()
        label3.hide()
        MY_SIGNAL.sigLedOnOff.connect(self.flash)
        # self.label2.setPicture(self.pic(color='red'))
        pixPic = QPixmap(r"C:\Users\tonse\Pictures\std\p.png")
        self.label2.setPixmap(pixPic)
        self.label2.update()

    def startThread(self):
        print("start thread")
        freq = float(self.freqLine.text())
        duty = float(self.dutyLine.text())
        if self.flashThread is not None:
            self.flashThread.keepRun = False
            time.sleep(1)
        self.flashThread = ShowHideThread(freq, duty)
        self.flashThread.setDaemon(True)
        self.flashThread.start()

    def stopThread(self):
        if self.flashThread is not None:
            self.flashThread.keepRun = False

    def time_start(self):
        timer = QTimer(self)
        timer.timeout.connect(self.cao)
        timer.start(500)

    def cao(self):
        if self.flag:
            self.label2.setPicture(self.pic(color='red'))
            self.flag = False
            self.label2.show()
        else:
            self.label2.setPicture(self.pic(color='green'))
            self.flag = True
            self.label2.hide()

    def flash(self, onOff):
        if onOff is True:
            self.label2.show()
        else:
            self.label2.hide()

    def pic(self, color='green'):
        m = QPicture()
        painter = QPainter(m)
        brush = QBrush(QColor(color))
        painter.setBrush(brush)
        painter.drawEllipse(0, 0, 50, 50)
        return m


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
