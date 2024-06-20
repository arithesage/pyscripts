#!/usr/bin/env python


def array_to_str (array, sep: str = " ") -> str:
    string = ""

    if (array != None) and (len (array) != 0):
        for item in array:
            string += (item + sep)

        string = string.strip (sep)

    return string


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


