#!/usr/bin/env python

"""
OS related functions.
"""

import os
import subprocess

from lang import *
from log import *
from str_utils import array_to_str, str_empty




class ProcessResult:
    def __init__(self, exit_code: int, output: str) -> None:
        self.__exit_code = exit_code
        self.__output = output
        self.__output_lines = output.split ("\n")

    def exit_code (self) -> int:
        return self.__exit_code

    def failed (self) -> bool:
        """
        The process exited returning anything but 0
        """
        return (self.__exit_code != 0)

    def ok (self) -> bool:
        """
        The process exited returning 0
        """
        return (self.__exit_code == 0)

    def output (self) -> str:
        return self.__output
    
    def output_lines (self) -> Tuple:
        return self.__output_lines
    

def env (var_name: str) -> str:
    """
    Returns the value of the specified environment variable,
    or an empty string if does not exists.
    """
    env_var = os.getenv (var_name)

    if env_var == None:
        return ""
    else:
        return env_var    


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
        if os.path.isfile (os.path.join (path, executable)):
            return True
        else:
            if in_windows() and (not executable_extension.startswith (".")):
                for ext in windows_exec_extensions:
                    if os.path.isfile (os.path.join (path, (executable + ext))):
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


def paths ():
    """
    Returns a list of the paths registered in the OS PATH environment variable.
    """
    _paths = []

    path_var = env ("PATH")
    path_sep = ":"

    if in_windows ():
        path_sep = ";"

    for p in path_var.split (path_sep):
        _paths.append (p)
    
    return _paths


def path_of (program: str) -> str:
    """
    Returns the path where the specified executable resides
    or an empty string if was not found.
    """
    _paths = paths ()

    exec_path = ""

    for p in _paths:
        exec_path = os.path.join (p, program)

        if os.path.isfile (exec_path):
            break

    return exec_path


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


def run (cmdline) -> ProcessResult:
    """
    Shortcut for executing a command line without changing the current working dir
    and without capturing the output (it will be printed to stdout).

    The command line can be specified as an array or as a string.
    """
    return run_program (cmdline)


def run_quietly (cmdline) -> ProcessResult:
    """
    Shortcut for executing a command line without changing the current working dir
    and capturing the output (it will NOT be printed to stdout).

    The command line can be specified as an array or as a string.
    """
    return run_program (cmdline, ".", True)


def run_from (cmdline, working_dir: str) -> ProcessResult:
    """
    Shortcut for executing a command line with a custom working dir and without
    capturing the output (it will be printed to stdout).

    The command line can be specified as an array or as a string.
    """
    return run_program (cmdline, working_dir)


def run_from_quietly (cmdline, working_dir: str) -> ProcessResult:
    """
    Shortcut for executing a command line with a custom working dir and
    capturing the output (it will NOT be printed to stdout).

    The command line can be specified as an array or as a string.
    """
    return run_program (working_dir, True)


def run_program (cmdline, working_dir: str = ".", get_output: bool = False) -> ProcessResult:
    """
    Executes the given command line, optionally from 'working_dir'.
    The command line can be specified as an array or as a string.
    Returns a dictionary containing the exit_code and the output.
    
    Set 'get_output' to True if you want to capture output instead
    or showing it. In this case, the output key of the dictionary
    will be an empty string.
    """

    if (working_dir != "."):
        working_dir = si_path (working_dir)
   
    if type_of (cmdline, list):
        cmdline = array_to_str (cmdline)
    
    command = cmdline.split()[0]
    
    # If the executable is in the current directory...
    if os.path.isfile (os.path.join (".", command)):

        # Let's update the command with it's full path
        command = os.path.realpath (command)

    # If is being invoked as a command...    
    elif (not ("/") in command) and (not ("\\") in command):

        # ... and it isn't in PATH, we cannot execute anything
        if not in_path (command):
            print ("ERROR: The executable '" + command + "' is not in PATH and isn't in the current dir.'")
            print ()

            return ProcessResult (255, "")
        

    log_d ("Running '" + cmdline + "' from " + str (working_dir) + " ...")
    log_d ()

    if get_output:
        process = subprocess.run (cmdline, shell=True, stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT, cwd=working_dir, text=True)
    else:
        process = subprocess.run (cmdline, shell=True, cwd=working_dir)
    
    if not get_output:
        return ProcessResult (process.returncode, "")
    else:
        return ProcessResult (process.returncode, process.stdout)
    

def si_path (path: str) -> str:
    """
    Creates a System Independent Path.
    Really, this transforms the given path to the ones used by the current OS.
    The name is an attempt to differenciate the function name from the variables.
    """
    fixed_path = ""

    if not str_empty (path):
        if in_windows ():
            fixed_path = path.replace ("/", "\\")
        else:
            fixed_path = path.replace ("\\", "/")

    return fixed_path


def temp_path () -> str:
    """
    Returns the user temp dir path in this OS
    """
    if in_windows ():
        return env ("TEMP")
    else:
        return os.path.join (user_home(), "_tmp")


def user_home () -> str:
    """
    Returns the user home dir path in this OS
    """
    if in_windows ():
        return env ("USERPROFILE")
    else:
        return env ("HOME")



disable_logd ()

