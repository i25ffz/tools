#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  simple-parser.py
#
#  Simple parse single mp4 file's metadata.
#
#  You should install mediainfo(sudo apt install mediainfo) first.
#
#  Copyright 2017 martin <martin@martin>
#
#

import os

import subprocess

def main(args):
    # ref: https://stackpointer.io/mobile/android-adb-list-installed-package-names/416/
    proc = subprocess.Popen(['adb', 'shell', 'pm', 'list', 'packages', '-f'], stdout=subprocess.PIPE)
    for line in proc.stdout:
        # the real code does filtering here
        strTmp = line.rstrip()[8:]
        if (strTmp.startswith('/data/app')):
            vals = strTmp.split('=')
            pullCmd = 'adb pull ' + vals[0] + ' ' + vals[1] + '.apk'
            print os.popen(pullCmd).read()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
