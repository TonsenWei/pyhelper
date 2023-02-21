import time

from PySide6.QtWidgets import QApplication, QTextBrowser
from PySide6.QtUiTools import QUiLoader
from threading import Thread

from PySide6.QtCore import Signal, QObject, Slot


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串(pyside6参数不能是qt控件，QTextBrowser已经不能在这里传了！)
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(str)

    # 还可以定义其他种类的信号
    update_table = Signal(int)


# 实例化
global_ms = MySignals()


class Stats:

    def __init__(self):
        self.ui = QUiLoader().load('main.ui')

        # 自定义信号的处理函数
        global_ms.text_print.connect(self.printToGui)
        self.ui.btnStartTask1.clicked.connect(self.task1)
        # self.task1()
        # self.task2()

    @Slot(str)
    def printToGui(self, text):
        self.ui.infoBox1.append(text)
        self.ui.infoBox1.ensureCursorVisible()

    # @Slot
    def task1(self):
        print("clicked")
        def threadFunc():
            # 通过Signal 的 emit 触发执行 主线程里面的处理函数
            # emit参数和定义Signal的数量、类型必须一致
            counter = 0
            while counter < 50:
                counter = counter + 1
                global_ms.text_print.emit('输出内容:' + str(counter))
                time.sleep(1)

        thread = Thread(target=threadFunc)
        thread.setDaemon(True)
        thread.start()

    def task2(self):
        def threadFunc():
            while True:
                global_ms.text_print.emit('输出内容')
                time.sleep(1)

        thread = Thread(target=threadFunc)
        thread.start()


if __name__ == "__main__":
    app = QApplication([])
    gui_main = Stats()
    gui_main.ui.show()
    app.exec()
