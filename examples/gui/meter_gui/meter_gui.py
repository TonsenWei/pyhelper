# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\projects\python\pylearning\examples\gui\meter_gui\meter_gui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_meterGui(object):
    def setupUi(self, meterGui):
        meterGui.setObjectName("meterGui")
        meterGui.resize(642, 548)
        self.gridLayout = QtWidgets.QGridLayout(meterGui)
        self.gridLayout.setObjectName("gridLayout")
        self.lblTip = QtWidgets.QLabel(meterGui)
        self.lblTip.setObjectName("lblTip")
        self.gridLayout.addWidget(self.lblTip, 0, 0, 1, 1)
        self.lineEditSetValue = QtWidgets.QLineEdit(meterGui)
        self.lineEditSetValue.setObjectName("lineEditSetValue")
        self.gridLayout.addWidget(self.lineEditSetValue, 0, 1, 1, 1)
        self.btnSetValue = QtWidgets.QPushButton(meterGui)
        self.btnSetValue.setObjectName("btnSetValue")
        self.gridLayout.addWidget(self.btnSetValue, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(194, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.widget = QtWidgets.QWidget(meterGui)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 4)

        self.retranslateUi(meterGui)
        QtCore.QMetaObject.connectSlotsByName(meterGui)

    def retranslateUi(self, meterGui):
        _translate = QtCore.QCoreApplication.translate
        meterGui.setWindowTitle(_translate("meterGui", "Form"))
        self.lblTip.setText(_translate("meterGui", "设置指针指向值:"))
        self.btnSetValue.setText(_translate("meterGui", "设置"))
