#!/usr/bin/env python

"""
A set of functions that tries to mimic Linux shell commands when
porting BASH scripts to Python.
"""

from scripting_commons import dir_name as dirname
from scripting_commons import move as mv
from scripting_commons import makedir as mkdir
from scripting_commons import full_path as realpath

from scripting_commons import basename, chdir, copy, cwd, list_dir,\
                              delete, dir_exists, file_exists, path_exists,\
                              print_va, si_path




PWD = None




def cd (path: str) -> None:
    path = si_path (path)

    if dir_exists (path):
        chdir (path)
        PWD = cwd ()


def cp (source: str, destination: str) -> bool:
    return copy (source, destination)


def echo (message: str  = "") -> None:
    if (message != None):
        print (message)


def echo_va (message: str, *vars) -> None:
    print_va (message, vars)


def ls (path: str = ".") -> None:
    path = si_path (path)

    if path_exists (path):
        print (list_dir (path))


def pwd () -> None:
    print (PWD)


def rm (path: str, opts: str = "") -> bool:
    opts = opts.split ()
    return delete (path, ("-r") in opts)




PWD = cwd ()

