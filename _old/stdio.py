#!/usr/bin/env python

from lang import type_of
from str_utils import array_to_str




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


def print_va (text: str, *variables) -> None:
    """
    Prints a message, replacing placeholders with the provided variables if any.
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
    Prints a message, replacing placeholders with the provided variables if any.
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


def pause () -> None:
    """
    Stops program's execution until enter key is pressed.
    """
    print ("Press INTRO/ENTER for continue.")
    input ()

