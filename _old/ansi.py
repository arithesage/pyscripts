#!/bin/bash

from stdio import print_va
from stdio import print_vd
from str_utils import array_to_str




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


class ANSIStyle:
    """
    Defines a text style with ANSI codes
    """
    def __init__(self, fgcolor=FGCOLOR.WHITE, bgcolor=BGCOLOR.BLACK, effects=[]) -> None:
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
#        formatted_text = (f'\033[' + self.__bgcolor + f';' + self.__fgcolor + f'm')
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




def ansi_style (text, fgcolor=FGCOLOR.WHITE, bgcolor=BGCOLOR.BLACK, effects=[]) -> str:
    """
    Applies an ANSIStyle to the given text.
    If text is None, an empty string will be formatted.
    """
    styled_text = ""

    if (text != None):
        style = ANSIStyle (fgcolor, bgcolor, effects)
        styled_text = style.apply (text)
    
    return styled_text



def ansi_print (text="", fgcolor=FGCOLOR.WHITE, bgcolor=BGCOLOR.BLACK, effects=[]):
    """
    Shortcut for print a text with an ANSIStyle
    """
    text = ansi_style (text, fgcolor, bgcolor, effects)
    print (text)


def ansi_print_va (text="", fgcolor=FGCOLOR.WHITE, bgcolor=BGCOLOR.BLACK, effects=[], *variables):
    text = ansi_style (fgcolor, bgcolor, effects)

    print_va (text, array_to_str (variables))


def ansi_print_vd (text="", fgcolor=FGCOLOR.WHITE, bgcolor=BGCOLOR.BLACK, effects=[], variables={}):
    text = ansi_style (fgcolor, bgcolor)

    print_vd (text, variables)


