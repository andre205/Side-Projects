'''Fortroute Mapper takes screenshots of Fortnite BR minimap to map out a route through a match.'''

import cv2
import json
import requests
import numpy as np
import os, sys, time
from shutil import copyfile
from PIL import ImageGrab

import wavtest
from threading import Thread

REGION = (0,100,200,400)

TEST_REGION = (590,780,1050,785)
BIGGER_REGION = (0,500,600,700)

NUM_PINKS = 50
PINK_RGB = [0,0,0]
GRAB_FREQ = .5
TOTAL_DINGS = 0

if __name__ == '__main__':
    print("Starting screen captures every " + str(GRAB_FREQ) + " seconds.", flush=True)
    i=1
    while(i):
        #screen = ImageGrab.grab(bbox=TEST_REGION)
        screen =  ImageGrab.grab(bbox=BIGGER_REGION)
        img_np = np.array(screen.getdata(),dtype='uint8')\
        .reshape((screen.size[1],screen.size[0],3))
        #cv2.imshow('window',img_np)

        pinks = 0
        for i in range(len(img_np)):
            for j in range(len(img_np[0])):
                px = img_np[i,j]
                if px[0] == 0:
                    pinks += 1
                #print(px)
        if pinks > NUM_PINKS:
            TOTAL_DINGS += 1
            print("DING " + str(TOTAL_DINGS), flush=True)
            th = Thread(target = wavtest.ding())
            th.start()
            th.join()

            #wavtest.ding()

            #play('ding.wav')
        else:
            print("---", flush=True)

        cv2.imwrite('out_img.png', img_np)
        cv2.destroyAllWindows()
        time.sleep(GRAB_FREQ)
        i += GRAB_FREQ
        continue



def update_image():
        screen =  ImageGrab.grab(bbox=REGION)
        img_np = np.array(screen.getdata(),dtype='uint8')\
        .reshape((screen.size[1],screen.size[0],3))
        cv2.imwrite('out_img.png', img_np)
        cv2.destroyAllWindows()
