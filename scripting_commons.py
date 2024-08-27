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
import json
import platform
import shutil
import sys
import zipfile

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

from subprocess import CompletedProcess, PIPE, STDOUT
from subprocess import run

from typing import Dict
from typing import Tuple

from zipfile import ZipFile

import wget




class ExecResult:
    ok = False
    return_code = -1
    stdout = ""
    stderr = ""

    def __init__(self, completed_process: CompletedProcess) -> None:
        ExecResult.stderr = completed_process.stderr
        ExecResult.stdout = completed_process.stdout
        ExecResult.return_code = completed_process.returncode
        ExecResult.ok = (completed_process.returncode == 0)
        

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



class CHARS:
    """
    Unicode characters hex codes. I don't plan to put the whole table here,
    only those characters that i use commonly.
    """
    DOTS_LOW = 0x2591
    DOTS_MEDIUM = 0x2592
    DOTS_HIGH = 0x2593
    BLACK = 0x2590
    FRAME_H_LINE = 0x2550
    FRAME_BOTTOM_LEFT = 0x255A
    FRAME_BOTTOM_RIGHT = 0x255D
    FRAME_T = 0x2566
    FRAME_T_90 = 0x2563
    FRAME_T_180 = 0x2569
    FRAME_T_270 = 0x2560
    FRAME_TOP_LEFT = 0x2554
    FRAME_TOP_RIGHT = 0x2557
    FRAME_V_LINE = 0x2551
    SPACE = 0x0020

    def __init__(self) -> None:
        pass




last_exec_exit_code = -1


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


def cls () -> None:
    """
    Clears the terminal
    """
    print (f"\033[2J")
    print (f"\033[H")


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
    

def download (url: str, destination: str = ".") -> bool:
    """
    Downloads a file using the wget module.
    Destination, is given, is the destination dir, without filename.
    """
    
    if (destination == "."):
        destination = cwd ()
    
    file_name = basename (url)
    destination = make_path (destination, file_name)

    print_va ("Downloading '$[0]'...", file_name)
    
    try:
        wget.download (url, destination)
        return True
    except:
        return False
    

def draw (char_code: int, new_line: bool = False) -> str:
    """
    'Draws' characters in the terminal. This is mainly intended for writing
    characters like those to draw boxes and another symbols with their
    unicode character code.
    """
    if not new_line:
        print (chr (char_code), end="")
    else:
        print (chr (char_code))


def draw_framed_text (text: str, margin: int = 1) -> str:
    text_lines = text.split ("\n")
    
    text_w = 0
    text_h = len (text_lines)
    frame = 1

    for line in text_lines:
        line_w = len (line)

        if (line_w > text_w):
            text_w = line_w

    columns = (text_w + frame)
    lines = (text_h + frame)

    last_column = (columns - 1)
    last_line = (lines - 1)

    for l in range (0, lines):
        for c in range (0, columns):
            if (l == 0):
                if (c == 0):
                    draw (CHARS.FRAME_TOP_LEFT)
                elif (c == last_column):
                    draw (CHARS.FRAME_TOP_RIGHT, True)
                else:
                    draw (CHARS.FRAME_H_LINE)

            elif (l == last_line):
                if (c == 0):
                    draw (CHARS.FRAME_BOTTOM_LEFT)
                elif (c == last_column):
                    draw (CHARS.FRAME_BOTTOM_RIGHT, True)
                else:
                    draw (CHARS.FRAME_H_LINE)

            else:
                if (c == 0):
                    draw (CHARS.FRAME_V_LINE)
                elif (c == last_column):
                    draw (CHARS.FRAME_V_LINE, True)
                else:
                    print (text_lines[l - 1][c])
    #                draw (CHARS.SPACE)



def draw_message (text: str) -> None:
    pass


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
        if (type_of (cmdline, tuple)):
            cmdline_str = ""

            for chunk in cmdline:
                cmdline_str += chunk
                cmdline_str += " "

            cmdline = cmdline_str.strip()

            return shellexec (cmdline, run_from, capture_output)
    else:
        if capture_output:
            exec_result = run (cmdline, cwd=run_from,
                               stdout=PIPE, stderr=STDOUT,
                               text=True)
        else:
            exec_result = run (cmdline, cwd=run_from)

        return ExecResult (exec_result)
    

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


