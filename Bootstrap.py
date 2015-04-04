#!/usr/bin/python3
# -*- coding: utf8 -*-

import os
import subprocess

# links
git_polygon4        = 'https://github.com/aimrebirth/Polygon4.git'

content_files       = ['https://www.dropbox.com/s/sghc0vmubxcmzvt/content_files.7z?dl=1', 'polygon4_content_files.7z']
project_files       = ['https://www.dropbox.com/s/e7snjoqbcz0k0qy/project_files.7z?dl=1', 'polygon4_project_files.7z']
third_party_files   = ['https://www.dropbox.com/s/37134r4975iclgo/third_party_files.7z?dl=1', 'polygon4_third_party_files.7z']

# executables
cmake = 'cmake'
git = 'git'

_7z = '7z'
curl = 'curl'

# names
polygon4 = 'Polygon4'

def main():
    base_dir = os.path.abspath(os.path.curdir) + '/'
    dir = base_dir + polygon4
    if os.path.exists(dir) == False:
        os.mkdir(dir)
        download_sources(dir)
    else:
        update_sources(dir)
    download_files(dir)
    run_cmake(dir)
    #build project
    #run editor

def download_sources(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Downloading latest sources from Github repositories')
    p = subprocess.Popen([git, 'clone', git_polygon4, '.'])
    p.communicate()
    p = subprocess.Popen([git, 'submodule', 'init'])
    p.communicate()
    p = subprocess.Popen([git, 'submodule', 'update'])
    p.communicate()
    os.chdir(old)

def update_sources(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Updating latest sources from Github repositories')
    p = subprocess.Popen([git, 'pull', 'origin', 'master'])
    p.communicate()
    p = subprocess.Popen([git, 'submodule', 'init'])
    p.communicate()
    p = subprocess.Popen([git, 'submodule', 'update'])
    p.communicate()
    os.chdir(old)

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

def download_file(url, file):
    print('Downloading file: ' + file)
    p = subprocess.Popen([curl, '-L', '-k', '-o', file, url])
    p.communicate()

def unpack_file(file):
    print('Unpacking file: ' + file)
    p = subprocess.Popen([_7z, 'x', '-o' + polygon4, file])
    p.communicate()

def download_and_unpack_file(url, file):
    if os.path.exists(third_party_files[1]) == False:
        download_file(url, file)
        unpack_file(file)

def download_files(dir):
    print('Downloading project files')
    download_and_unpack_file(project_files[0], project_files[1])
    download_and_unpack_file(content_files[0], content_files[1])
    download_and_unpack_file(third_party_files[0], third_party_files[1])

if __name__ == '__main__':
    main()