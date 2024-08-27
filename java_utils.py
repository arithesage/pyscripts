#!/usr/bin/env python

import sys

from scripting_commons import Messages as CommonMessages

from scripting_commons import basename,\
                              concat,\
                              file_contains,\
                              file_exists,\
                              file_ext,\
                              in_windows,\
                              print_va,\
                              read_file,\
                              write_file

from scripting_commons import make_path, cwd




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


def path_from_package (package: str) -> str:
    """
    Given a package, like 'me.java.app' returns it in path form: 'me/java/app'.
    """

    path = None    

    if in_windows ():
        path = package.replace (".", "\\")
    else:
        path = package.replace (".", "/")

    return path


def rename_package (src_file_path: str, new_package: str) -> bool:
    if not file_exists (src_file_path):
        print_va (CommonMessages.FileNotFoundError, src_file_path)
        return False
    
    java_file = is_java_file (src_file_path)
    kotlin_file = is_kotlin_file (src_file_path)

    if not java_file and not kotlin_file:
        print_va ("ERROR: '$[0]' isn't a Java or Kotlin file.", src_file_path)
        return False
    
    src_contents = read_file (src_file_path)
    src_lines = src_contents.split ("\n")

    old_package = None

    for line in src_lines:
        if line.startswith ("package"):
            old_package = line.split(" ")[1].strip(";")
            break

    if (old_package == None):
        print_va ("ERROR: Could not find file '$[0]' package.", src_file_path)
        return False
    
    src_contents = src_contents.replace (old_package,
                                         new_package)
    
    write_file (src_file_path, src_contents)

    print_va ("Updated '$[0]' package with '$[1]'.", 
              src_file_path, new_package)
    
    return True
    

def is_java_file (file_path: str) -> bool:
    if not file_exists (file_path):
        return False
    
    file_extension = file_ext (file_path).lower()

    if (file_extension == ".java"):
        return True
    
    return False


def is_kotlin_file (file_path: str) -> bool:
    if not file_exists (file_path):
        return False
    
    file_extension = file_ext (file_path).lower()

    if (file_extension == ".kt"):
        return True
    
    return False


rename_package (make_path (cwd(), "MainActivity.java"), "me.arithesage.java.android.testapp")


DEBUGGING = True

if __name__ == "__main__":
    if DEBUGGING:
        argv = ("DUMMY", "me/android/baseapp")        
    else:
        argv = sys.argv

    args = len (argv)

    print (package_from_path (argv[1]))
