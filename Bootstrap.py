#!/usr/bin/python3
# -*- coding: utf8 -*-

from distutils import dir_util
import hashlib
import json
import os
import shutil
import subprocess
import sys

# version
bootstrapper_version = 3

# links
git_polygon4 = 'https://github.com/aimrebirth/Polygon4.git'

# names
polygon4 = 'Polygon4'
data_file = '/ThirdParty/Bootstrap/Bootstrap.json'
inet_data_file = 'https://raw.githubusercontent.com/aimrebirth/Bootstrap/master/Bootstrap.json'
inet_src_file = 'https://raw.githubusercontent.com/aimrebirth/Bootstrap/master/Sources.json'
src_file = 'Sources.json'
github_repo = 'https://github.com/aimrebirth/{0}/archive/master.zip'
master_suffix = '-master'

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
zip_ext = '.zip'

def main():
    print_version()
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

def manual_download():
    file = BootstrapDownloads + src_file
    download_file(inet_src_file, file)
    data = load_json(file)
    for r in data['repositories']:
        url = github_repo.format(r['name'])
        file = BootstrapDownloads + r['name'] + master_suffix + zip_ext
        download_file(url, file)
    for r in data['repositories']:
        dir = BootstrapDownloads + r['name'] + master_suffix
        file = dir + zip_ext
        r['downloaded'] = True
        unpack_file(file, r, BootstrapDownloads)
        src = BootstrapDownloads + r['name'] + master_suffix
        dst = polygon4
        if r['name'] != 'Polygon4':
            dst = dst + '/' + r['unpack_dir'] + '/' + r['name']
        dir_util.copy_tree(src, dst)

def has_program_in_path(prog):
    try:
        execute_command([prog], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    except:
        print('Warning: "' + prog + '" is missing in your PATH environment variable')
        return False
    return True

def build_project(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Building Polygon4 Unreal project')
    space()
    execute_command([msbuild, 'Polygon4.sln', '/property:Configuration=Development Editor', '/property:Platform=Windows', '/m'])
    os.chdir(old)
    space()

def check_return_code(c):
    if c == 0:
        return
    space()
    print('Last bootstrap step failed')
    exit(1)

def create_project_files(dir):
    if os.path.exists(os.path.curdir + '/Polygon4.sln'):
        return
    print('Creating project files')
    execute_command([uvc, '/projectfiles', dir + '/Polygon4.uproject'])
    space()

def print_version():
    print('Polygon-4 Bootstrapper Version ' + str(bootstrapper_version))
    space()

def load_json(file):
    f = None
    try:
        f = open(file)
    except:
        print(check)
        print(err)
        print('Json file: ' + file + ' is not found!')
        exit(1)
    data = None
    try:
        data = json.load(f)
    except:
        print(check)
        print(err)
        print('Json file: ' + file + ' has errors in its structure!')
        exit(1)
    return data

def self_check(file):
    check = 'Performing self check'
    err = 'Critical error: cannot do a self check'
    data = load_json(file)
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
    execute_command([git, 'clone', git_polygon4, '.'])
    if os.path.exists('.git') == False:
        execute_command([git, 'init'])
        execute_command([git, 'remote', 'add', 'origin', git_polygon4])
        execute_command([git, 'fetch'])
        execute_command([git, 'reset', 'origin/master', '--hard'])
    download_submodules()
    os.chdir(old)
    space()

def update_sources(dir):
    old = os.path.abspath(os.path.curdir)
    os.chdir(dir)
    print('Updating latest sources from Github repositories')
    execute_command([git, 'pull', 'origin', 'master'])
    download_submodules()
    os.chdir(old)
    space()

def download_submodules():
    execute_command([git, 'submodule', 'init'])
    execute_command([git, 'submodule', 'update'])

def run_cmake(dir):
    dir = dir + '/ThirdParty/'
    file = dir + 'Engine/Win64/Engine.sln'
    if os.path.exists(file) == False:
        print('Running CMake')
        execute_command([cmake,
                            '-H' + dir + 'Engine',
                            '-B' + dir + 'Engine/Win64',
                            '-DBOOST_ROOT=' + dir + 'boost',
                            '-DBOOST_LIBRARYDIR=' + dir + 'boost/lib64-msvc-12.0/',
                            '-G', 'Visual Studio 12 Win64'
                            ])
        if os.path.exists(file) == False:
            check_return_code(1)
        space()

def build_engine(dir):
    print('Building Engine')
    space()
    execute_command([cmake, '--build', dir + '/ThirdParty/Engine/Win64/', '--config', 'RelWithDebInfo'])
    space()

def download_file(url, file):
    print('Downloading file: ' + file)
    execute_command([curl, '-L', '-k', '-o', file, url])
    space()

def unpack_file(file, data, output_dir):
    if data['downloaded'] == False:
        if 'check_path' in data and os.path.exists(polygon4 + '/' + data['check_path']) == False:
            pass
        else:
            return
    print('Unpacking file: ' + file)
    execute_command([_7z, 'x', '-y', '-o' + output_dir, file])

def try_download_file(url, file, hash, data):
    data['downloaded'] = False
    if os.path.exists(file) == False or md5(file) != hash:
        download_file(url, file)
        data['downloaded'] = True
        if md5(file) != hash:
            print('Wrong file is located on server! Cannot proceed.')
            exit(1)

def download_files(dir, data):
    for d in data['files']:
        try_download_file(d['url'], dir + data['file_prefix'] + d['name'], d['md5'], d)

def unpack_files(dir, data):
    for d in data['files']:
        unpack_file(dir + data['file_prefix'] + d['name'], d, polygon4)

def md5(file):
    md5 = hashlib.md5()
    f = open(file, mode = 'rb')
    while True:
        data = f.read(2 ** 20)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()

def execute_command(args, bufsize=-1, executable=None,
                    stdin=None, stdout=None, stderr=None,
                    preexec_fn=None, close_fds=subprocess._PLATFORM_DEFAULT_CLOSE_FDS,
                    shell=False, cwd=None, env=None, universal_newlines=False,
                    startupinfo=None, creationflags=0,
                    restore_signals=True, start_new_session=False,
                    pass_fds=()):
    p = subprocess.Popen(
                    args, bufsize, executable,
                    stdin, stdout, stderr,
                    preexec_fn, close_fds,
                    shell, cwd, env, universal_newlines,
                    startupinfo, creationflags,
                    restore_signals, start_new_session,
                    pass_fds)
    p.communicate()
    check_return_code(p.returncode)

def space():
    print()

if __name__ == '__main__':
    main()
