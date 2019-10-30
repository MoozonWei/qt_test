#!/usr/bin/python3
# coding=utf8
import sys
import cv2
import serial  # 树莓派串口包
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow

from controllerUI import Ui_MainWindow

stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"

##################################################################
# ------------------------------状态--------------------------------
no_rect = 0
no_highLeg = 1
no_hexagon = 2
no_crab = 3
no_upDown = 4
##################################################################
# 串口指令（第5位十六进制数代表动作组号，后两位次数，(0x00,0x00指无限次) #
##################################################################
cmd_upDown_init =       [0x55, 0x55, 0x05, 0x06, 0x00, 0x01, 0x00]
cmd_upDown_forward =    [0x55, 0x55, 0x05, 0x06, 0x01, 0x01, 0x00]
cmd_upDown_backward =   [0x55, 0x55, 0x05, 0x06, 0x02, 0x01, 0x00]
cmd_upDown_left =       [0x55, 0x55, 0x05, 0x06, 0x04, 0x01, 0x00]
cmd_upDown_right =      [0x55, 0x55, 0x05, 0x06, 0x03, 0x01, 0x00]

cmd_crab_init =         [0x55, 0x55, 0x05, 0x06, 0x12, 0x01, 0x00]
cmd_crab_forward =      [0x55, 0x55, 0x05, 0x06, 0x13, 0x01, 0x00]
cmd_crab_backward =     [0x55, 0x55, 0x05, 0x06, 0x14, 0x01, 0x00]

cmd_rect_init =         [0x55, 0x55, 0x05, 0x06, 0x19, 0x01, 0x00]
cmd_rect_forward =      [0x55, 0x55, 0x05, 0x06, 0x1A, 0x01, 0x00]
cmd_rect_backward =     [0x55, 0x55, 0x05, 0x06, 0x1B, 0x01, 0x00]
cmd_rect_left =         [0x55, 0x55, 0x05, 0x06, 0x1C, 0x01, 0x00]
cmd_rect_right =        [0x55, 0x55, 0x05, 0x06, 0x1D, 0x01, 0x00]

cmd_highLeg_init =      [0x55, 0x55, 0x05, 0x06, 0x1E, 0x01, 0x00]
cmd_highLeg_forward =   [0x55, 0x55, 0x05, 0x06, 0x1F, 0x01, 0x00]

cmd_hexagon_init =      [0x55, 0x55, 0x05, 0x06, 0x22, 0x01, 0x00]
cmd_hexagon_forward =   [0x55, 0x55, 0x05, 0x06, 0x23, 0x01, 0x00]
cmd_hexagon_backward =  [0x55, 0x55, 0x05, 0x06, 0x24, 0x01, 0x00]
cmd_hexagon_left =      [0x55, 0x55, 0x05, 0x06, 0x25, 0x01, 0x00]
cmd_hexagon_right =     [0x55, 0x55, 0x05, 0x06, 0x26, 0x01, 0x00]

cmd_transform_rectToUpDown = [0x55, 0x55, 0x05, 0x06, 0x32, 0x01, 0x00]
cmd_transform_upDownToRect = [0x55, 0x55, 0x05, 0x06, 0x33, 0x01, 0x00]

cmd_pose_rectStandSway = [0x55, 0x55, 0x05, 0x06, 0x64, 0x01, 0x00]
cmd_pose_rectM =        [0x55, 0x55, 0x05, 0x06, 0x65, 0x01, 0x00]
cmd_pose_rectSuperman = [0x55, 0x55, 0x05, 0x06, 0x66, 0x01, 0x00]
cmd_pose_rectDogSitP =  [0x55, 0x55, 0x05, 0x06, 0x68, 0x01, 0x00]
cmd_pose_rectDogSitO =  [0x55, 0x55, 0x05, 0x06, 0x69, 0x01, 0x00]
cmd_pose_rectTakeOff =  [0x55, 0x55, 0x05, 0x06, 0x6A, 0x01, 0x00]

cmd_upStairs = [0x55, 0x55, 0x05, 0x06, 0xC8, 0x01, 0x00]

# ----------------------前、后、左、右、初始化------------------------
# ------------------------摄像、变胞、上楼梯-------------------------
# ---------------------四边、高脚、六边形、螃蟹-----------------------


