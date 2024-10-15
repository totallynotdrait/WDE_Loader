import dearpygui.dearpygui as dpg

class WDEApp:
    def __init__(self):
        pass

    def __endtry__(self):
        with dpg.window(label="entry_point"):
            dpg.add_text("we got working")
