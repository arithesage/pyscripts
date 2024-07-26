#!/usr/bin/env python

"""
WTF? Scripting commons??

Well... yes. I wanted to put in one file all the functions i usually use
(and those i could need) when i do scripting.

I have decided to use Python as THE scripting language for Windows, Linux
and MacOS (and even Android), so, i wanted to have all 'commands' i usually
have in BASH.

So, scripting commons is a bunch of functions that are usually handful when
you do scripting.
"""

import datetime
import hashlib
import io
from os import chdir
from os import getenv
from os import getcwd as cwd
from os import listdir
from os import makedirs
from os import remove
from os import removedirs
from os.path import isdir as dir_exists
from os.path import dirname as dir_name
from os.path import isfile as file_exists
from os.path import realpath as full_path
from os.path import join as make_path
from os.path import basename, realpath
from pathlib import Path
import shutil
from subprocess import CompletedProcess as ExecResult
from subprocess import run
import sys
from typing import Tuple




class Messages:
    """
    Here we store the most common messages
    """
    CannotOpenFileForWriting = "ERROR: Cannot open file '$[0]' for writing."
    FileNotFoundError = "ERROR: File '$[0]' doesn't exists."
    PathNotFoundError = "ERROR: Path '$[0]' doesn't exists."

    def __init__(self) -> None:
        pass


class ANSIStyle:
    class BGCOLOR:
        NONE = "0"

        BLACK = "40"
        RED = "41"
        GREEN = "42"
        YELLOW = "43"
        BLUE = "44"
        MAGENTA = "45"
        CYAN = "46"
        WHITE = "47"

        GRAY = "100"
        BRIGHT_RED = "101"
        BRIGHT_GREEN = "102"
        BRIGHT_YELLOW = "103"
        BRIGHT_BLUE = "104"
        BRIGHT_MAGENTA = "105"
        BRIGHT_CYAN = "106"
        BRIGHT_WHITE = "107"

        def __init__(self) -> None:
            pass

    class EFFECTS:
        NONE = "0"

        UNDERLINE = "5"
        BLINK = "6"

        def __init__(self) -> None:
            pass

    class FGCOLOR:
        NONE = "0"

        BLACK = "30"
        RED = "31"
        GREEN = "32"
        YELLOW = "33"
        BLUE = "34"
        MAGENTA = "35"
        CYAN = "36"
        WHITE = "37"

        GRAY = "90"
        BRIGHT_RED = "91"
        BRIGHT_GREEN = "92"
        BRIGHT_YELLOW = "93"
        BRIGHT_BLUE = "94"
        BRIGHT_MAGENTA = "95"
        BRIGHT_CYAN = "96"
        BRIGHT_WHITE = "97"

        def __init__(self) -> None:
            pass


    """
    Defines a text style with ANSI codes
    """
    def __init__(self, fgcolor=FGCOLOR.WHITE, 
                 bgcolor=BGCOLOR.BLACK, effects=[]) -> None:
        
        self.__fgcolor = fgcolor
        self.__bgcolor = bgcolor
        self.__effects = effects

    
    def fg (self):
        """
        Foreground color
        """
        return self.__fgcolor
    

    def bg (self):
        """
        Background color
        """
        return self.__bgcolor
    

    def apply (self, text=""):
        """
        Applies the style to the given text
        """
        formatted_text = (f'\033[' + str (self.__bgcolor))
        formatted_text = (";" + str (self.__fgcolor))

        if len (self.__effects > 0):
            effects = ""

            for effect in self.__effects:
                effects += str (effect)
                effects += ";"

            effects = effects.strip (';')
            formatted_text += effects

        formatted_text += text
        formatted_text += (f'\033[0m')

        return formatted_text




def ansi_style (text, fgcolor=ANSIStyle.FGCOLOR.WHITE, 
                      bgcolor=ANSIStyle.BGCOLOR.BLACK, 
                      effects=[]) -> str:
    """
    Applies an ANSIStyle to the given text.
    If text is None, an empty string will be formatted.
    """
    styled_text = ""

    if (text != None):
        style = ANSIStyle (fgcolor, bgcolor, effects)
        styled_text = style.apply (text)
    
    return styled_text



