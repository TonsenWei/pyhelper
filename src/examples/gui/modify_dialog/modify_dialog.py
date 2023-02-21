# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'modify_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_modifyDialog(object):
    def setupUi(self, modifyDialog):
        if not modifyDialog.objectName():
            modifyDialog.setObjectName(u"modifyDialog")
        modifyDialog.resize(597, 411)
        self.gridLayout = QGridLayout(modifyDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.checkBoxApplyAll = QCheckBox(modifyDialog)
        self.checkBoxApplyAll.setObjectName(u"checkBoxApplyAll")

        self.gridLayout.addWidget(self.checkBoxApplyAll, 2, 0, 1, 1)

        self.lblModifySteps = QLabel(modifyDialog)
        self.lblModifySteps.setObjectName(u"lblModifySteps")

        self.gridLayout.addWidget(self.lblModifySteps, 0, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(modifyDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)

        self.comboBoxStepType = QComboBox(modifyDialog)
        self.comboBoxStepType.setObjectName(u"comboBoxStepType")

        self.gridLayout.addWidget(self.comboBoxStepType, 0, 1, 1, 2)

        self.tableWidgetModify = QTableWidget(modifyDialog)
        self.tableWidgetModify.setObjectName(u"tableWidgetModify")

        self.gridLayout.addWidget(self.tableWidgetModify, 1, 0, 1, 3)


        self.retranslateUi(modifyDialog)
        self.buttonBox.accepted.connect(modifyDialog.accept)
        self.buttonBox.rejected.connect(modifyDialog.reject)

        QMetaObject.connectSlotsByName(modifyDialog)
    # setupUi

    def retranslateUi(self, modifyDialog):
        modifyDialog.setWindowTitle(QCoreApplication.translate("modifyDialog", u"Dialog", None))
        self.checkBoxApplyAll.setText(QCoreApplication.translate("modifyDialog", u"\u5e94\u7528\u5230\u6240\u6709\u6a21\u5757", None))
        self.lblModifySteps.setText(QCoreApplication.translate("modifyDialog", u"\u4fee\u6539\u6b65\u9aa4:", None))
    # retranslateUi

