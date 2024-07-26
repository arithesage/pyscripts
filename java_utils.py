#!/usr/bin/env python

import sys

from scripting_commons import in_windows




def package_from_path (path: str) -> str:
    """
    Given a path, like 'me/java/app' returns it in package form: 'me.java.app'.
    """
    package = None

    if in_windows ():
        package = path.replace ("\\", ".")
    else:
        package = path.replace ("/", ".")

    return package




DEBUGGING = True

if __name__ == "__main__":
    if DEBUGGING:
        argv = ("DUMMY", "me/android/baseapp")        
    else:
        argv = sys.argv

    args = len (argv)

    print (package_from_path (argv[1]))