class PyQtMainEntry(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.radioButton_bodyStatus_rect.setChecked(True)

        self.camera = cv2.VideoCapture(stream)
        self.is_camera_opened = False   # 摄像头有没有打开标记
        self.body_status = no_rect      # 机器人的初始状态是rect

        # 定时器：30ms捕获一帧
        self._timer = QtCore.QTimer(self)
        self._timer.timeout.connect(self._queryFrame)
        self._timer.setInterval(15)

    #########################################################

    def move_forward(self):
        '''
        前
        '''
        if self.body_status == no_rect:
            serialHandle.write(cmd_rect_forward)
        elif self.body_status == no_highLeg:
            serialHandle.write(cmd_highLeg_forward)
        elif self.body_status == no_hexagon:
            serialHandle.write(cmd_hexagon_forward)
        elif self.body_status == no_crab:
            serialHandle.write(cmd_crab_forward)
        elif self.body_status == no_upDown:
            serialHandle.write(cmd_upDown_forward)

    def move_backward(self):
        '''
        后
        '''
        if self.body_status == no_rect:
            serialHandle.write(cmd_rect_backward)
        elif self.body_status == no_highLeg:
            pass
        elif self.body_status == no_hexagon:
            serialHandle.write(cmd_hexagon_backward)
        elif self.body_status == no_crab:
            serialHandle.write(cmd_crab_backward)
        elif self.body_status == no_upDown:
            serialHandle.write(cmd_upDown_backward)

    def move_left(self):
        '''
        左
        '''
        if self.body_status == no_rect:
            serialHandle.write(cmd_rect_left)
        elif self.body_status == no_highLeg:
            pass
        elif self.body_status == no_hexagon:
            serialHandle.write(cmd_hexagon_left)
        elif self.body_status == no_crab:
            pass
        elif self.body_status == no_upDown:
            serialHandle.write(cmd_upDown_left)

    def move_right(self):
        '''
        右
        '''
        if self.body_status == no_rect:
            serialHandle.write(cmd_rect_right)
        elif self.body_status == no_highLeg:
            pass
        elif self.body_status == no_hexagon:
            serialHandle.write(cmd_hexagon_right)
        elif self.body_status == no_crab:
            pass
        elif self.body_status == no_upDown:
            serialHandle.write(cmd_upDown_right)

    def initialize_body_shape(self):
        '''
        初始化
        '''
        if self.body_status == no_rect:
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_highLeg:
            serialHandle.write(cmd_highLeg_init)
        elif self.body_status == no_hexagon:
            serialHandle.write(cmd_hexagon_init)
        elif self.body_status == no_crab:
            serialHandle.write(cmd_crab_init)
        elif self.body_status == no_upDown:
            serialHandle.write(cmd_upDown_init)

    def up_stairs(self):
        '''
        上楼梯
        '''
        if self.body_status == no_rect:
            serialHandle.write(cmd_upStairs)
        elif self.body_status == no_highLeg:
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_hexagon:
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_crab:
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_upDown:
            serialHandle.write(cmd_transform_upDownToRect)

    #########################################################

    def camera_status(self):
        '''
        打开和关闭摄像头
        '''
        self.is_camera_opened = ~self.is_camera_opened
        if self.is_camera_opened:
            self._timer.start()
        else:
            self._timer.stop()

    #########################################################

    def transform_to_rect(self):
        '''
        变换为四边
        '''
        if self.body_status == no_rect:  # rect -> rect
            self.body_status = no_rect
            pass
        elif self.body_status == no_highLeg:  # highLeg -> rect
            self.body_status = no_rect
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_hexagon:  # hexagon -> rect
            self.body_status = no_rect
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_crab:  # crab -> rect
            self.body_status = no_rect
            serialHandle.write(cmd_rect_init)
        elif self.body_status == no_upDown:  # upDown -> rect
            self.body_status = no_rect
            serialHandle.write(cmd_transform_upDownToRect)

    def transform_to_highLeg(self):
        '''
        变换为高脚
        '''
        if self.body_status == no_rect:  # rect -> highLeg
            self.body_status = no_highLeg
            serialHandle.write(cmd_highLeg_init)
        elif self.body_status == no_highLeg:  # highLeg -> highLeg
            self.body_status = no_highLeg
            pass
        elif self.body_status == no_hexagon:  # hexagon -> rect -> highLeg
            self.body_status = no_highLeg
            serialHandle.write(cmd_rect_init)
            time.sleep(3)
            serialHandle.write(cmd_highLeg_init)
        elif self.body_status == no_crab:  # crab -> rect -> highLeg
            self.body_status = no_highLeg
            serialHandle.write(cmd_rect_init)
            time.sleep(3)
            serialHandle.write(cmd_highLeg_init)
        elif self.body_status == no_upDown:  # upDown -> rect -> highLeg
            self.body_status = no_highLeg
            serialHandle.write(cmd_transform_upDownToRect)
            time.sleep(25)
            serialHandle.write(cmd_highLeg_init)

    def transform_to_hexagon(self):
        '''
        变换为六边形
        '''
        if self.body_status == no_rect:  # rect -> hexagon
            self.body_status = no_hexagon
            serialHandle.write(cmd_hexagon_init)
        elif self.body_status == no_highLeg:  # highLeg -> hexagon
            self.body_status = no_hexagon
            serialHandle.write(cmd_hexagon_init)
        elif self.body_status == no_hexagon:  # hexagon -> hexagon
            self.body_status = no_hexagon
            pass
        elif self.body_status == no_crab:  # crab -> hexagon
            self.body_status = no_hexagon
            serialHandle.write(cmd_hexagon_init)
        elif self.body_status == no_upDown:  # upDown -> hexagon
            self.body_status = no_hexagon
            serialHandle.write(cmd_transform_upDownToRect)
            time.sleep(25)
            serialHandle.write(cmd_hexagon_init)

    def transform_to_crab(self):
        '''
        变换为螃蟹
        '''
        if self.body_status == no_rect:  # rect -> crab
            self.body_status = no_crab
            serialHandle.write(cmd_crab_init)
        elif self.body_status == no_highLeg:  # highLeg -> crab
            self.body_status = no_crab
            serialHandle.write(cmd_crab_init)
        elif self.body_status == no_hexagon:  # hexagon -> crab
            self.body_status = no_crab
            serialHandle.write(cmd_crab_init)
        elif self.body_status == no_crab:  # crab -> crab
            self.body_status = no_crab
            pass
        elif self.body_status == no_upDown:  # upDown -> crab
            self.body_status = no_crab
            serialHandle.write(cmd_transform_upDownToRect)
            time.sleep(25)
            serialHandle.write(cmd_crab_init)

    def transform_to_upDown(self):
        '''
        变换为翻转
        '''
        if self.body_status == no_rect:  # rect -> upDown
            self.body_status = no_upDown
            serialHandle.write(cmd_transform_rectToUpDown)
        elif self.body_status == no_highLeg:  # highLeg -> rect -> upDown
            self.body_status = no_upDown
            serialHandle.write(cmd_rect_init)
            time.sleep(3)
            serialHandle.write(cmd_transform_rectToUpDown)
        elif self.body_status == no_hexagon:  # hexagon -> rect -> upDown
            self.body_status = no_upDown
            serialHandle.write(cmd_rect_init)
            time.sleep(3)
            serialHandle.write(cmd_transform_rectToUpDown)
        elif self.body_status == no_crab:  # crab -> rect -> upDown
            self.body_status = no_upDown
            serialHandle.write(cmd_rect_init)
            time.sleep(3)
            serialHandle.write(cmd_transform_rectToUpDown)
        elif self.body_status == no_upDown:  # upDown -> upDown
            self.body_status = no_upDown
            pass

    #########################################################

    @QtCore.pyqtSlot()
    def _queryFrame(self):
        '''
        循环捕获图片
        '''
        ret, self.frame = self.camera.read()

        img_rows, img_cols, channels = self.frame.shape
        bytesPerLine = channels * img_cols

        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        QImg = QImage(self.frame.data, img_cols, img_rows,
                      bytesPerLine, QImage.Format_RGB888)
        self.labelCamera.setPixmap(QPixmap.fromImage(QImg).scaled(
            self.labelCamera.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PyQtMainEntry()
    serialHandle = serial.Serial("/dev/ttyAMA0", 9600)  # 实例化一个串口对象。波特率9600
    serialHandle.write(cmd_rect_init)
    window.show()
    sys.exit(app.exec_())
