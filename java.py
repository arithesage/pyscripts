#!/usr/bin/env python

from lang import argv
from lang import executing
from lang import type_of

from os_utils import ProcessResult
from os_utils import run_program

from stdio import print_va




def java (args) -> ProcessResult:
    java_cmdline = []
    java_cmdline.append ("java")

    if type_of (args, str):
        args = args.split (" ")
    
    for arg in args:
        java_cmdline.append (arg)

    process_result = run_program (java_cmdline, ".", True)
    return process_result


def java_version ():
    version = ""
    
    process_result = java ("--version")

    if process_result.ok ():
        version = process_result.output().split("\n")[0]

    return version


if executing ():
    command = argv[0]

    if ("version") in argv:
        version = java_version ()
        print_va ("$[0]", version)


















