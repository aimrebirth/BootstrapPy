#!/usr/bin/python3
# -*- coding: utf8 -*-

import os

from polygon4bootstrap import *

def main():
    print_version()
    data = load_data()
    base_dir = os.path.abspath(os.path.curdir) + '/'
    dir = base_dir + polygon4
    download_dir = base_dir + BootstrapDownloads
    if os.path.exists(dir) == False:
        os.mkdir(dir)
    if has_program_in_path(git):
        if os.path.exists(dir + '/.git') == False:
            download_sources(dir)
        else:
            update_sources(dir)
    else:
        manual_download()
    data = self_check(dir + data_file)
    if os.path.exists(download_dir) == False:
        os.mkdir(download_dir)
    download_files(download_dir, data)
    unpack_files(download_dir, data)
    run_cmake(dir)
    build_engine(dir)
    create_project_files(dir)
    build_project(dir)
    print('Bootstrapping is finished. You may run now Polygon4.uproject.')

if __name__ == '__main__':
    main()
