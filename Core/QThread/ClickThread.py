from Core.globals.Base_import import *
from Core.configs.ClickerThread_Configs import ClickerThread_Configs
from Core.api.MouseApi import FMClickerAPI


class ClickerThread(QThread):
    status_update = pyqtSignal(str)
    click_count_update = pyqtSignal(int)
    script_event = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self._setup_state()
        self._setup_settings()
        self._setup_dependencies()
        
        self._script_control_enabled = False
        self._script_actions = []
        self._current_script_action = None
        
    def _setup_state(self):
        self.is_running = False
        self.total_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.last_click_time = time.perf_counter()
        self.cps = 0
        self._paused = False
        
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
    
    def enable_script_control(self, enable: bool = True):
        self._script_control_enabled = enable
        if enable:
            self.status_update.emit("Script control enabled")
    
    def add_script_action(self, action_type: str, **kwargs):
        action = {"type": action_type, **kwargs}
        self._script_actions.append(action)
        self.script_event.emit({
            "event": "action_added",
            "action": action,
            "queue_length": len(self._script_actions)
        })
    
    def clear_script_queue(self):
        self._script_actions.clear()
        self.script_event.emit({"event": "queue_cleared"})
    
    def pause_script(self):
        self._paused = True
        self.status_update.emit("Script paused")
    
    def resume_script(self):
        self._paused = False
        self.status_update.emit("Script resumed")
    
    def run(self):
        self._reset_counters()
        while self.is_running:
            if self._paused:
                time.sleep(0.1)
                continue 
            if self._script_control_enabled and self._script_actions:
                self._execute_script_action()
            else:
                self._execute_click_cycle()
        self._signal_stop()
    
    def _execute_script_action(self):
        if not self._script_actions:
            return

        action = self._script_actions.pop(0)
        self._current_script_action = action
        handlers = {
            "click": self._execute_script_click,
            "move": self._execute_script_move,
            "wait": self._execute_script_wait,
            "drag": self._execute_script_drag,
            "mouse_down": self._execute_script_mouse_down,
            "mouse_up": self._execute_script_mouse_up,
            "scroll": self._execute_script_scroll,
        }
        try:
            handler = handlers.get(action["type"])
            if not handler:
                raise ValueError(f"Unknown action type: {action['type']}")
            handler(action)
            self.script_event.emit({
                "event": "action_completed",
                "action": action
            })
        except Exception as e:
            self.script_event.emit({
                "event": "action_error",
                "action": action,
                "error": str(e)
            })
        self._current_script_action = None
    
    def _execute_script_click(self, action: dict):
        x = action.get("x")
        y = action.get("y")
        button = action.get("button", "left")
        double = action.get("double", False)
        
        if x is not None and y is not None:
            self.clicker.click_at(x, y, button, double)
        else:
            if double:
                self.clicker.double_click(button)
            else:
                self.clicker.click(button)
    
    def _execute_script_move(self, action: dict):
        x = action["x"]
        y = action["y"]
        duration = action.get("duration", 0.0)
        self.clicker.move_to(x, y, duration)
    
    def _execute_script_wait(self, action: dict):
        seconds = action["seconds"]
        time.sleep(seconds)
    
    def _execute_script_drag(self, action: dict):
        start_x = action["start_x"]
        start_y = action["start_y"]
        end_x = action["end_x"]
        end_y = action["end_y"]
        button = action.get("button", "left")
        duration = action.get("duration", 0.0)
        self.clicker.drag(start_x, start_y, end_x, end_y, button, duration)
    
    def _execute_script_mouse_down(self, action: dict):
        button = action.get("button", "left")
        self.clicker.mouse_down(button)
    
    def _execute_script_mouse_up(self, action: dict):
        button = action.get("button", "left")
        self.clicker.mouse_up(button)
    
    def _execute_script_scroll(self, action: dict):
        clicks = action["clicks"]
        self.clicker.scroll(clicks)
    
    def _reset_counters(self):
        self.total_clicks = ClickerThread_Configs.INITIAL_CLICKS
        self.click_count_update.emit(self.total_clicks)
    
    def _execute_click_cycle(self):
        target_interval = self._calculate_interval()
        self._move_cursor_if_needed(target_interval)
        click_duration = self._perform_click(target_interval)
        self._update_counters(target_interval)
        if not self._check_click_limit():
            return
        self._precision_sleep(target_interval, click_duration)
        self._update_cps()
    
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
    
    def get_script_queue_length(self):
        return len(self._script_actions)
    
    def get_current_script_action(self):
        return self._current_script_action
    
    def is_script_control_enabled(self):
        return self._script_control_enabled
    
    def is_script_paused(self):
        return self._paused