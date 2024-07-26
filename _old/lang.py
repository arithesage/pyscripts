#!/usr/bin/env python

import sys

from typing import Tuple


argv = []
__argsd = None


def arg (arg_name: str) -> str:
    """
    For an argument of type '[-|--]arg_name=value', obtain its value.
    If nothing is found, an empty string is returned.
    """
    value = ""

    if in_args (arg_name):
        for _arg in sys.argv[1:]:
            if arg_name in _arg:
                if ("=") in _arg:
                    value = _arg.split ("=")[1]

    return value


def args (arg_name: str) -> str:
    """
    Returns the value of the command line argument 'arg_name'.
    
    Before this, and if this is the first time the function is called,
    it will create a dictionary (__argv) with all '[-|--]arg=value' found
    arguments.
    """
    global __argsd

    arg_value = ""

    if __argsd == None:
        __argsd = {}
        
        if (len (sys.argv[1:]) > 0):
            for arg in sys.argv[1:]:
                if ("=") in arg:
                    _arg = arg.split ("=")
                    __argsd [_arg[0]] = _arg[1]

    if arg_name in __argsd.keys:
        arg_value = __argsd [arg_name]

    return arg_value


def executing () -> bool:
    global argv

    """
    Returns if the current script is being executed.

    Also, if True, pupulates 'argv' list with the received args from
    the command line.
    """
    
    if (__name__ != "__main__"):
        return False
    else:
        argv = sys.argv[1:]
        return True


def in_args (arg: str) -> bool:
    """
    Returns true if 'arg' is among the arguments passed from the command line.
    """
    if not str in sys.argv[1:]:
        return False
    
    return True


def module_functions (loaded_module) -> Tuple[str]:
    """
    Returns a list with the name of the functions found in 'loaded_module'.
    Only user-made functions will be returned.
    """
    func_names = []

    if loaded_module != None:
        for func in dir (loaded_module):
            if not func.startswith ("__") and not func.endswith ("__"):
                func_names.append (func)

    return func_names


def no_args () -> bool:
    """
    Shortcut for checking if no arguments where passed from command line
    """
    return (len (sys.argv[1:]) == 0)


def type_of (variable: str, variable_type) -> bool:
    """
    Alias for 'isinstance'.
    Returns if a variable is of the given type.
    """
    return isinstance (variable, variable_type)


