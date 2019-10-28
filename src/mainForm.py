# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnSibian = QtWidgets.QPushButton(self.centralwidget)
        self.btnSibian.setGeometry(QtCore.QRect(340, 470, 93, 28))
        self.btnSibian.setObjectName("btnSibian")
        self.labelCamera = QtWidgets.QLabel(self.centralwidget)
        self.labelCamera.setGeometry(QtCore.QRect(50, 10, 700, 450))
        self.labelCamera.setObjectName("labelCamera")
        self.btnBianbao = QtWidgets.QPushButton(self.centralwidget)
        self.btnBianbao.setGeometry(QtCore.QRect(340, 510, 93, 28))
        self.btnBianbao.setObjectName("btnBianbao")
        self.btnOpenCamera = QtWidgets.QPushButton(self.centralwidget)
        self.btnOpenCamera.setGeometry(QtCore.QRect(50, 470, 93, 28))
        self.btnOpenCamera.setObjectName("btnOpenCamera")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.btnSibian.clicked.connect(MainWindow.btnSibian_Clicked)
        self.btnBianbao.clicked.connect(MainWindow.btnBianbao_Clicked)
        self.btnOpenCamera.clicked.connect(MainWindow.btnOpenCamera_Clicked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnSibian.setText(_translate("MainWindow", "四边形态"))
        self.labelCamera.setText(_translate("MainWindow", "摄像头"))
        self.btnBianbao.setText(_translate("MainWindow", "变胞形态"))
        self.btnOpenCamera.setText(_translate("MainWindow", "打开摄像头"))


