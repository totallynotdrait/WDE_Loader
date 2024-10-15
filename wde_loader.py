import json
import os
import importlib.util
from typing import Any

def exec(path: str) -> Any:
    if not path.endswith("/"):
        path += "/"

    if not os.path.exists(path + "data.json"):
        print("data.json not found or broken symbol links.")
        return None

    with open(path + "data.json", "r") as file:
        datab = json.load(file)

    folder_name = os.path.basename(os.path.dirname(path))

    module_path = os.path.join(path, 'app.py')
    
    # somehow load script to here
    spec = importlib.util.spec_from_file_location(f"{folder_name}.app", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # call entry
    try: 
        entry_return = module.WDEApp().__entry__()

        return entry_return
    except Exception as e:
        print(f"Failed at exec: {e}")

        return None
    
    