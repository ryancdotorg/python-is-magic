#!/usr/bin/env python3
# Author: Ryan Castellucci https://rya.nc/
# SPDX-License-Identifier: 0BSD OR OR MIT-0 OR Unlicense OR CC0-1.0+

import re
import io, os, sys
import psutil, shutil, subprocess
from pathlib import Path

def real_exec(real, arg0, args, *, debug=False):
    extensions = ['']
    paths = os.environ.get('PATH', os.defpath).split(os.pathsep)
    if os.name == 'os2' and not real.suffix:
        real = Path(real.parent, real.name+'.exe')
    elif sys.platform == 'win32':
        pathext = os.environ['PATHEXT'].lower().split(os.pathsep)
        if real.suffix.lower not in pathext:
            extensions = pathext
        paths.insert(0, '')

    for e in extensions:
        for p in paths:
            f = Path(p, real, e)
            if f.is_file():
                if debug:
                    print('os.execv', f, [arg0.name, *args], file=sys.stderr)
                os.execv(f, [arg0.name, *args])

    print(f'{arg0.resolve()}: Could not find `{real.name}` in PATH!', file=sys.stderr)

compile_check = b"""
import sys
f=sys.argv[1]
try:
    compile(open(f).read(),f,'exec',dont_inherit=True)
except:
    sys.exit(1)
sys.exit(0)
"""

def py_version(filename):
    try:
        with open(filename, 'rb') as f:
            head = f.read(1024)
            if head[0:2] == b'#!':
                split = re.split(rb'\r?\n', head, 1)
                if len(split):
                    shebang = split[0].decode()
                    m = re.search(r'\b(python[23]?)\b', shebang)
                    if m:
                        py = m.group(1)
                        if py == 'python2':
                            return 2
                        elif py == 'python3':
                            return 3
                        # continue if it's just 'python'
                    else:
                        # this doesn't look like a python shebang
                        return None
            body = head + f.read()
            for version in (3, 2):
                python = f'python{version}'
                p = subprocess.run([python, '-', filename], input=compile_check)
                if p.returncode == 0:
                    return version
    except Exception as e:
        pass

    return None

arg0 = Path(sys.argv[0])
args = sys.argv[1:]

parent = psutil.Process(psutil.Process().ppid())
ancestors = (parent.name(), psutil.Process(parent.ppid()).name())

if arg0.name == 'python':
    real = 'python3'
    # check whether this is interactive use
    disallowed_options = {'-m', '-V', '-x', '-h', '--help'}
    terminating_options = {'-c', '-m', '-'}
    if ancestors[1] == 'vim':
        pass
    else:
        args_okay = True
        for a in args:
            if a in disallowed_options or not a.startswith('-'):
                args_okay = False
            elif a in terminating_options:
                break
        if not args_okay:
            cmdline = ' '.join([arg0.name, *args])
            if len(args) == 1:
                script = sys.argv[-1]
                print(f'{arg0.resolve()}: Trying to determine python version for `{script}`!', file=sys.stderr)
                version = py_version(script)
                if not version:
                    print(f'Does not seem to be a vaild python script: {script}', file=sys.stderr)
                    sys.exit(127)
                else:
                    python = f'python{version}'
                    real_exec(python, arg0, args, debug=True)
            print(f'{arg0.resolve()}: Unsure how to handle `{cmdline}`, exiting!', file=sys.stderr)
            sys.exit(127)
elif arg0.name == 'ipython':
    real = 'ipython3'
else:
    print(f'{arg0.resolve()}: No handler for {arg0.name}', file=sys.stderr)
    sys.exit(127)

real_exec(real, arg0, args)
