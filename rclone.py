#!/usr/bin/env python

#from filesystem import *
from file_utils import *
from os_utils import *



class RCLONE_CONSTS:
    LOCAL_MACHINE = "[Local]\ntype = local\n"

    def __init__ (self):
        pass


class RCLONE_PATHS:
    RCLONE_CONFIG_PATH_WINDOWS = ""
    RCLONE_CONFIG_PATH_UNIX = make_path (env ("HOME"), ".config", "rclone")
    RCLONE_CONFIG_PATH = None
    RCLONE_CONFIG_FILE = None

    def __init__ (self):
        pass




def config_available ():
    return file_exists (RCLONE_PATHS.RCLONE_CONFIG_FILE)


def local_config_entry_available ():
    return file_contains (RCLONE_PATHS.RCLONE_CONFIG_FILE, RCLONE_CONSTS.LOCAL_MACHINE)


def lsf (host, path):
    run ("rclone lsf " + host + ":" + path)




if (in_windows ()):
    RCLONE_PATHS.RCLONE_CONFIG_FILE = make_path (RCLONE_PATHS.RCLONE_CONFIG_PATH_WINDOWS, "rclone.conf")
else:
    RCLONE_PATHS.RCLONE_CONFIG_FILE = make_path (RCLONE_PATHS.RCLONE_CONFIG_PATH_UNIX, "rclone.conf")
