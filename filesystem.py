#!/usr/bin/env python

from datetime import datetime
import hashlib
import io
import shutil
from typing import Tuple
import os

from os_utils import in_windows, si_path, ramdisk_path
from stdio import print_va
from str_utils import *




class Messages:
    CannotOpenFileForWriting = "ERROR: Cannot open file '$[0]' for writing."
    FileNotExists = "ERROR: File '$[0]' do not exists."
    StringNotFound = "ERROR: Didn't find any occurrence of '$[0]' in '$[1]'."

    def __init__ (self):
        pass




def append_to_file (file_path: str, data: str, append_newline:bool = True) -> bool:
    file_path = si_path (file_path)

    if not file_exists (file_path):
        print_va (Messages.FileNotExists, file_path)
        print ()
        return False

    file = io.open (file_path, "a")

    if (file == None):
        print_va (Messages.CannotOpenForWriting, file_path)
        print ()
        return False

    file.write (data)

    if (append_newline):
        file.write ("\n")

    file.close ()
    return True


def base_name (path: str) -> str:
    path = si_path (path)

    path_basename = ""

    if path_exists (path):
        path_basename = os.path.basename (path)

    return path_basename


def break_path (path: str) -> Tuple[str]:
    path_chunks = []

    if not str_empty (path):        
        if in_windows ():
            path = path.strip ("\\")
            path_chunks = path.split ("\\")
        else:
            path = path.strip ("/")
            path_chunks = path.split ("/")

    return path_chunks


def chdir (path: str) -> bool:
    path = si_path (path)

    if not dir_exists (path):
        print_va ("ERROR: Cannot chdir to '$[0]'. Path does not exists.")
        return False
    
    os.chdir (path)
    return True


def copy (source: str, destination: str) -> bool:
    source = si_path (source)
    destination = si_path (destination)

    if not path_exists (source):
        print_va ("ERROR: Copying '$[0]' failed. Does not exists.", source)
        return False
    
    if not dir_exists (source):
        shutil.copy2 (source, destination)
    else:
        shutil.copytree (source, destination)

    if not path_exists (destination):
        return False

    return True


def cwd () -> str:
    """
    Returns the current working directory
    """
    return os.getcwd ()


def delete (path: str, recursive:bool = False) -> bool:
    path = si_path (path)

    if not (path_exists (path)):
        print ("ERROR: Path '" + path + "' doesn't exist.")
        return False

    else:
        if os.path.isdir (path):
            if not recursive:
                print ("ERROR: Path is a directory. Use '-r' option to delete it entirely.")
                return False
            else:
                os.removedirs (path)
        else:
            os.remove (path)

        if path_exists (path):
            return False

        return True


def dir_exists (path: str) -> bool:
    path = si_path (path)

    if (path != None) and (path != ""):
        return os.path.isdir (os.path.realpath (path))


def dir_name (path: str) -> str:
    path = si_path (path)
    return os.path.dirname (path)


def file_contains (file_path: str, data: str) -> bool:
    file_path = si_path (file_path)

    if not file_exists (file_path):
        print_va (Messages.FileNotExists, file_path)
        print ()
        return False

    file_contents = read_file (file_path)

    if str_empty (file_contents):
        return False

    return (data in file_contents)


def file_exists (path: str) -> bool:
    path = si_path (path)

    if (path != None) and (path != ""):
        return os.path.isfile (os.path.realpath (path))


def full_path (path: str) -> str:
    path = si_path (path)
    real_path = ""

    if not str_empty (path) and path_exists (path):
        real_path = os.path.realpath (path)

    return real_path


def list_dir (path: str = ".") -> Tuple[str]:
    """
    Returns the contents of the given path or an empty tuple
    if path does not exists.

    If no path is given, current path is read.
    """
    path = si_path (path)

    empty_dir = ()

    if str_empty (path) or not dir_exists (path):
        print_va ("ERROR: Path '$[0]' does not exists.", path)
        return empty_dir
    
    return os.listdir (path)


def makedir (path: str) -> bool:
    """
    Creates the specified directory tree (not only the final part).
    Returns True if the path was created or if the path already exists.
    """
    path = si_path (path)
    os.makedirs (path)

    if not dir_exists (path):
        print_va ("ERROR: Path '$[0]' could not be created.")
        return False
    
    return True


def make_tempdir () -> str:
    """
    Creates a temporal dir and returns its path.
    If the directory cannot be created, it returns an empty string.
    """
    tempdir_path = ""

    now_microseconds = datetime.now().microsecond
    now_microseconds_byte_str = str (now_microseconds).encode ()

    hash = hashlib.sha1 ()
    hash.update (now_microseconds_byte_str)

    temp_path = make_path (ramdisk_path(), str(hash.hexdigest()))

    makedir (temp_path)

    if dir_exists (temp_path):
        tempdir_path = temp_path

    return tempdir_path


def make_path (*path_chunks: Tuple[str]) -> str:
    path = ""

    if (path_chunks != None) and (len (path_chunks) > 0):
        for chunk in path_chunks:
            if in_windows ():
                chunk = chunk.strip ("\\")
            else:
                chunk = chunk.strip ("/")

            path = os.path.join (path, chunk)

    return path


def move (source: str, destination: str) -> bool:
    source = si_path (source)
    destination = si_path (destination)

    if not path_exists (source):
        print_va ("ERROR: Cannot move '$[0]'. Path does not exists.", source)
        return False
    
    moved = shutil.move (source, destination)

    if (moved == None) or not path_exists (moved):
        return False
    
    return True


def path_exists (path: str) -> bool:
    return (dir_exists (path) or file_exists (path))


def read_file (file_path: str) -> str:
    file_path = si_path (file_path)

    file_contents = ""

    if file_exists (file_path):
        file = io.open (file_path, "r")

        if (file != None):
            file_contents = file.read ()
            file.close ()

    return file_contents


def replace_all_in (old_text: str, new_text: str, file_path: str) -> bool:
    file_path = si_path (file_path)

    if not (file_exists (file_path)):
        print_va (Messages.FileNotExists, file_path)
        print ()
        return False

    file_contents = read_file (file_path)

    old_text_index = file_contents.find (old_text)

    if (old_text_index == -1):
        print_va (Messages.StringNotFound, old_text, file_path)
        print ()
        return False

    file_contents = file_contents.replace (old_text, new_text)
    file = io.open (file_path, "w")

    if (file == None):
        print_va (Messages.CannotOpenFileForWriting, file_path)
        print ()
        return False

    file.write (file_contents)
    file.close ()

    return True


def test_rw (path: str) -> bool:
    """
    Tests if we have write permissions in path
    """
    path = si_path (path)

    # If a file path is received, obtain the parent's path.
    if file_exists (path):
        path = dir_name (path)
    
    if not dir_exists (path):
        return False
    
    file_path = make_path (path, "touched")

    if not write_file (file_path, ""):
        return False
    else:
        delete (file_path)
        return True
    

def write_file (file_path: str, data: str) -> bool:
    if str_empty (file_path):
        return False
    
    file_path = si_path (file_path)

    file = io.open (file_path, "w")

    if (file == None):
        print_va (Messages.CannotOpenFileForWriting, file_path)
        print ()
        return False

    file.write (data)
    file.close ()
    return True