def file_ext (file_path: str) -> str:
    """
    Returns the extension of the given file path (example: .txt).
    If not exists or do not have extension, returns an empty string.
    """
    extension = ""

    if file_exists (file_path):
        filename = basename (file_path)

        if (".") in filename:
            extension = Path (file_path).suffix

    return extension


def file_is_32bit_exec (file_path: str) -> bool:
    if file_exists (file_path):
        exec_result = exec (["file", file_path], capture_output=True)
    
        if ("Intel 80386") in exec_result.stdout:
            return True
        
    return False


def file_is_64bit_exec (file_path: str) -> bool:
    if file_exists (file_path):
        exec_result = exec (["file", file_path], capture_output=True)
    
        if ("x86-64") in exec_result.stdout:
            return True
        
    return False


def from_json (source: str) -> Dict:
    """
    Reads a JSON file (or a JSON string) and returns
    a dictionary with the loaded data
    """

    if source.startswith ("{"):
        obj = json.loads (source)
        
        if (obj != None):
            return obj
        
    elif file_exists (source):
        file_data = read_file (source)

        if not str_empty (file_data):
            obj = json.loads (file_data)

            if (obj != None):
                return obj
    return None


def has_path (filename: str) -> bool:
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


def in_linux () -> bool:
    """
    Returns True if we are in Linux (any version)
    """
    return (platform.system().lower() == "linux")


def in_macos () -> bool:
    """
    Returns True if we are in MacOS (any version)
    """
    return (platform.system().lower() == "darwin")


def in_windows () -> bool:
    """
    Returns True if we are in Windows (any version)
    """
    return (platform.system().lower() == "windows")
    # windir = env ("WINDIR")

    # if str_empty (windir):
    #     return False

    # return True


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


def last_exit_code () -> int:
    global last_exec_exit_code
    return last_exec_exit_code


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


def os_arch () -> str:
    return platform.machine()


def os_name () -> str:
    return platform.system().lower()


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
    """
    As exec, executes a command line, but this time it uses the shell
    for doing it. And because this, the command line must be provided
    as a string.

    If an array is provided, it will be converted to an string.
    """

    if not type_of (cmdline, str):
        cmdline = array_to_str (cmdline)
    
    if capture_output:
        exec_result = run (cmdline, 
                           shell=True, 
                           cwd=run_from, 
                           stdout=PIPE,
                           stderr=STDOUT,
                           text=True)
    else:
        exec_result = run (cmdline, shell=True, cwd=run_from)

    return ExecResult (exec_result)


def shellexec_int (cmdline, run_from: str = None) -> None:    
    """    
    Is the same as calling shellexec without capturing output and
    ignoring the returning object. More like the system() C function.

    As nothing is returned, the cmdline exit code is accessed with
    last_exit_code function.
    """

    global last_exec_exit_code

    result = shellexec (cmdline, run_from, False)
    last_exec_exit_code = result.return_code
    

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


def temp_path () -> str:
    """
    Returns the user temp dir path in this OS
    """
    if in_windows ():
        return env ("TEMP")
    else:
        return make_path (user_home(), "_tmp")
    

def test_ip (ip_address: str) -> bool:
    """
    Calls ping command line program to test if a IP address is reachable
    """
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


def to_json (obj: any) -> str:
    """
    Serializes an object to a JSON string
    """
    
    if (obj != None):
        json_data = json.dumps (obj)

        if (json_data != None) and not str_empty (json_data):
            return json_data
    
    return None


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
    

def write_file (file_path: str, data: str, append: bool = False, 
                append_new_line: bool = True) -> bool:
    """
    Writes data to file.
    If appending, append_to_file will be called instead.
    """

    if append:
        return append_to_file (file_path, data, append_new_line)

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


def zip_contents (zip_path: str) -> Tuple[str, ...]:
    """
    Returns a list with all files found in a ZIP file.
    """
    if file_exists (zip_path) and zipfile.is_zipfile (zip_path):
        contents = []

        with ZipFile (zip_path, "r") as zip:
            for entry in zip.filelist:
                contents.append (entry.filename)

        return contents


# DEBUGGING zone

#draw_frame (5, 3)
#l = zip_contents ("/home/javier/Descargas/ddwrapper.zip")
#print (l)