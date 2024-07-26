#!/usr/bin/env python


DEBUG_LOG = True


def disable_logd () -> None:
    global DEBUG_LOG

    DEBUG_LOG = False


def enable_logd () -> None:
    global DEBUG_LOG

    DEBUG_LOG = True


def log_d (message: str = "") -> None:
    """
    Prints a debug message ONLY IF DEBUG_LOG IS ENABLED (True)
    """
    if (DEBUG_LOG == True):
        print ("[DEBUG] " + message)


def log_e (message: str = "") -> None:
    print ("[ERROR] " + message)


def log_i (message: str = "") -> None:
    print ("[INFO]" + message)


def log_w (message: str = "") -> None:
    print ("[WARNING] " + message)


