# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Maya_TESTY\customCtrl\test.ui'
#
# Created: Sun Sep 24 18:56:02 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)

        self.controlGroupBox = QtWidgets.QGroupBox(Form)
        self.controlGroupBox.setGeometry(QtCore.QRect(20, 10, 241, 451))
        self.controlGroupBox.setTitle("")
        self.controlGroupBox.setObjectName("controlGroupBox")
        self.label = QtWidgets.QLabel(self.controlGroupBox)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.retranslateUi(Form)
        #QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtWidgets.QApplication.translate("Form", "Form", None))

