import io
import json
from os.path import isfile as file_exists
from typing import Dict

from stdio import print_va


def loadJSONFile (json_file_path:str) -> Dict[str]:
    json_data = {}

    if not file_exists (json_file_path):
        print_va ("ERROR: File '$[0]' was not found.", json_file_path)
    else:
        with io.open(json_file_path, 'r', encoding='utf-8') as json_file:
            json_data = json.load (json_file)

    if (json_data != None):
        return json_data
    
    return None


