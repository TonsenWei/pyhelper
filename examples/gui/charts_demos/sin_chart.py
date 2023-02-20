# -*- coding: utf-8 -*-
"""
@Author : WeiDongcheng @tonse
@Time : 2022/11/25 17:27
@File : sin_chart.py
@Desc : pip install PyQtChart
"""
import json
import time

import numpy as np
import sys

from PyQt5.Qt import *
from dym_plot_qchart import Ui_MainWindow
from PyQt5.QtChart import QChart, QValueAxis, QChartView, QSplineSeries


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, app):
        super(QMainWindow, self).__init__()
        self.app = app
        self.setup_ui()  # 渲染画布
        self.update_data_thread = UpdateDataThread()  # 创建更新波形数据线程
        self.connect_signals()  # 绑定触发事件

    def setup_ui(self):
        self.setupUi(self)  # 调用Ui_MainWindow的setupUi渲染界面

        # 加载Qchart波形界面
        self.plot_qchart = QChartViewPlot()
        self.plot_view.setChart(self.plot_qchart)
        self.plot_view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.plot_view.setRubberBand(QChartView.RectangleRubberBand)

    def connect_signals(self):
        # 绑定触发事件
        self.btn_start.clicked.connect(self.btn_start_clicked)  # 按钮点击后，启动生成数据线程
        # 初始化线程中的信号，线程生成数据并发送信号，触发update_data_thread_slot更新显示
        self.update_data_thread._signal_update.connect(self.update_data_thread_slot)

    def btn_start_clicked(self):
        # 开启按钮
        self.update_data_thread.start()

    def update_data_thread_slot(self, data):
        # 线程回调函数
        data = json.loads(data)
        self.plot_qchart.handle_update(data['sin_data'])

    def wheelEvent(self, event):
        # 鼠标滚轮:缩放Qchart波形
        if event.angleDelta().y() >= 0:
            #  鼠标滚轮向上
            if event.x() < (
                    self.plot_view.width() + self.plot_view.x()) and event.x() > self.plot_view.x():
                if event.y() < (
                        self.plot_view.height() + self.plot_view.y()) and event.y() > self.plot_view.y():
                    self.plot_qchart.zoomIn()
        else:
            #  鼠标滚轮向下
            if event.x() < (
                    self.plot_view.width() + self.plot_view.x()) and event.x() > self.plot_view.x():
                if event.y() < (
                        self.plot_view.height() + self.plot_view.y()) and event.y() > self.plot_view.y():
                    self.plot_qchart.zoomOut()


# 波形显示
class QChartViewPlot(QChart):
    # 相位振动波形
    def __init__(self, parent=None):
        super(QChartViewPlot, self).__init__(parent)
        self.window = parent
        self.xRange = 1024
        self.counter = 0
        self.seriesList = []
        self.legend().show()

        self.axisX = QValueAxis()
        self.axisX.setRange(0, self.xRange)
        self.addAxis(self.axisX, Qt.AlignBottom)
        # self.setAxisX(self.axisX, series)
        self.y_min = 0
        self.y_max = 100
        self.axisY = QValueAxis()
        self.axisY.setRange(self.y_min, self.y_max)
        self.addAxis(self.axisY, Qt.AlignLeft)
        # self.setAxisY(self.axisY, series)

        self.series = QSplineSeries()
        self.series.setName("波形")
        self.series.setUseOpenGL(True)
        self.addSeries(self.series)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

    def handle_update(self, ydata):
        # 更新y值
        if self.counter < self.xRange:
            self.series.append(self.counter, ydata)
            self.counter += 1
        else:
            points = self.series.pointsVector()
            for i in range(self.xRange - 1):
                points[i].setY(points[i + 1].y())
            points[-1].setY(ydata)
            self.y_min = min(points, key=lambda point: point.y()).y()
            self.y_max = max(points, key=lambda point: point.y()).y()
            self.series.replace(points)
            self.axisY.setRange(self.y_min - 20, self.y_max + 20)


# 使用线程不断更新波形数据
class UpdateDataThread(QThread):
    _signal_update = pyqtSignal(str)  # 信号

    def __init__(self, parent=None):
        super(UpdateDataThread, self).__init__(parent)
        self.qmut = QMutex()  # 互斥锁
        self.is_exit = False
        self.x_range = 1024
        self.sin = Sin()

    def run(self):
        while True:
            self.qmut.lock()
            if self.is_exit:
                break
            self.qmut.unlock()
            for i in range(self.x_range):
                self._signal_update.emit(json.dumps({'sin_data': self.sin.get_data(i)}))  # 发送信号给槽函数
                time.sleep(0.01)

        self.qmut.unlock()


class Sin():
    # 创建一个正弦波数据
    def __init__(self, pha=0):
        self.pha = pha  # 初始相位

    def get_data(self, index):
        self.pha += 10
        if self.pha > 1000:
            self.pha = 0
        return 1000 * np.sin(8 * np.pi * index + self.pha * np.pi / 180.0)


def main():
    app = QApplication(sys.argv)
    mywindow = Window(app)
    mywindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
