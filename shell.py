#!/usr/bin/env python

"""
A set of functions that tries to mimic Linux shell commands.
Mainly intended for creting multi-platform shell-like scripts.
"""

from filesystem import base_name, chdir, cwd, copy, delete, list_dir, dir_name, dir_exists, full_path, makedir, move, path_exists
from log import disable_logd
from os_utils import si_path
from stdio import print_va, print_vd
from str_utils import str_to_array




PWD = None


def basename (path: str) -> str:
    path_basename = ""

    if path_exists (path):
        path_basename = base_name (path)

    return path_basename


def cd (path: str) -> None:
    path = si_path (path)

    if dir_exists (path):
        chdir (path)
        PWD = cwd ()


def cp (source: str, destination: str) -> bool:
    return copy (source, destination)


def dirname (path: str) -> str:
    path_dirname = dir_name (path)
    return path_dirname


def echo (message: str  = "") -> None:
    if (message != None):
        print (message)


def echo_va (message: str, *vars) -> None:
    print_va (message, vars)


def echo_vd (message: str, vars) -> None:
    print_vd (message, vars)


def ls (path: str = ".") -> None:
    path = si_path (path)

    if path_exists (path):
        print (list_dir (path))


def mkdir (path: str) -> bool:
    """
    Creates the given path.
    Returns true if the path exist or if it was created.
    """
    path = si_path (path)

    if not dir_exists (path):
        makedir (path)

    return dir_exists (path)


def mv (path: str, destination: str) -> bool:
    path = si_path (path)
    destination = si_path (destination)

    return move (path, destination)


def pwd () -> None:
    print (PWD)


def realpath (path: str) -> str:
    path = si_path (path)

    path_realpath = ""

    if path_exists (path):
        path_realpath = full_path (path)

    return path_realpath


def rm (path: str, opts: str = "") -> bool:
    opts = str_to_array (opts)
    return delete (path, ("-r") in opts)




disable_logd ()
PWD = cwd ()

