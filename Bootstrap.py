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

# names
polygon4 = 'Polygon4'
data_file = '/ThirdParty/Bootstrap/Bootstrap.json'

BootstrapDownloads = 'BootstrapDownloads/'
BootstrapPrograms  = 'BootstrapPrograms/'

# executables
cmake   = 'cmake'
git     = 'git'
msbuild = r'C:\Windows\Microsoft.NET\Framework\v4.0.30319\MSBuild.exe'

_7z     = BootstrapPrograms + '7za'
curl    = BootstrapPrograms + 'curl'
uvc     = BootstrapPrograms + 'UnrealVersionSelector'

_7z_ext = '.7z'

def main():
    print_version()
    base_dir = os.path.abspath(os.path.curdir) + '/'
    dir = base_dir + polygon4
    download_dir = base_dir + BootstrapDownloads
    if os.path.exists(dir) == False:
        os.mkdir(dir)
        download_sources(dir)
    else:
        update_sources(dir)
    data = self_check(dir)
    if os.path.exists(download_dir) == False:
        os.mkdir(download_dir)
    download_files(download_dir, data)
    unpack_files(download_dir, data)
    run_cmake(dir)
    build_engine(dir)
    create_project_files(dir)
    build_project(dir)
    print('Bootstrapping is finished. You may run now Polygon4.uproject.')
    #exit(0)

def build_project(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Building Polygon4 Unreal project')
    space()
    p = subprocess.Popen([msbuild, 'Polygon4.sln', '/property:Configuration=Development Editor', '/property:Platform=Windows', '/m'])
    p.communicate()
    check_return_code(p.returncode)
    os.chdir(old)
    space()

def check_return_code(c):
    if c == 0:
        return
    space()
    print('Last bootstrap step failed')
    exit(1)

def create_project_files(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    if os.path.exists(os.path.curdir + '/Polygon4.uproject'):
        return
    print('Creating project files')
    p = subprocess.Popen([uvc, '/projectfiles', os.path.abspath(os.path.curdir) + '/Polygon4.uproject'])
    p.communicate()
    check_return_code(p.returncode)
    os.chdir(old)
    space()

def print_version():
    print('Polygon-4 Bootstrapper Version ' + str(bootstrapper_version))
    space()

def self_check(dir):
    check = 'Performing self check'
    err = 'Critical error: cannot do a self check'
    file = dir + data_file
    f = None
    try:
        f = open(file)
    except:
        print(check)
        print(err)
        print('Base file: ' + polygon4 + data_file + ' is not found!')
        exit(1)
    data = None
    try:
        data = json.load(f)
    except:
        print(check)
        print(err)
        print('Base file: ' + polygon4 + data_file + ' has errors in json structure!')
        exit(1)
    self = data['bootstrapper']
    if self['version'] != bootstrapper_version:
        print(check)
        print('FATAL ERROR:')
        print('You have wrong version of bootstrapper!')
        print('Actual version: ' + str(self['version']))
        print('Your version: ' + str(bootstrapper_version))
        print('Please, run BootstrapUpdater.exe to update the bootstrapper.')
        exit(1)
    return data

def exit(code):
    space()
    print('Press Enter to continue...')
    input()
    sys.exit(code)

def download_sources(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Downloading latest sources from Github repositories')
    p = subprocess.Popen([git, 'clone', git_polygon4, '.'])
    p.communicate()
    check_return_code(p.returncode)
    p = subprocess.Popen([git, 'submodule', 'init'])
    p.communicate()
    check_return_code(p.returncode)
    p = subprocess.Popen([git, 'submodule', 'update'])
    p.communicate()
    check_return_code(p.returncode)
    os.chdir(old)
    space()

def update_sources(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Updating latest sources from Github repositories')
    p = subprocess.Popen([git, 'pull', 'origin', 'master'])
    p.communicate()
    check_return_code(p.returncode)
    p = subprocess.Popen([git, 'submodule', 'init'])
    p.communicate()
    check_return_code(p.returncode)
    p = subprocess.Popen([git, 'submodule', 'update'])
    p.communicate()
    check_return_code(p.returncode)
    os.chdir(old)
    space()

def run_cmake(dir):
    dir = dir + '/ThirdParty/'
    file = dir + 'Engine/Win64/Engine.sln'
    if os.path.exists(file) == False:
        print('Running CMake')
        p = subprocess.Popen([cmake,
                              '-H' + dir + 'Engine',
                              '-B' + dir + 'Engine/Win64',
                              '-DBOOST_ROOT=' + dir + 'boost',
                              '-DBOOST_LIBRARYDIR=' + dir + 'boost/lib64-msvc-12.0/',
                              '-G', 'Visual Studio 12 Win64'
                              ])
        p.communicate()
        check_return_code(p.returncode)
        if os.path.exists(file) == False:
            check_return_code(1)
        space()

def build_engine(dir):
    print('Building Engine')
    space()
    #p = subprocess.Popen([msbuild, dir + '/ThirdParty/Engine/Win64/Engine.sln', '/property:Configuration=RelWithDebInfo', '/property:Platform=x64', '/m'])
    p = subprocess.Popen([cmake, '--build', dir + '/ThirdParty/Engine/Win64/', '--config', 'RelWithDebInfo'])
    p.communicate()
    check_return_code(p.returncode)
    space()

def download_file(url, file):
    print('Downloading file: ' + file)
    p = subprocess.Popen([curl, '-L', '-k', '-o', file, url])
    p.communicate()
    check_return_code(p.returncode)
    space()

def unpack_file(file, data):
    if data['downloaded'] == False:
        return
    print('Unpacking file: ' + file)
    p = subprocess.Popen([_7z, 'x', '-y', '-o' + polygon4, file])
    p.communicate()
    check_return_code(p.returncode)

def try_download_file(url, file, hash, data):
    data['downloaded'] = False
    if os.path.exists(file) == False or md5(file) != hash:
        download_file(url, file)
        data['downloaded'] = True
        if md5(file) != hash:
            print('Wrong file is located on server! Cannot proceed.')
            exit(1)

def create_7z_file_name(file):
    return polygon4 + '_' + file + _7z_ext

def download_files(dir, data):
    for d in data['files']:
        try_download_file(d['url'], dir + create_7z_file_name(d['name']), d['md5'], d)

def unpack_files(dir, data):
    for d in data['files']:
        unpack_file(dir + create_7z_file_name(d['name']), d)

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
