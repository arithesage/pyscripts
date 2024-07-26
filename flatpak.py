#!/usr/bin/env python


from scripting_commons import concat
from scripting_commons import cwd
from scripting_commons import file_exists
from scripting_commons import make_path
from scripting_commons import exec, shellexec


class Flatpak:
    PATH = "/usr/bin/flatpak"

    def __init__(self) -> None:
        pass




def flatpak_available () -> bool:
    return file_exists (Flatpak.PATH)


def flatapp_can_access (app_name: str, path: str, as_user: bool = True) -> bool:
    """
    Returns if the given app have access to 'path' (and below).
    """
    cmdline = []
    cmdline.append (Flatpak.PATH)
    cmdline.append ("override")

    if as_user:
        cmdline.append ("--user")
    
    cmdline.append ("--show")
    cmdline.append (app_name)

    exec_result = exec (cmdline, capture_output=True)

    if (exec_result.returncode == 0):
        return path in exec_result.stdout
    
    return False


def flatapp_grant_access (app_name: str, path: str, as_user: bool = True) -> bool:
    cmdline = []
    cmdline.append (Flatpak.PATH)
    cmdline.append ("override")

    if as_user:
        cmdline.append ("--user")

    cmdline.append (concat ("--filesystem=\"", path, "\""))
    cmdline.append (app_name)

    exec_result = exec (cmdline)

    if (exec_result.returncode == 0):
        return True
    else:
        return False


def flatapp_install (app_name: str, as_user: bool = True) -> bool:
    cmdline = []
    cmdline.append (Flatpak.PATH)
    cmdline.append ("install")

    if as_user:
        cmdline.append ("--user")

    cmdline.append (app_name)

    exec_result = exec (cmdline)

    if (exec_result.returncode == 0):
        return True
    else:
        return False


def flatapp_installed (app_name: str, as_user: bool = True) -> bool:
    cmdline = []
    cmdline.append (Flatpak.PATH)
    cmdline.append ("list")

    if as_user:
        cmdline.append ("--user")

    exec_result = exec (cmdline, capture_output=True)

    if (exec_result.returncode == 0):
        if app_name in exec_result.stdout:
            return True
        
    return False


def flatapp_run (app_name: str, as_user: bool = True, *params) -> bool:
    cmdline = []
    cmdline.append (Flatpak.PATH)
    cmdline.append ("run")

    if as_user:
        cmdline.append ("--user")

    cmdline.append (app_name)

    for param in params:
        cmdline.append (param)

    exec_result = exec (cmdline)

    if (exec_result.returncode == 0):
        return True
    else:
        return False
    
