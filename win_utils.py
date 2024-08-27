from scripting_commons import ExecResult
from scripting_commons import shellexec

"""
Functions for working specifically with Windows
"""


class REGEDIT:
    COMMAND = "reg"

    class ACTIONS:
        ADD = "add"
        QUERY = "query"

        def __init__(self) -> None:
            pass

    class CONSTS:
        DEFAULT_FIELD = "/ve"
        FIELD_DATA = "/d"
        FIELD_NAME = "/v"
        FIELD_TYPE = "/t"

        def __init__(self) -> None:
            pass

    class VALUE_TYPES:
        BINARY = "REG_BINARY"
        DWORD = "REG_DWORD"
        MULTI_LINE_STRING = "REG_MULTI_SZ"
        NOTHING = "REG_NONE"
        QWORD = "REG_QWORD"
        STRING = "REG_SZ"
        STRING_WITH_VARS = "REG_EXPAND_SZ"

        def __init__(self) -> None:
            pass

    def __init__(self) -> None:
        pass




def reg_query (key:str, field_name: str = None) -> str:
    """
    Returns the value of the given registry key and field.

    If None is provided as the field_name, the value of the
    default field will be retrieved.
    """
    cmdline = []
    cmdline.append (REGEDIT.COMMAND)
    cmdline.append (REGEDIT.ACTIONS.QUERY)
    cmdline.append (key)

    if (field_name == None):
        cmdline.append (REGEDIT.CONSTS.DEFAULT_FIELD)
    else:
        cmdline.append (REGEDIT.CONSTS.FIELD_NAME)
        cmdline.append (field_name)

    result = shellexec (cmdline)
    
    if result.ok:
        temp = result.stdout.split("\n")[2]
        temp = temp.strip()
        value = temp.split("    ")[2]
        return value

    return None


def reg_update (key: str, field_name: str, field_type: str, value: str) -> bool:
    """
    Updates the registry (BE VERY CAREFUL WITH THIS).
    Field type is one of REGEDIT.VALUE_TYPES constants.
    """
    cmdline = []
    cmdline.append (REGEDIT.COMMAND)
    cmdline.append (REGEDIT.ACTIONS.ADD)
    cmdline.append (key)

    if (field_name == None):
        cmdline.append (REGEDIT.CONSTS.DEFAULT_FIELD)
    else:
        cmdline.append (REGEDIT.CONSTS.FIELD_NAME)
        cmdline.append (field_name)

    cmdline.append (REGEDIT.CONSTS.FIELD_TYPE)
    cmdline.append (field_type)

    cmdline.append (REGEDIT.CONSTS.FIELD_DATA)
    cmdline.append (value)

    result = shellexec (cmdline)
    
    return result.ok



# Debugging area
#result = reg_query ("HKEY_CURRENT_USER\\SOFTWARE\\CRYO\\Atlantis\\GameDirectory")

#print (result)
