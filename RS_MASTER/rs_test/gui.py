import sys
import os
import json
#import keyboard

from PyQt5.QtCore import QCoreApplication, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QStyleFactory
from PyQt5.QtWidgets import QAction, QMessageBox, QCheckBox, QProgressBar, QLabel, QComboBox
from PyQt5.QtWidgets import QFileDialog, QLineEdit
from PyQt5.QtCore import pyqtSlot

import cv2
import json
import requests
import numpy as np
import os, sys, time
from shutil import copyfile
from PIL import ImageGrab

import threading
from threading import Thread

import wavtest

DEFAULT_REGION = (0,100,200,400)
REGION = (0,100,200,400)

DEFAULT_PX_CT = 50

RGB = [0,0,0]
DEFAULT_R = 0
DEFAULT_G = 0
DEFAULT_B = 0
GRAB_FREQ = .5


class Window(QMainWindow):
    resized = pyqtSignal()
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(100, 100, 620, 500)
        self.setWindowTitle('Duel/Trade Alerter 1.0.2')
        self.init_ui()
        self.threads = []

        self.ok = True

    def init_ui(self):
        boldFont = QFont()
        boldFont.setBold(True)
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.monitor_region = QLabel(self)
        self.update_monitor_region()
        self.monitor_region.move(100,20)

        self.tbx1 = QLineEdit(self)
        self.tbx1.move(100, 300)
        self.tbx1.resize(100,30)
        self.tbx1.setText(str(DEFAULT_REGION[0]))

        self.x_label = QLabel('X1,Y1', self)
        self.x_label.setFont(boldFont)
        self.x_label.resize(150, 10)
        self.x_label.move(20, 310)

        self.tby1 = QLineEdit(self)
        self.tby1.move(250, 300)
        self.tby1.resize(100,30)
        self.tby1.setText(str(DEFAULT_REGION[1]))

        self.tbx2 = QLineEdit(self)
        self.tbx2.move(100, 350)
        self.tbx2.resize(100,30)
        self.tbx2.setText(str(DEFAULT_REGION[2]))

        self.y_label = QLabel('X2,Y2', self)
        self.y_label.setFont(boldFont)
        self.y_label.resize(150, 10)
        self.y_label.move(20, 360)

        self.tby2 = QLineEdit(self)
        self.tby2.move(250, 350)
        self.tby2.resize(100,30)
        self.tby2.setText(str(DEFAULT_REGION[3]))

        self.rgb_label = QLabel('RGB', self)
        self.rgb_label.setFont(boldFont)
        self.rgb_label.resize(150, 10)
        self.rgb_label.move(400, 310)

        self.rgb_r = QLineEdit(self)
        self.rgb_r.move(450, 300)
        self.rgb_r.resize(40,30)
        self.rgb_r.setText(str(DEFAULT_R))

        self.rgb_g = QLineEdit(self)
        self.rgb_g.move(500, 300)
        self.rgb_g.resize(40,30)
        self.rgb_g.setText(str(DEFAULT_G))

        self.rgb_b = QLineEdit(self)
        self.rgb_b.move(550, 300)
        self.rgb_b.resize(40,30)
        self.rgb_b.setText(str(DEFAULT_B))

        self.rgb_label = QLabel('PX', self)
        self.rgb_label.setFont(boldFont)
        self.rgb_label.resize(150, 10)
        self.rgb_label.move(400, 360)

        self.px_ct = QLineEdit(self)
        self.px_ct.move(450, 350)
        self.px_ct.resize(40,30)
        self.px_ct.setText(str(DEFAULT_PX_CT))

        self.pxct_label = QLabel('TOTAL PX', self)
        self.pxct_label.setFont(boldFont)
        self.pxct_label.resize(150, 10)
        self.pxct_label.move(250, 400)

        self.pxct = QLabel('', self)
        self.pxct.setFont(boldFont)
        self.pxct.resize(150, 10)
        self.pxct.move(250, 410)

        self.px_ct = QLineEdit(self)
        self.px_ct.move(450, 350)
        self.px_ct.resize(40,30)
        self.px_ct.setText(str(DEFAULT_PX_CT))

        self.reg_button = QPushButton('CHECK REGION', self)
        self.reg_button.move(100, 400)
        self.reg_button.clicked.connect(self.check_reg)

        self.start_button = QPushButton('START', self)
        self.start_button.move(100, 450)
        self.start_button.clicked.connect(self.start)

        self.reset_button = QPushButton('STOP', self)
        self.reset_button.move(250, 450)
        self.reset_button.clicked.connect(self.reset)

        self.show()


    def start(self, event):
        tbx1 = self.tbx1.text()
        tby1 = self.tby1.text()
        tbx2 = self.tbx2.text()
        tby2 = self.tby2.text()

        tbr = self.rgb_r.text()
        tbg = self.rgb_g.text()
        tbb = self.rgb_b.text()

        tbpx = self.px_ct.text()

        REGION = (int(tbx1), int(tby1), int(tbx2), int(tby2))
        RGB = [int(tbr), int(tbg), int(tbb)]

        th = Thread(target = monitor(REGION, RGB, int(tbpx)))

        self.threads.append(th)
        th.start()
        th.join()
        #monitor(REGION, RGB)

    def reset(self, event):
        x=1
        self.OK = False
        for i in range(len(self.threads)):
            self.threads[i].terminate()

    def check_reg(self, event):
        tbx1 = self.tbx1.text()
        tby1 = self.tby1.text()
        tbx2 = self.tbx2.text()
        tby2 = self.tby2.text()

        REGION = (int(tbx1), int(tby1), int(tbx2), int(tby2))


        #print("region update", flush=True)
        #print(str(REGION), flush=True)
        update_image(REGION)
        self.pxct.setText(str(((REGION[2] - REGION[0])*(REGION[3] - REGION[1]))))
        self.update_monitor_region()
        #update_monitor_region(self)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)


    def update_monitor_region(self):
        image_filepath = 'out_img.png'
        self.pixmap = QPixmap(image_filepath)
        self.monitor_region.setPixmap(self.pixmap)
        self.monitor_region.resize(400,200)


def run():
    app = QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

def monitor(REGION, RGB, NUM):
    #print("Starting screen captures every " + str(GRAB_FREQ) + " seconds.", flush=True)
    print("CTRL+C TO QUIT",flush=True)
    while(1):
        #print("in loop", flush=True)
        QCoreApplication.processEvents()
        screen =  ImageGrab.grab(bbox=REGION)
        img = np.array(screen.getdata(),dtype='uint8')\
        .reshape((screen.size[1],screen.size[0],3))
        img_np = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        pinks = 0
        for i in range(len(img_np)):
            for j in range(len(img_np[0])):
                px = img_np[i,j]
                if px[0] == RGB[2] and px[1] == RGB[1] and px[2] == RGB[0]:
                    pinks += 1

        if pinks > NUM:
            #print("DING " + str(TOTAL_DINGS), flush=True)
            wavtest.ding()

        #else:
            #print("---", flush=True)

        cv2.imwrite('out_img.png', img_np)
        cv2.destroyAllWindows()
        time.sleep(GRAB_FREQ)

        continue

def update_image(REGION):
    screen =  ImageGrab.grab(bbox=REGION)
    img_np = np.array(screen.getdata(),dtype='uint8')\
    .reshape((screen.size[1],screen.size[0],3))
    img_np = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
    cv2.imwrite('out_img.png', img_np)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()
