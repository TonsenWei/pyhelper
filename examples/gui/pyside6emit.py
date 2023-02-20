import sys, time
from PySide6.QtCore import Signal, Slot, Qt, QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QApplication


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.label = QLabel("Hello!")
        self.label.setAlignment(Qt.AlignCenter)
        self.but = QPushButton("Click!")
        self.but.clicked.connect(self.fun)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.but)
        self.setLayout(self.layout)
        self.setWindowTitle('Signal Example')
        self.resize(300, 300)
        self.show()

    @Slot()
    def fun(self):
        self.th = Th()
        self.th.timer.connect(self.flushlabel)
        self.th.finish.connect(self.isFinish)
        self.th.start()

    @Slot(int)
    def flushlabel(self, nu):
        self.label.setText(str(nu))

    @Slot(bool)
    def isFinish(self, bo):
        if bo is True:
            self.but.setEnabled(True)
        else:
            self.but.setEnabled(False)


class Th(QThread):
    timer = Signal(int)
    finish = Signal(bool)

    def __init__(self) -> None:
        super().__init__()

    def run(self):
        print('Start Timer')
        self.finish.emit(False)
        for x in range(5):
            self.timer.emit(5 - x)
            time.sleep(1)
        self.finish.emit(True)


if __name__ == '__main__':
    app = QApplication([])
    widgets = MainWindow()
    sys.exit(app.exec())