def ansi_print (text="", fgcolor=ANSIStyle.FGCOLOR.WHITE,
                         bgcolor=ANSIStyle.BGCOLOR.BLACK,
                         effects=[]):
    """
    Shortcut for print a text with an ANSIStyle
    """
    text = ansi_style (text, fgcolor, bgcolor, effects)
    print (text)


def ansi_print_va (text="", fgcolor=ANSIStyle.FGCOLOR.WHITE,
                            bgcolor=ANSIStyle.BGCOLOR.BLACK,
                            effects=[], *variables):
    
    text = ansi_style (fgcolor, bgcolor, effects)

    print_va (text, array_to_str (variables))


def ansi_print_vd (text="", fgcolor=ANSIStyle.FGCOLOR.WHITE,
                            bgcolor=ANSIStyle.BGCOLOR.BLACK,
                            effects=[], variables={}):
    
    text = ansi_style (fgcolor, bgcolor)

    print_vd (text, variables)


def append_to_file (file_path: str, data: str, 
                    append_newline:bool = True) -> bool:
    
    file_path = si_path (file_path)

    if not file_exists (file_path):
        print_va ("ERROR: File '$[0]' does not exists.", file_path)
        print ()
        return False

    file = io.open (file_path, "a")

    if (file == None):
        print_va ("ERROR: Cannot open file '$[0]' for writing.", file_path)
        print ()
        return False

    file.write (data)

    if (append_newline):
        file.write ("\n")

    file.close ()
    return True


def arg (arg_name: str) -> str:
    """
    If the command line args includes one of type 'key=value',
    and 'key' is arg_name, returns its value.

    Otherwise returns an empty string
    """

    for arg in sys.argv[1:]:
        if arg.startswith (concat (arg_name, "=")):
            return arg.split ("=")[1]
        
    return ""
    

def array_to_str (array, sep: str = " ") -> str:
    string = ""

    if (array != None) and (len (array) != 0):
        for item in array:
            string += (item + sep)

        string = string.strip (sep)

    return string


def ask_if_continue () -> bool:
    """
    Shortcut for asking user if execution must continue
    """
    return ask_yn ("Continue?")


def ask_yn (question: str) -> bool:
    """
    Shortcut for printing a question that must be answered with s|y or n.
    """
    print (question + " (s|y/n) [n]: ", end='')

    response = input ()

    print ()

    if (response == "s") or (response == "y"):
        return True

    return False


def break_path (path: str) -> Tuple[str, ...]:
    path_chunks = []

    if not str_empty (path):        
        if in_windows ():
            path = path.strip ("\\")
            path_chunks = path.split ("\\")
        else:
            path = path.strip ("/")
            path_chunks = path.split ("/")

    return tuple (path_chunks)


def cd (path: str) -> bool:
    path = si_path (path)

    if not dir_exists (path):
        print_va ("ERROR: Cannot chdir to '$[0]'. Path does not exists.")
        return False
    
    chdir (path)
    return True


def concat (*items, sep: str = "") -> str:
    """
    A simply way to concatenate múltiple items in one string.
    """
    s = ""

    for item in items:        
        if not type_of (item, str):
            item = str (item)

        s += item
        s += sep

    s = s.strip (sep)

    return s


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


def delete (path: str, recursive:bool = False) -> bool:
    path = si_path (path)

    if not (path_exists (path)):
        print ("ERROR: Path '" + path + "' doesn't exist.")
        return False

    else:
        if dir_exists (path):
            if not recursive:
                print ("ERROR: Path is a directory.", end="")
                print ("Use '-r' option to delete it entirely.")
                return False
            else:
                removedirs (path)
        else:
            remove (path)

        if path_exists (path):
            return False

        return True


def env (var_name: str) -> str:
    """
    Returns the value of the specified environment variable,
    or an empty string if does not exists.
    """
    env_var = getenv (var_name)

    if env_var == None:
        return ""
    else:
        return env_var
    

