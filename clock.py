#!/usr/bin/env python

from timer import Timer




class Clock:
    def __init__(self) -> None:
        self.__ticker = Timer (1.0, -1, self.__tick)
        self.__reset ()        


    def on (self) -> None:
        """
        Enables the clock
        """
        self.__on = True
        self.__ticker.start ()


    def off (self) -> None:
        """
        Disables the clock
        """
        self.__on = False
        self.__ticker.stop ()


    def __reset (self) -> None:
        self.__h = 0
        self.__m = 0
        self.__s = 0


    def __tick (self) -> None:
        self.__s += 1

        if (self.__s == 60):
            self.__m += 1

            if (self.__m == 60):
                self.__h += 1

                if (self.__h == 24):
                    self.__reset ()


    def set (self, h, m, s):
        """
        Sets the clock's time
        """
        self.__h = h
        self.__m = m
        self.__s = s


    def time (self) -> str:
        """
        Returns current time in format HH:MM:SS
        """
        time_str = ""

        if (self.__h < 10):
            time_str += "0"

        time_str += str (self.__h)
        time_str += ":"

        if (self.__m < 10):
            time_str += "0"

        time_str += str (self.__m)
        time_str += ":"

        if (self.__s < 10):
            time_str += "0"

        time_str += str (self.__s)

        return time_str
