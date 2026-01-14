from Core.globals.Base_import import *
from Core.configs.ClickerThread_Configs import ClickerThread_Configs
from Core.api.MouseApi import FMClickerAPI


class ClickerThread(QThread):
    status_update = pyqtSignal(str)
    click_count_update = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self._setup_state()
        self._setup_settings()
        self._setup_dependencies()

    def _setup_state(self):
        self.is_running = False
        self.total_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.last_click_time = time.perf_counter()
        self.cps = 0

    def _setup_settings(self):
        self.interval = ClickerThread_Configs.DEFAULT_INTERVAL
        self.remaining_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.button = ClickerThread_Configs.BUTTONS[0]
        self.double_click = False
        self.fixed_pos = None
        self.randomize = False
        self.random_range = ClickerThread_Configs.DEFAULT_RANDOM_RANGE

    def _setup_dependencies(self):
        self.clicker = FMClickerAPI()

    def run(self):
        self._reset_counters()
        while self.is_running:
            self._execute_click_cycle()
        self._signal_stop()

    def _execute_click_cycle(self):
        target_interval = self._calculate_interval() 
        self._move_cursor_if_needed(target_interval) 
        click_duration = self._perform_click(target_interval) 
        self._update_counters(target_interval)
        if not self._check_click_limit():
            return
        self._precision_sleep(target_interval, click_duration) 
        self._update_cps() 

    def _reset_counters(self):
        self.total_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.click_count_update.emit(self.total_clicks)

    def _calculate_interval(self):
        target_interval = self.interval
        if self.randomize:
            target_interval += random.uniform(-self.random_range, self.random_range)
            target_interval = max(ClickerThread_Configs.MIN_INTERVAL_LIMIT, target_interval)
        return target_interval

    def _move_cursor_if_needed(self, interval):
        if self.fixed_pos is not None and interval >= ClickerThread_Configs.MOVE_THRESHOLD:
            pyautogui.moveTo(*self.fixed_pos, duration=ClickerThread_Configs.CLICK_MOVE_DURATION)

    def _perform_click(self, interval):
        start_time = time.perf_counter()
        if self.double_click and interval >= ClickerThread_Configs.MOVE_THRESHOLD:
            self.clicker.double_click(self.button)
        else:
            self.clicker.click(self.button)
        return time.perf_counter() - start_time

    def _update_counters(self, interval):
        self.total_clicks += 1
        should_emit = (
            interval >= ClickerThread_Configs.CLICK_EMIT_THRESHOLD or 
            self.total_clicks % ClickerThread_Configs.CLICK_EMIT_FREQUENCY == 0
        )
        if should_emit:
            self.click_count_update.emit(self.total_clicks)

    def _check_click_limit(self):
        if self.remaining_clicks > 0:
            self.remaining_clicks -= 1
            if self.remaining_clicks == 0:
                self.is_running = False
                self.status_update.emit(ClickerThread_Configs.STATUS_FINISHED)
                return False
        return True

    def _precision_sleep(self, target_interval, click_duration):
        actual_interval = target_interval - click_duration
        
        if actual_interval > 0:
            if actual_interval < ClickerThread_Configs.PERFORMANCE_THRESHOLD:
                self._busy_wait(actual_interval)
            else:
                sleep_time = max(actual_interval, ClickerThread_Configs.MIN_SLEEP_TIME)
                sleep_time = min(sleep_time, ClickerThread_Configs.MAX_SLEEP_TIME)
                time.sleep(sleep_time)

    def _busy_wait(self, duration):
        end_time = time.perf_counter() + duration
        while time.perf_counter() < end_time and self.is_running:
            if duration > ClickerThread_Configs.BUSY_WAIT_CHECK_INTERVAL:
                time.sleep(ClickerThread_Configs.BUSY_WAIT_CHECK_INTERVAL)

    def _update_cps(self):
        current_time = time.perf_counter()
        time_since_last_update = current_time - self.last_click_time
        
        if time_since_last_update >= ClickerThread_Configs.CPS_UPDATE_INTERVAL:
            self.cps = ClickerThread_Configs.CLICK_EMIT_FREQUENCY / time_since_last_update
            self.last_click_time = current_time

    def _signal_stop(self):
        self.status_update.emit(ClickerThread_Configs.STATUS_STOPPED)

    def get_actual_cps(self):
        return self.cps