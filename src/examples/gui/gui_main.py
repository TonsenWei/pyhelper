# PySide6~=6.2.4
from threading import Thread

from PySide2 import QtCore
from PySide6.QtCore import QObject, Signal
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QTextBrowser

from examples.gui.utils.file_util import FileUtil

VERSION_INFO = "版本：V1.0.0 \n日期：2022-04-07\n作者：韦冬成"


# 自定义信号源对象类型，一定要继承自 QObject
class MySignals(QObject):
    # 定义一种信号，两个参数 类型分别是： QTextBrowser 和 字符串
    # 调用 emit方法 发信号时，传入参数 必须是这里指定的 参数类型
    text_print = Signal(QTextBrowser, str)
    # 还可以定义其他种类的信号
    update_table = Signal(str)


# 实例化
global_ms = MySignals()


class GuiMain:

    def __init__(self):
        self.ui = QUiLoader().load('gui_main.ui')
        # 自定义信号的处理函数
        global_ms.text_print.connect(self.printToGui)

        self.ui.btnSelectDir.clicked.connect(self.select_dir)
        self.ui.actionAbout.triggered.connect(self.show_about_dialog)
        self.ui.btnStart.clicked.connect(self.start_process)

    def printToGui(self, fb, text):
        fb.append(str(text))
        fb.ensureCursorVisible()

    def select_dir(self):
        print("select dir ...")
        dialog = QFileDialog(self.ui)
        path = dialog.getExistingDirectory(self.ui, "选择目录", "./", QFileDialog.ShowDirsOnly)
        print(path)
        self.ui.lineEditDir.setText(path)
        files_list = FileUtil.get_files_path_list(path, ".py")
        for file_str in files_list:
            self.ui.textBrowser.append(str(file_str))

    def start_process(self):
        print("clicked")
        def threadFunc():
            # 通过Signal 的 emit 触发执行 主线程里面的处理函数
            # emit参数和定义Signal的数量、类型必须一致
            # while True:
            global_ms.text_print.emit(self.ui.textBrowser, '输出内容')
            # time.sleep(1)

        thread = Thread(target=threadFunc)
        thread.start()

    def show_about_dialog(self):
        QMessageBox.information(
            self.ui,
            '关于',
            VERSION_INFO)


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)  # 解决2K分辨率电脑显示不全的问题
    app = QApplication([])
    gui_main = GuiMain()
    gui_main.ui.show()
    app.exec()
