#!/usr/bin/env python

from flatpak import *

from scripting_commons import ask_yn, cwd




flatapp_name = "org.DolphinEmu.dolphin-emu"
as_user = True

def play (game_path: str, user_dir: str = cwd()) -> bool:
    if not flatapp_installed (flatapp_name, as_user):
        if ask_yn ("DolphinEmu isn't installed. Install it?"):
            if not flatapp_install (flatapp_name, as_user):
                print ("ERROR: Failed installing DolphinEmu.")
                print ()
                exit (1)
        else:
            print ("Aborted.")
            print ()
            exit (1)

    return flatapp_run (flatapp_name,
                        as_user,
                        "--batch", "-e", game_path, "-u", user_dir)


