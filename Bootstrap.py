#!/usr/bin/python3
# -*- coding: utf8 -*-

import hashlib
import json
import os
import subprocess
import sys

# version
bootstrapper_version = 1

# links
git_polygon4 = 'https://github.com/aimrebirth/Polygon4.git'

# executables
cmake   = 'cmake'
git     = 'git'
#devenv  = 'C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\Common7\\IDE\\devenv.com'

_7z = '7z'
curl = 'curl'

_7z_ext = '.7z'

# names
polygon4 = 'Polygon4'
data_file = '/ThirdParty/Bootstrap/Bootstrap.json'

def main():
    base_dir = os.path.abspath(os.path.curdir) + '/'
    dir = base_dir + polygon4
    if os.path.exists(dir) == False:
        os.mkdir(dir)
        download_sources(dir)
    else:
        update_sources(dir)
    space()
    data = self_check(dir)
    space()
    download_files(dir, data)
    space()
    unpack_files(dir, data)
    space()
    run_cmake(dir)
    space()
    build_engine(dir)
    #build project
    #run editor

def self_check(dir):
    print('Performing self check')
    err = 'Critical error: cannot do a self check'
    file = dir + data_file
    f = None
    try:
        f = open(file)
    except:
        print(err)
        print('Base file: ' + polygon4 + data_file + ' is not found!')
        sys.exit(1)
    data = None
    try:
        data = json.load(f)
    except:
        print(err)
        print('Base file: ' + polygon4 + data_file + ' has errors in json structure!')
        sys.exit(1)
    self = data['bootstrapper']
    if self['version'] < bootstrapper_version:
        print(err)
        print('You are in the future! The version of your bootstrapper is higher than maximum possible.')
        sys.exit(1)
    if self['version'] > bootstrapper_version:
        print('WARNING:')
        print('There are newer version (' + str(self['version']) + ') of bootstrapper.')
        print('Your version is (' + str(bootstrapper_version) + ').')
        print('Please, download it as soon as possible.')
    return data

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
    dir = dir + '/ThirdParty/'
    if os.path.exists(dir + 'Engine/Win64') == False:
        print('Running CMake')
        p = subprocess.Popen([cmake,
                              '-H' + dir + 'Engine',
                              '-B' + dir + 'Engine/Win64',
                              '-DBOOST_ROOT=' + dir + 'boost',
                              '-DBOOST_LIBRARYDIR=' + dir + 'boost/lib64-msvc-12.0/',
                              '-G', 'Visual Studio 12 Win64'
                              ])
        p.communicate()

def build_engine(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir + '/ThirdParty/Engine')
    print('Building Engine')
    p = subprocess.Popen([cmake, '--build', 'Win64', '--config', 'RelWithDebInfo'])
    p.communicate()
    os.chdir(old)

def download_file(url, file):
    print('Downloading file: ' + file)
    p = subprocess.Popen([curl, '-L', '-k', '-o', file, url])
    p.communicate()

def unpack_file(file, data):
    if data['downloaded'] == False:
        return
    print('Unpacking file: ' + file)
    p = subprocess.Popen([_7z, 'x', '-y', '-o' + polygon4, file])
    p.communicate()

def try_download_file(url, file, hash, data):
    data['downloaded'] = False
    if os.path.exists(file) == False or md5(file) != hash:
        download_file(url, file)
        data['downloaded'] = True
        if md5(file) != hash:
            print('Wrong file is located on server! Cannot proceed.')
            sys.exit(1)

def create_7z_file_name(file):
    return polygon4 + '_' + file + _7z_ext

def download_files(dir, data):
    print('Trying to download new files')
    for d in data['files']:
        try_download_file(d['url'], create_7z_file_name(d['name']), d['md5'], d)

def unpack_files(dir, data):
    print('Unpacking files')
    for d in data['files']:
        unpack_file(create_7z_file_name(d['name']), d)

def md5(file):
    md5 = hashlib.md5()
    f = open(file, mode = 'rb')
    while True:
        data = f.read(2 ** 20)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def space():
    print()

if __name__ == '__main__':
    main()