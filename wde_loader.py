import json
import os
import importlib.util
from typing import Any
import log
import dearpygui.dearpygui as dpg
import gc
import psutil

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # Resident Set Size (physical memory used)

def exec(path: str) -> Any:
    if not path.endswith("/"):
        path += "/"

    if not os.path.exists(path + "data.json"):
        log.failed("data.json not found or broken symbol links.")
        return None

    with open(path + "data.json", "r") as file:
        datab = json.load(file)

    folder_name = os.path.basename(os.path.dirname(path))
    module_path = os.path.join(path, 'app.py')
    
    # load module
    try:
        spec = importlib.util.spec_from_file_location(f"{folder_name}.app", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    except Exception as e:
        log.failed(f"Failed at loading exec: {e}")

    # call entry
    app_instance = module.WDEApp()
    cleanup = datab.get('allow_clean_up', None)
    hwnd = datab.get('hwnd_tag', None)
    texture_registry = datab.get('texture_registry_tag', None)
    tr_cleanup = datab.get('allow_texture_cleanup', None)
    font_cleanup = datab.get('allow_font_cleanup', None)
    atexit_reference = None
    initial_local = None
    print(f"{hwnd} asldaxasd")
    print(datab)
    print(path + "data.json")
    
    # Entry Point Check
    if hasattr(app_instance, '__entry__'):
        entry_reference = app_instance.__entry__
    else:
        log.failed(f"Format error: no entry point for {app_instance}.")
        return None
    initial_local = set(locals().keys())
    entry_return = entry_reference()  # Call entry and get return


    def _exec_eof():
        log.log(f"call _exec_eof {hex(id(_exec_eof))} : {module.WDEApp()}")
        memory_before = get_memory_usage()
        log.info(f"mem usage {memory_before / 1024:.2f} KB")
        # Variable Cleanup
        if cleanup == True and isinstance(entry_return, dict):
            for var in entry_return:
                if var not in initial_local:
                    log.log(f"Cleaning up {app_instance}: {var} ({hex(id(var))})")
                    del var

            if (tr_cleanup == True):
                if (dpg.does_item_exist(texture_registry) == True):
                    for i in dpg.get_item_children(texture_registry, slot=1):
                        log.log(f"clean up texture {i} : {app_instance}")
                        dpg.delete_item(i)
                else:
                    log.log(f"texture_registry not defined, passed : {app_instance}")
            else:
                log.warn(f"passed texture clean up : {app_instance}")
        else:
            log.warn("Passed clean up or not returned clean up.")

        dpg.set_item_alias(hwnd, "")
        dpg.delete_item(hwnd)

        # Delete the app_instance and perform garbage collection
        gc.collect()

        # Memory usage after cleanup
        memory_after = get_memory_usage()
        log.info(f"mem usage {memory_after / 1024:.2f} KB")

        # Log how much memory has been freed
        memory_freed = memory_before - memory_after
        log.ok(f"cleand up memory for {module.WDEApp()}: {memory_freed / 1024:.2f} KB")
        if (not atexit_reference == None):
            log.log(f"call __atexit__ {hex(id(atexit_reference))} : {module.WDEApp()}")
            atexit_reference()

    # Handle atexit
    if hasattr(app_instance, '__atexit__'):

        if dpg.does_item_exist(hwnd):
            atexit_reference = app_instance.__atexit__
            dpg.configure_item(hwnd, on_close=_exec_eof)
        else:
            log.warn(f"__atexit__ defined but no hwnd tag : {hwnd} : {app_instance}")
    else:
        if dpg.does_item_exist(hwnd):
            dpg.configure_item(hwnd, on_close=_exec_eof)
        else:
            log.failed(f"__atexit__ defined but no hwnd tag : {hwnd} : {app_instance}")
        log.warn(f"__atexit__ reference not found, passed : {app_instance}")

    log.ok(f'{app_instance} finished with return {entry_return}')
    
    return module
