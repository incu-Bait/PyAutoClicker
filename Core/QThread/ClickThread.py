from Core.globals.Base_import import *
from Core.configs.ClickerThread_Configs import ClickerThread_Configs
from Core.api.MouseApi import FMClickerAPI

class ClickerThread(QThread):
    status_update = pyqtSignal(str)
    click_count_update = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.is_running = False
        self.interval = ClickerThread_Configs.DEFAULT_INTERVAL
        self.remaining_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.button = ClickerThread_Configs.BUTTONS[0]
        self.double_click = False
        self.fixed_pos = None
        self.randomize = False
        self.random_range = ClickerThread_Configs.DEFAULT_RANDOM_RANGE
        self.total_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.clicker = FMClickerAPI()
        self.last_click_time = time.perf_counter()
        self.actual_cps = 0

    def run(self):
        import time
        self.total_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.click_count_update.emit(ClickerThread_Configs.INITIAL_CLICKS)
        
        while self.is_running:
            
            target_interval = self.interval  # \\ Store interval before any operations
            if self.randomize:               #  \\ Apply randomization if enabled
                target_interval += random.uniform(-self.random_range, self.random_range)
                target_interval = max(0.0001, target_interval)  # \\ Minimum 0.1ms
            if self.fixed_pos is not None and target_interval >= 0.01:   # \\ Move to fixed position if needed (ONLY if not ultra-fast)
                pyautogui.moveTo(*self.fixed_pos, duration=ClickerThread_Configs.CLICK_MOVE_DURATION)
            start_time = time.perf_counter() 
            if self.double_click and target_interval >= 0.01:  # \\ Only double click if not ultra fast 
                self.clicker.double_click(self.button)         #  \\ No one will need DoubleClick when clicking fast 
            else:
                self.clicker.click(self.button)
            click_duration = time.perf_counter() - start_time
            self.total_clicks += 1
            if target_interval >= 0.01 or self.total_clicks % 10 == 0:
                self.click_count_update.emit(self.total_clicks)
            # --- Check click limit ---
            if self.remaining_clicks > 0:
                self.remaining_clicks -= 1
                if self.remaining_clicks == 0:
                    self.is_running = False
                    self.status_update.emit("Finished (click limit reached)")
                    break
            
            # Calculate sleep time accounting for click execution time
            # Starting to think im making this click to fast.
            # high precision sleep for fast intervals
            # if Busy wait for ultrafast intervals 
            actual_interval = target_interval - click_duration
            if actual_interval > 0:
                if actual_interval < 0.005:  # <5ms
                    end_time = time.perf_counter() + actual_interval
                    while time.perf_counter() < end_time and self.is_running:
                        pass
                else:
                    time.sleep(max(actual_interval, ClickerThread_Configs.MIN_SLEEP_TIME))  # \\ Normal sleep with minimal overhead
            # ---- Update CPS every 0.1 seconds ----
            current_time = time.perf_counter()
            if current_time - self.last_click_time >= 0.1:
                self.cps = 10 / (current_time - self.last_click_time)  # \\ Approximate CPS
                self.last_click_time = current_time
        
        self.status_update.emit("Stopped")
    
    def get_actual_cps(self):
        return self.cps