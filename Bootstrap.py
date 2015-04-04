#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import subprocess

# links
git_polygon4 = 'https://github.com/aimrebirth/Polygon4.git'

content_file = ''
project_file = ''
third_party_file = ''

# executables
cmake = 'cmake'
git = 'git'

# names
polygon4 = 'Polygon4'

def main():
    base_dir = os.path.abspath(os.path.curdir) + '/'
    dir = base_dir + polygon4
    if os.path.exists(dir):
        print('Directory Polygon4 exists. Remove it and try again.')
        #return
    #os.mkdir(dir)
    os.chdir(dir)
    download_sources()
    download_files(dir)
    run_cmake(dir)
    #build project
    #run editor

def download_sources():
    print('Downloading latest sources from Github repositories')
    p = subprocess.Popen([git, 'clone', git_polygon4, '.'])
    p.communicate()
    p = subprocess.Popen([git, 'submodule', 'init'])
    p.communicate()
    p = subprocess.Popen([git, 'submodule', 'update'])
    p.communicate()

def run_cmake(dir):
    print('Running CMake')
    dir = dir + '/ThirdParty/'
    p = subprocess.Popen([cmake,
                          '-H' + dir + 'Engine',
                          '-B' + dir + 'Engine/Win64',
                          '-DBOOST_ROOT=' + dir + 'boost',
                          '-DBOOST_LIBRARYDIR=' + dir + 'boost/lib64-msvc-12.0/',
                          '-G', 'Visual Studio 12 Win64'
                          ])
    p.communicate()

def download_files(dir):
    print('Downloading project files')

if __name__ == '__main__':
    main()