def exec (cmdline, run_from: str = None, capture_output: bool = False, 
          use_shell: bool = False) -> ExecResult:
    """
    Executes a command line.

    The command line can be an string or a list.
    If an string is passed, it will converteed to list.

    Set 'run_from' to change the current working dir.

    Enable 'use_shell' if you want to execute the
    command line through the system's shell.

    This will call shellexec.
    """

    if type_of (cmdline, str):
        cmdline = cmdline.split (" ")

    if use_shell:
        return shellexec (cmdline, run_from, capture_output)
    else:
        if capture_output:
            exec_result = run (cmdline, cwd=run_from,
                               capture_output=capture_output, 
                               text=True, shell=False)
        else:
            exec_result = run (cmdline, cwd=run_from, shell=False)

        return exec_result
    

def file_contains (file_path: str, data: str) -> bool:
    file_path = si_path (file_path)

    if not file_exists (file_path):
        print_va (Messages.FileNotFoundError, file_path)
        print ()
        return False

    file_contents = read_file (file_path)

    if str_empty (file_contents):
        return False

    return (data in file_contents)


def in_args (arg: str) -> bool:
    global argv

    for _arg in argv:
        if arg in _arg:
            return True
        
    return False


def includes_path (filename: str) -> bool:
    """
    Check if the given filename has a path before it.
    """

    if in_windows() and ("\\" in filename):
        return True
    
    if not in_windows() and ("/" in filename):
        return True
    
    return False    
    

def in_args (arg: str) -> bool:
    """
    Returns true if 'arg' is among the arguments passed from the command line.
    """
    if not arg in sys.argv[1:]:
        return False
    
    return True
    

def in_path (executable: str) -> bool:
    """
    Checks the OS PATH environment variable and returns True if the specified
    executable filename is available in one of the registered paths.
    """
    path_var = env ("PATH")

    if str_empty (path_var) or str_empty (executable):
        return False

    windows_exec_extensions = [ ".exe", ".bat", ".py" ]
    executable_extension = executable [executable.rfind("."):]

    if in_windows ():
        paths = path_var.split (";")
    else:
        paths = path_var.split (":")

    for path in paths:
        if file_exists (make_path (path, executable)):
            return True
        else:
            if in_windows() and (not executable_extension.startswith (".")):
                for ext in windows_exec_extensions:
                    if file_exists (make_path (path, (executable + ext))):
                        return True

    return False


def in_windows () -> bool:
    """
    Returns True if we are in Windows (any version)
    """
    windir = env ("WINDIR")

    if str_empty (windir):
        return False

    return True


def is_windows_exec (executable :str) -> bool:
    """
    Returns true if the specified executable filename is a Windows one
    """
    if str_empty (executable):
        return False

    if (".exe") in executable or \
       (".bat") in executable or \
       (".py") in executable:
        return True

    return False


def list_dir (path: str = ".") -> Tuple[str, ...]:
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
    
    return tuple (listdir (path))


def makedir (path: str) -> bool:
    """
    Creates the specified directory tree (not only the final part).
    Returns True if the path was created or if the path already exists.
    """
    path = si_path (path)
    makedirs (path)

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


def no_args () -> bool:
    """
    Shortcut for checking if no arguments where passed from command line
    """
    return (len (sys.argv[1:]) == 0)


def parent_dir (path: str) -> str:
    """
    Returns the parent of the given path.
    If the path does not exists, an empty string is returned.
    """
    parent = ""

    if path_exists (path):
        parent = Path (path).parent.absolute()

    return parent


def path_exists (path: str) -> bool:
    return (dir_exists (path) or file_exists (path))


def path_of (program: str) -> str:
    """
    Returns the path where the specified executable resides
    or an empty string if was not found.
    """
    _paths = paths ()

    exec_path = ""

    for p in _paths:
        exec_path = make_path (p, program)

        if file_exists (exec_path):
            break

    return exec_path


def paths ():
    """
    Returns a list of the paths registered
    in the OS PATH environment variable.
    """
    _paths = []

    path_var = env ("PATH")
    path_sep = ":"

    if in_windows ():
        path_sep = ";"

    for p in path_var.split (path_sep):
        _paths.append (p)
    
    return _paths


