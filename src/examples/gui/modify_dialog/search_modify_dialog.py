# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'search_modify_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_searchModifyDialog(object):
    def setupUi(self, searchModifyDialog):
        if not searchModifyDialog.objectName():
            searchModifyDialog.setObjectName(u"searchModifyDialog")
        searchModifyDialog.resize(606, 142)
        self.gridLayout = QGridLayout(searchModifyDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.lblModifySteps = QLabel(searchModifyDialog)
        self.lblModifySteps.setObjectName(u"lblModifySteps")
        self.lblModifySteps.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.lblModifySteps, 1, 0, 1, 1)

        self.lineEditModifyTo = QLineEdit(searchModifyDialog)
        self.lineEditModifyTo.setObjectName(u"lineEditModifyTo")
        self.lineEditModifyTo.setMinimumSize(QSize(0, 28))

        self.gridLayout.addWidget(self.lineEditModifyTo, 2, 1, 1, 2)

        self.lineEditKeyword = QLineEdit(searchModifyDialog)
        self.lineEditKeyword.setObjectName(u"lineEditKeyword")
        self.lineEditKeyword.setMinimumSize(QSize(0, 28))

        self.gridLayout.addWidget(self.lineEditKeyword, 1, 1, 1, 2)

        self.buttonBox = QDialogButtonBox(searchModifyDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)

        self.label = QLabel(searchModifyDialog)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)

        self.labelTip = QLabel(searchModifyDialog)
        self.labelTip.setObjectName(u"labelTip")
        self.labelTip.setStyleSheet(u"color: rgb(255, 0, 0)")
        self.labelTip.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelTip, 0, 0, 1, 3)

        self.checkBoxApplyAll = QCheckBox(searchModifyDialog)
        self.checkBoxApplyAll.setObjectName(u"checkBoxApplyAll")

        self.gridLayout.addWidget(self.checkBoxApplyAll, 3, 0, 1, 2)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)

        self.retranslateUi(searchModifyDialog)
        self.buttonBox.accepted.connect(searchModifyDialog.accept)
        self.buttonBox.rejected.connect(searchModifyDialog.reject)

        QMetaObject.connectSlotsByName(searchModifyDialog)
    # setupUi

    def retranslateUi(self, searchModifyDialog):
        searchModifyDialog.setWindowTitle(QCoreApplication.translate("searchModifyDialog", u"Dialog", None))
        self.lblModifySteps.setText(QCoreApplication.translate("searchModifyDialog", u"\u5173\u952e\u5b57:", None))
        self.label.setText(QCoreApplication.translate("searchModifyDialog", u"\u4fee\u6539\u4e3a:", None))
        self.labelTip.setText(QCoreApplication.translate("searchModifyDialog", u"\u4f1a\u641c\u7d22\u6307\u5b9a\u5185\u5bb9\uff0c\u66ff\u6362\u641c\u7d22\u5230\u7684\u5173\u952e\u5b57\u4e3a\u65b0\u4fee\u6539\u7684\u5b57\u7b26\u4e32\uff0c\u8bf7\u6ce8\u610f\u5907\u4efd\u7528\u4f8b!", None))
        self.checkBoxApplyAll.setText(QCoreApplication.translate("searchModifyDialog", u"\u5e94\u7528\u5230\u6240\u6709\u6a21\u5757", None))
    # retranslateUi

