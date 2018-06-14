#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  run-swipe.py
#
#  Test script for vmate feed, you need install opencv for python to run this script:
#  # sudo pip install opencv-python
#
#  Copyright 2018 martin <martin@martin>
#
#

import os
import sys
import time
import datetime
import cv2

ADB_SWP = 'adb shell input swipe %d 600 %d 200 %d'
ADB_TAP = 'adb shell input tap %d %d'
ADB_SCR = 'adb shell dumpsys window displays | grep cur | awk -F " " \'{print $3}\' | awk -F "=" \'{print $2}\''
ADB_CAP = 'adb shell screencap -p /sdcard/%s && adb pull /sdcard/%s'

# define color in vmate
DEF_COLORS = [
    '#F0D7C5',
    '#EEBEB0',
    '#C3C7D0',
    '#F2F2F2',
    '#8E8CC4',
    '#D7CAE8',
    '#8BC4CA',
    '#E0DADF',
    '#D1A0D1',
    '#9AC9E1',
    '#E5C18C',
    '#C9C4B2'
]

DEF_SPEED = 50
DEF_DELAY = 50

screen_w = 0
screen_h = 0

# check capture image has defined color block
def chkColorBlock(imgFn):
    img = cv2.imread(imgFn)
    b, g, r = cv2.split(img)

    hist = cv2.calcHist([b], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    bMax = maxLoc[1]

    hist = cv2.calcHist([g], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    gMax = maxLoc[1]

    hist = cv2.calcHist([r], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    rMax = maxLoc[1]

    hexColor = '#%02X%02X%02X' % (rMax, gMax, bMax)

    return (hexColor in DEF_COLORS)

# capture current screen & return file name
def capScreen():
    img_fn = 'scr-{date:%Y%m%d%H%M%S}.png'.format(date=datetime.datetime.now())
    # print img_fn
    # swipe cmd
    cmd = ADB_CAP % (img_fn, img_fn)
    # print 'capture cmd:', cmd
    os.system(cmd)

    return img_fn

# init screen width & height
def initScreen():
    global screen_w
    global screen_h
    lines = os.popen(ADB_SCR).readlines()
    for line in lines:
        if len(line) > 0:
            vals = line[:-1].split('x')
            if len(vals) == 2:
                screen_w = int(vals[0])
                screen_h = int(vals[1])

def main(argv):
    if len(argv) == 1:
        print 'usage:' + argv[0] + ' [count] [speed] [delay]'

    # set count
    if len(argv) >= 2:
        count = int(argv[1])
    else:
        count = 10
    print 'count:', count

    # set count
    if len(argv) >= 3:
        speed = int(argv[2])
    else:
        speed = DEF_SPEED
    print 'speed:', speed

    # set delay
    if len(argv) >= 4:
        delay = int(argv[3])
    else:
        delay = DEF_DELAY
    print 'delay:', delay

    # init screen
    initScreen()
    print 'w:%d, h:%d' % (screen_w, screen_h)
    print '------------------------------------'

    # capScreen()

    idx = 0
    while idx < count:
        idx_s = 0
        while idx_s < 5:
            # swipe cmd
            cmd = ADB_SWP % (screen_w / 2, screen_w / 2, speed)
            # print 'swipe cmd:', cmd
            os.system(cmd)

            idx_s += 1

        # tap screen center
        cmd = ADB_TAP % (screen_w / 2, screen_h / 2)
        # print 'tap cmd:', cmd
        os.system(cmd)

        # delay 50ms
        time.sleep(delay / 1000)

        imgFn = capScreen()
        if chkColorBlock(imgFn):
            print idx, 'loading...'
        else:
            print idx, 'ok!'

        idx += 1

if __name__ == '__main__':
    main(sys.argv)