def pause () -> None:
    """
    Stops program's execution until enter key is pressed.
    """
    print ("Press INTRO/ENTER for continue.")
    input ()


def print_va (text: str, *variables) -> None:
    """
    Prints a message, replacing placeholders with
    the provided variables if any.

    This variant expects an array as the 'variables' object.
    Include place holders like '$[0]', '$[1]', etc. in text.
    Each one corresponds to an index of the 'variables' array.
    """    
    if (text != None):
        if (variables != None):
            if (len (variables) == 1) and type_of (variables[0], tuple):
                variables = variables[0]
            
            var_count = len (variables)
        
            for v in range (0, var_count):
                vPlaceHolder = ("$[" + str(v) + "]")

                if vPlaceHolder in text:
                    text = text.replace (vPlaceHolder, variables[v])

        print (text)


def print_vd (text: str, variables) -> None:
    """
    Prints a message, replacing placeholders with
    the provided variables if any.

    This variant expects a dictionary as the 'variables' object.
    Include place holders like '$[var_name]' in text.
    Each one corresponds to a key of the 'variables' dictionary.
    """
    if (text != None):
        if (variables != None):
            vNames = variables.keys ()

            for vName in vNames:
                vPlaceHolder = ("$[" + vName + "]")

                if vPlaceHolder in text:
                    text = text.replace (vPlaceHolder, variables[vName])
        
        print (text)


def ramdisk_path () -> str:
    """
    Returns the path to a temporal directory stored in RAM.

    It may be cleaner store temporal data here because it will
    wiped upon rebooting.
    """
    if not in_windows ():
        return "/tmp"
    else:
        # Windows do not create a RAM disk by default, as UNIX systems do,
        # so, we use the regular TEMP dir instead.
        return temp_path ()
    

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
        print_va (Messages.FileNotFoundError, file_path)
        print ()
        return False

    file_contents = read_file (file_path)

    old_text_index = file_contents.find (old_text)

    if (old_text_index == -1):
        print_va ("ERROR: String '$[0]' wasn't found in '$[1]'", 
                  old_text, file_path)
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


def shellexec (cmdline, 
               run_from: str = None, 
               capture_output: bool = True) -> ExecResult:
    
    if capture_output:
        exec_result = run (cmdline, 
                           shell=True, 
                           cwd=run_from, 
                           capture_output=capture_output, 
                           text=True)
    else:
        exec_result = run (cmdline, shell=True, cwd=run_from)

    return exec_result
    

def si_path (path: str) -> str:
    """
    Returns an OS/system independent path.
    Transforms the given path to the ones used by the current OS.    
    """
    fixed_path = ""

    if not str_empty (path):
        if in_windows ():
            fixed_path = path.replace ("/", "\\")
        else:
            fixed_path = path.replace ("\\", "/")

    return fixed_path


def str_empty (string: str) -> bool:
    """
    Returns True only if the given string isn't None OR EMPTY
    """
    return (string == None) or (string == "")


def str_to_array (string: str, sep: str = " ") -> list:
    array = []

    if (string != None) and (string != ""):
        array = string.split (sep)
    
    return array


def temp_path () -> str:
    """
    Returns the user temp dir path in this OS
    """
    if in_windows ():
        return env ("TEMP")
    else:
        return make_path (user_home(), "_tmp")
    

def test_ip (ip_address: str) -> bool:
    if str_empty (ip_address):
        print ("ERROR: IP address cannot be empty.")
        print ()
        return False
    
    print ("Trying connecting to " + ip_address + " ...")

    if in_windows ():
        exit_code = run ("ping -n 1 " + ip_address + " > NUL")
    else:
        exit_code = run ("ping -c 1 " + ip_address + " > /dev/null")

    if (exit_code != 0):
        return False

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
    

def type_of (variable: str, variable_type) -> bool:
    """
    Alias for 'isinstance'.
    Returns if a variable is of the given type.
    """
    return isinstance (variable, variable_type)

    
def user_home () -> str:
    """
    Returns the user home dir path in this OS
    """
    if in_windows ():
        return env ("USERPROFILE")
    else:
        return env ("HOME")
    

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
    
