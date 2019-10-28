#!/usr/bin/python3
#coding=utf8
import sys
import time

from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QFileDialog, QMainWindow

from controllerUI import Ui_MainWindow

stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"

class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radioButton_A.setChecked(True);

    def btnForward_Clicked(self):
        '''
        前
        '''
        print("前")

    def btnBackward_Clicked(self):
        '''
        后
        '''
        print("后")

    def btnLeft_Clicked(self):
        '''
        左
        '''
        print("左")

    def btnRight_Clicked(self):
        '''
        右
        '''
        print("右")

    def btnInitialize_Clicked(self):
        '''
        初始化
        '''
        print("初始化")

    #########################################################

    def btnOpenCamera_Clicked(self):
        '''
        打开和关闭摄像头
        '''
        pass

    def btnBianbao_Clicked(self):
        '''
        变胞
        '''
        pass

    def btnUpSteps_Clicked(self):
        '''
        上楼梯
        '''
        pass

    #########################################################

    def btnSibian_Clicked(self):
        '''
        四边
        '''
        pass

    def btnHighLeg_Clicked(self):
        '''
        高脚
        '''
        pass

    def btnHexagon_Clicked(self):
        '''
        六边形
        '''
        pass

    def btnCrab_Clicked(self):
        '''
        螃蟹
        '''
        pass

    ###############
    def test_check_camera(self):
        if self.radioButton_camera.isChecked():
            print("摄像头已经打开")
        if not self.radioButton_camera.isChecked():
            print("摄像头已经关闭")

    def test_a(self):
        if not self.radioButton_A.isChecked():
            print("a")

    def test_b(self):
        if not self.radioButton_B.isChecked():
            print("b")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    window.show()
    sys.exit(app.exec_())
