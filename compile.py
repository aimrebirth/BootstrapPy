#!/usr/bin/python3
# -*- coding: utf8 -*-

import sys

from distutils.core import setup
import py2exe

manifest = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
       <asmv3:trustInfo xmlns:asmv3="urn:schemas-microsoft-com:asm.v3">
         <asmv3:security>
           <asmv3:requestedPrivileges>
             <asmv3:requestedExecutionLevel
               level="asInvoker"
               uiAccess="false" />
           </asmv3:requestedPrivileges>
         </asmv3:security>
       </asmv3:trustInfo>
     </assembly>
'''

scripts = [
           'Bootstrap.py',
           'BootstrapUpdater.py',
           ]

def main():
    sys.argv.append('py2exe')
    for s in scripts:
        setup(
            options = { 'py2exe': {'compressed': 1, 'optimize': 1, 'bundle_files': 0 } },
            console = [{ 
                        'script': s,
                        'icon_resources': [(1, 'Bootstrap.ico')],
                        'other_resources': [(24, 1, manifest)],
                      }],
            zipfile = None
        )

if __name__ == '__main__':
    main()