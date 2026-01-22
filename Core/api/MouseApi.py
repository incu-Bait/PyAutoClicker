# MouseApi.py
from Core.globals.Base_import import *


class FMClickerAPI:
    BUTTON_CODES = {
        "left": (2, 4),      # \\ MOUSEEVENTF_LEFTDOWN \ MOUSEEVENTF_LEFTUP
        "right": (8, 16),    # \\ MOUSEEVENTF_RIGHTDOWN \ MOUSEEVENTF_RIGHTUP
        "middle": (32, 64),  # \\ MOUSEEVENTF_MIDDLEDOWN \MOUSEEVENTF_MIDDLEUP
    }
    VK_CODES = {
        "left": 0x01,    # \\ VK_LBUTTON
        "right": 0x02,   # \\ VK_RBUTTON
        "middle": 0x04,  # \\ VK_MBUTTON
    }
    
    def __init__(self):
        self.user32 = ctypes.windll.user32
    
    @staticmethod
    def click(button="left"):
        button_codes = FMClickerAPI.BUTTON_CODES.get(button, (2, 4))
        down_code, up_code = button_codes
        ctypes.windll.user32.mouse_event(down_code, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(up_code, 0, 0, 0, 0)
    
    @staticmethod
    def double_click(button="left"):
        FMClickerAPI.click(button)
        time.sleep(0.001)
        FMClickerAPI.click(button)
    
    def click_at(self, x: int, y: int, button: str = "left", double: bool = False):
        self.move_to(x, y)
        if double:
            self.double_click(button)
        else:
            self.click(button)
        
        return (x, y, button, double)
    
    def move_to(self, x: int, y: int, duration: float = 0.0):
        if duration <= 0:
            self.user32.SetCursorPos(x, y)  # \\ Instant move 
        else:
            pyautogui.moveTo(x, y, duration=duration)  # \\ Smooth move 
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             button: str = "left", duration: float = 0.0):
        self.move_to(start_x, start_y)
        # --- Press mouse button ---
        down_code = self.BUTTON_CODES.get(button, (2, 4))[0]
        self.user32.mouse_event(down_code, 0, 0, 0, 0)
        # --- Move to end position ---
        self.move_to(end_x, end_y, duration)
        # --- Release mouse button ---
        up_code = self.BUTTON_CODES.get(button, (2, 4))[1]
        self.user32.mouse_event(up_code, 0, 0, 0, 0)
    
    def mouse_down(self, button: str = "left"):
        down_code = self.BUTTON_CODES.get(button, (2, 4))[0]
        self.user32.mouse_event(down_code, 0, 0, 0, 0)
    
    def mouse_up(self, button: str = "left"):
        up_code = self.BUTTON_CODES.get(button, (2, 4))[1]
        self.user32.mouse_event(up_code, 0, 0, 0, 0)
    
    def get_position(self) -> Tuple[int, int]:
        point = ctypes.wintypes.POINT()
        self.user32.GetCursorPos(ctypes.byref(point))
        return (point.x, point.y)
    
    def is_button_pressed(self, button: str = "left") -> bool:
        vk_code = self.VK_CODES.get(button, 0x01)
        return self.user32.GetAsyncKeyState(vk_code) & 0x8000 != 0
    
    def get_button_state(self) -> dict:
        return {
            "left": self.is_button_pressed("left"),
            "right": self.is_button_pressed("right"),
            "middle": self.is_button_pressed("middle"),
        }
    
    def scroll(self, clicks: int):
        # --- Positive clicks = scroll up, negative = scroll down ---
        self.user32.mouse_event(0x0800, 0, 0, clicks, 0)  # \\ MOUSEEVENTF_WHEEL