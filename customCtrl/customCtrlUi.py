# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Maya_TESTY\customCtrl\customCtrlGUI.ui'
#
# Created: Sat Sep 23 15:16:48 2017
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CUCO(object):
    def setupUi(self, CUCO):
        CUCO.setObjectName("CUCO")
        CUCO.resize(283, 475)
        self.controlGroupBox = QtWidgets.QGroupBox(CUCO)
        self.controlGroupBox.setGeometry(QtCore.QRect(20, 10, 241, 451))
        self.controlGroupBox.setTitle("")
        self.controlGroupBox.setObjectName("controlGroupBox")
        self.label = QtWidgets.QLabel(self.controlGroupBox)
        
        self.label.setGeometry(QtCore.QRect(100, 10, 41, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.addControl = QtWidgets.QPushButton(self.controlGroupBox)
        self.addControl.setGeometry(QtCore.QRect(10, 40, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.addControl.setFont(font)
        self.addControl.setObjectName("addControl")
        self.controlList = QtWidgets.QListWidget(self.controlGroupBox)
        self.controlList.setGeometry(QtCore.QRect(10, 200, 221, 241))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.controlList.setFont(font)
        self.controlList.setAlternatingRowColors(True)
        self.controlList.setResizeMode(QtWidgets.QListView.Adjust)
        self.controlList.setSpacing(2)
        self.controlList.setObjectName("controlList")
        self.deleteControlBTN = QtWidgets.QPushButton(self.controlGroupBox)
        self.deleteControlBTN.setGeometry(QtCore.QRect(10, 160, 80, 30))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.deleteControlBTN.setFont(font)
        self.deleteControlBTN.setObjectName("deleteControlBTN")
        self.newControlName = QtWidgets.QTextEdit(self.controlGroupBox)
        self.newControlName.setGeometry(QtCore.QRect(10, 80, 220, 25))
        self.newControlName.setObjectName("newControlName")
        self.groupBox = QtWidgets.QGroupBox(self.controlGroupBox)
        self.groupBox.setGeometry(QtCore.QRect(10, 110, 221, 41))
        self.groupBox.setObjectName("groupBox")
        self.rigthSide = QtWidgets.QRadioButton(self.groupBox)
        self.rigthSide.setGeometry(QtCore.QRect(170, 10, 49, 30))
        self.rigthSide.setBaseSize(QtCore.QSize(0, 0))
        self.rigthSide.setObjectName("rigthSide")
        self.center = QtWidgets.QRadioButton(self.groupBox)
        self.center.setGeometry(QtCore.QRect(80, 10, 61, 30))
        self.center.setBaseSize(QtCore.QSize(0, 0))
        self.center.setObjectName("center")
        self.leftSide = QtWidgets.QRadioButton(self.groupBox)
        self.leftSide.setGeometry(QtCore.QRect(10, 10, 42, 30))
        self.leftSide.setChecked(True)
        self.leftSide.setObjectName("leftSide")

        self.retranslateUi(CUCO)
        QtCore.QMetaObject.connectSlotsByName(CUCO)

    def retranslateUi(self, CUCO):
        CUCO.setWindowTitle(QtWidgets.QApplication.translate("CUCO", "Form", None))
        self.label.setText(QtWidgets.QApplication.translate("CUCO", "CUCO", None))
        self.addControl.setText(QtWidgets.QApplication.translate("CUCO", "Add", None))
        self.deleteControlBTN.setText(QtWidgets.QApplication.translate("CUCO", "Delete", None))
        self.newControlName.setPlaceholderText(QtWidgets.QApplication.translate("CUCO", "Add new name", None))
        self.groupBox.setTitle(QtWidgets.QApplication.translate("CUCO", "Side", None))
        self.rigthSide.setText(QtWidgets.QApplication.translate("CUCO", "Right", None))
        self.center.setText(QtWidgets.QApplication.translate("CUCO", "Center", None))
        self.leftSide.setText(QtWidgets.QApplication.translate("CUCO", "Left", None))

