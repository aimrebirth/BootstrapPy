#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import shutil
import subprocess

from polygon4bootstrap import *

bootstrap_updater_version = 2

_7z  = '7za'
curl = 'curl'

def main():
    print_version()
    if os.path.exists(BootstrapDownloads) == False:
        os.mkdir(BootstrapDownloads)
    if os.path.exists(bootstrap_zip):
        shutil.copy(bootstrap_zip, bootstrap_zip + '.bak')
    download_file(bootstrap, bootstrap_zip)
    unpack_file(bootstrap_zip)

def download_file(url, file):
    print('Downloading file: ' + file)
    p = subprocess.Popen([curl, '-L', '-k', '-o', file, url])
    p.communicate()
    print()

def unpack_file(file):
    print('Unpacking file: ' + file)
    p = subprocess.Popen([_7z, 'x', '-y', file], stdout = subprocess.PIPE)
    p.communicate()

def print_version():
    print('Polygon-4 Bootstrap Updater Version ' + str(bootstrap_updater_version))
    print()

if __name__ == '__main__':
    main()
