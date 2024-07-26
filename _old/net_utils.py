#!/usr/bin/env python

import sys

from os_utils import in_windows, run
from str_utils import str_empty




def usage () -> None:
    print ("Usage: testip <IP address or URL>")
    print ("Returns 0/True if address is reachable. 1/False otherwise.")
    print ()


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




if __name__ == "__main__":
    argc = len (sys.argv[1:])
    argv = sys.argv

    if (argc == 0) or (argv[1] == ""):
        usage ()
        exit (1)

    ip_address = argv[1]
    test_result = test_ip (ip_address)

    if (test_result == False):
        print ("Cannot reach " + ip_address + ".")
        print ()

        exit (1)

    else:
        print ("Host is reachable.")
        print ()

        exit (0)

