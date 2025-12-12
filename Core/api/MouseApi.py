from Core.globals.Base_import import *

class FMClickerAPI:
    @staticmethod
    def click(button="left"):
        button_codes = {
            "left": (2, 4),      # \\ MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
            "right": (8, 16),    # \\ MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
            "middle": (32, 64),  # \\ MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP
        }
        down_code, up_code = button_codes.get(button, (2, 4))
        ctypes.windll.user32.mouse_event(down_code, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(up_code, 0, 0, 0, 0)
    ## Tiny delay between clicks for a DoubleClick 
    ## prob dont need this but oh well it took me 10 sec to make 
    @staticmethod
    def double_click(button="left"):
        FMClickerAPI.click(button)
        time.sleep(0.001) 
        FMClickerAPI.click(button)
