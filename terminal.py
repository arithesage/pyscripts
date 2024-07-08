#!/usr/bin/env python

from stdio import print_va
from str_utils import str_empty


class Terminal:
    def __init__(self) -> None:
        self.__commands = []
        self.__quit_command = "quit"
        self.__prompt = "> "
        self.__running = True

    def connect (self) -> None:
        self.prompt ()


    def prompt (self) -> None:
        while self.__running:
            print (self.__prompt, end="")        
            cmdline = input ()

            if not str_empty (cmdline):
                cmdline_chunks = cmdline.split (" ")

                command = cmdline_chunks[0]
                args = None

                if (len (cmdline_chunks) > 1):
                    args = cmdline_chunks[1:]

                if command == self.__quit_command:
                    self.__running = False
                    print ("Bye.")

                else:
                    if not command in self.__commands:
                        print_va ("Unknown command '$[0]'.", command)
                        print ()
