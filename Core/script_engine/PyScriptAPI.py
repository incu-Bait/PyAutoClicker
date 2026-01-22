from Core.globals.Base_import import *
from Core.script_engine.configs.PyScript_Configs import PyScriptConfig
from Core.api.MouseApi import FMClickerAPI
# ============================================================
#  Function               |       What it does
# ============================================================
# _validate_coordinates ---> Validates if coordinates are within screen bounds
# _validate_button ---> Validates and maps button names to standard format
# _validate_duration ---> Validates that duration values are non negative
# click ---> Performs mouse click at specified position or current position
# move ---> Moves mouse cursor to specified coordinates with optional duration
# wait ---> Pauses script execution for specified number of seconds
# get_position ---> Returns current mouse cursor position
# log ---> Logs messages with specified level to the engine
# stop ---> Stops script execution and raises StopIteration if enabled
# is_running ---> Returns whether the script is currently running
# on ---> Registers event listener callback for specified event
# emit ---> Triggers all callbacks registered for specified event
# _check_stop ---> Checks if script should stop and raises StopIteration if needed
# get_mouse_state ---> Returns current mouse state including position and button states
# is_button_pressed ---> Checks if specified mouse button is currently pressed
# get_button_state ---> Returns state of all mouse buttons
# get_mouse_position ---> Returns current mouse cursor position
# get_last_click_info ---> Returns timestamp and button of last click performed
# drag_to ---> Drags mouse from current position to target coordinates
# mouse_down ---> Presses specified mouse button down at optional coordinates
# mouse_up ---> Releases specified mouse button at optional coordinates
# is_dragging ---> Returns whether a drag operation is currently active
# get_drag_info ---> Returns information about current drag operation
# mouse_scroll ---> Scrolls mouse wheel by specified clicks at optional position
# wait_for_button_press ---> Waits for specified button to be pressed with timeout
# wait_for_button_release ---> Waits for specified button to be released with timeout
# ============================================================


class PyScript:
    def __init__(self, clicker_thread, script_engine):
        self.cfg = PyScriptConfig
        self.clicker = clicker_thread
        self.engine = script_engine
        self.mouse_api = FMClickerAPI()
        self._should_stop = False
        self._event_listeners = {}
        self._mouse_state = {
            'position': self.cfg.MOUSE_POSITION_DEFAULT,
            'pressed': self.cfg.MOUSE_PRESSED_DEFAULTS.copy(),
            'last_click': None,
            'drag_start': None,
            'drag_active': False
        }
        self._iteration_count = 0
        self._last_state_update = 0
        self._cached_state = None
        if self.cfg.VALIDATE_COORDINATES:
            try:
                screen_size = pyautogui.size()
                self.cfg.SCREEN_WIDTH = screen_size.width
                self.cfg.SCREEN_HEIGHT = screen_size.height
            except:
                pass
    
    def _validate_coordinates(self, x: int, y: int) -> bool:
        if not self.cfg.VALIDATE_COORDINATES:
            return True
            
        if (self.cfg.SCREEN_WIDTH and 
            self.cfg.SCREEN_HEIGHT):
            return (0 <= x < self.cfg.SCREEN_WIDTH and 
                    0 <= y < self.cfg.SCREEN_HEIGHT)
        return True
    
    def _validate_button(self, button: str) -> str:
        if not self.cfg.VALIDATE_BUTTON_NAMES:
            return button
            
        button = button.lower()
        return self.cfg.BUTTON_MAPPING.get(button, button)
    
    def _validate_duration(self, duration: float) -> float:
        if self.cfg.VALIDATE_DURATION_VALUES and duration < 0:
            raise ValueError(f"Duration cannot be negative: {duration}")
        return max(0.0, duration)
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = 'left', double: bool = False) -> None:
        self._check_stop()

        button = self._validate_button(button)
        if x is not None and y is not None:
            if not self._validate_coordinates(x, y):
                self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if x is not None and y is not None:
            self.mouse_api.click_at(x, y, button, double)
        else:
            if double:
                self.mouse_api.double_click(button)
            else:
                self.mouse_api.click(button)
        
        self._mouse_state['last_click'] = (time.time(), button)
        self._mouse_state['position'] = self.get_position()

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            pos_str = f"at ({x}, {y})" if x is not None and y is not None else "at current position"
            self.log(f"API: click {pos_str} with {button} button", "DEBUG")

        self.emit('mouse_click', {'x': x, 'y': y, 'button': button, 'double': double})
    
    def move(self, x: int, y: int, duration: float = None) -> None:
        self._check_stop()

        if not self._validate_coordinates(x, y):
            self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if duration is None:
            duration = self.cfg.MOUSE_MOVE_DURATION_DEFAULT

        self.mouse_api.move_to(x, y, duration)
        self._mouse_state['position'] = (x, y)

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            self.log(f"API: move to ({x}, {y}) in {duration}s", "DEBUG")

        self.emit('mouse_move', {'x': x, 'y': y, 'duration': duration})
    
    def wait(self, seconds: float) -> None:
        self._check_stop()

        seconds = self._validate_duration(seconds)
        if seconds > self.cfg.MAX_WAIT_TIME:
            raise ValueError(f"Wait time {seconds}s exceeds maximum of {self.cfg.MAX_WAIT_TIME}s")
        
        time.sleep(seconds)

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            self.log(f"API: wait for {seconds}s", "DEBUG")
    
    def get_position(self) -> Tuple[int, int]:
        return self.mouse_api.get_position()
    
    def log(self, message: str, level: str = None) -> None:
        if level is None:
            level = self.cfg.DEFAULT_LOG_LEVEL

        log_levels = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
        config_level = log_levels.get(self.cfg.DEFAULT_LOG_LEVEL.upper(), 1)
        msg_level = log_levels.get(level.upper(), 1)
        
        if msg_level >= config_level:
            formatted = self.cfg.LOG_FORMAT.format(level=level, message=message)
            self.engine.log_signal.emit(formatted)
    
    def stop(self) -> None:
        self._should_stop = True
        if self.cfg.ENABLE_STOP_ITERATION:
            raise StopIteration("Script stopped by user")
    
    def is_running(self) -> bool:
        return not self._should_stop
    
    def on(self, event_name: str, callback: Callable) -> None:
        if not self.cfg.ENABLE_EVENT_SYSTEM:
            self.log("Event system is disabled", "WARNING")
            return
            
        if event_name not in self._event_listeners:
            self._event_listeners[event_name] = []
        self._event_listeners[event_name].append(callback)
    
    def emit(self, event_name: str, data: Any = None) -> None:
        if not self.cfg.ENABLE_EVENT_SYSTEM:
            return
            
        if event_name in self._event_listeners:
            for callback in self._event_listeners[event_name]:
                try:
                    callback(data)
                except Exception as e:
                    self.log(f"Event callback error: {e}", "ERROR")

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_EVENTS:
            self.log(f"EVENT: {event_name} - {data}", "DEBUG")
    
    def _check_stop(self) -> None:
        self._iteration_count += 1

        if self._iteration_count % self.cfg.MAX_ITERATIONS_WITHOUT_CHECK == 0:
            if self._should_stop:
                if self.cfg.ENABLE_STOP_ITERATION:
                    raise StopIteration("Script stopped")

        if self._should_stop:
            if self.cfg.ENABLE_STOP_ITERATION:
                raise StopIteration("Script stopped")
    
    def get_mouse_state(self) -> dict:
        current_time = time.time()

        if (self.cfg.ENABLE_MOUSE_STATE_CACHING and 
            self._cached_state and 
            current_time - self._last_state_update < self.cfg.CACHE_DURATION):
            return self._cached_state.copy()
        current_x, current_y = self.mouse_api.get_position()
        self._mouse_state['position'] = (current_x, current_y)
        button_state = self.mouse_api.get_button_state()
        self._mouse_state['pressed']['left'] = button_state.get('left', False)
        self._mouse_state['pressed']['right'] = button_state.get('right', False)
        self._mouse_state['pressed']['middle'] = button_state.get('middle', False)

        self._last_state_update = current_time
        self._cached_state = self._mouse_state.copy()
        
        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_MOUSE_STATE:
            self.log(f"Mouse state: pos=({current_x}, {current_y}), pressed={self._mouse_state['pressed']}", "DEBUG")
        
        return self._cached_state.copy()
    
    def is_button_pressed(self, button: str = 'left') -> bool:
        return self.mouse_api.is_button_pressed(button)
    
    def get_button_state(self) -> dict:
        return self.mouse_api.get_button_state()
    
    def get_mouse_position(self) -> Tuple[int, int]:
        return self.mouse_api.get_position()
    
    def get_last_click_info(self) -> Optional[Tuple[float, str]]:
        return self._mouse_state.get('last_click')
    
    def drag_to(self, x: int, y: int, duration: float = None, button: str = 'left') -> None:
        self._check_stop()

        button = self._validate_button(button)
        if not self._validate_coordinates(x, y):
            self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if duration is None:
            duration = self.cfg.DRAG_DURATION_DEFAULT
        
        current_x, current_y = self.mouse_api.get_position()
        self._mouse_state['drag_start'] = (current_x, current_y)
        self._mouse_state['drag_active'] = True

        self.emit('mouse_drag_start', {'start': (current_x, current_y), 'button': button})
        self.mouse_api.drag(current_x, current_y, x, y, button, duration)
        
        self._mouse_state['drag_active'] = False
        self._mouse_state['position'] = (x, y)
        self.emit('mouse_drag_end', {
            'start': (current_x, current_y),
            'end': (x, y),
            'button': button
        })

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            self.log(f"API: drag from ({current_x}, {current_y}) to ({x}, {y})", "DEBUG")
    
    def mouse_down(self, button: str = 'left', x: int = None, y: int = None) -> None:
        self._check_stop()

        button = self._validate_button(button)
        if x is not None and y is not None:
            if not self._validate_coordinates(x, y):
                self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if x is not None and y is not None:
            self.mouse_api.move_to(x, y)
            self._mouse_state['position'] = (x, y)

        self.mouse_api.mouse_down(button)
        self._mouse_state['pressed'][button] = True

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            pos_str = f"at ({x}, {y})" if x is not None and y is not None else "at current position"
            self.log(f"API: mouse_down {pos_str} with {button} button", "DEBUG")
    
    def mouse_up(self, button: str = 'left', x: int = None, y: int = None) -> None:
        self._check_stop()

        button = self._validate_button(button)
        if x is not None and y is not None:
            if not self._validate_coordinates(x, y):
                self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if x is not None and y is not None:
            self.mouse_api.move_to(x, y)
            self._mouse_state['position'] = (x, y)

        self.mouse_api.mouse_up(button)
        self._mouse_state['pressed'][button] = False

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            pos_str = f"at ({x}, {y})" if x is not None and y is not None else "at current position"
            self.log(f"API: mouse_up {pos_str} with {button} button", "DEBUG")
    
    def is_dragging(self) -> bool:
        return self._mouse_state.get('drag_active', False)
    
    def get_drag_info(self) -> Optional[dict]:
        if not self._mouse_state.get('drag_active'):
            return None
        
        current_x, current_y = self._mouse_state['position']
        start_x, start_y = self._mouse_state.get('drag_start', (0, 0))
        
        return {
            'start': (start_x, start_y),
            'current': (current_x, current_y),
            'delta': (current_x - start_x, current_y - start_y)
        }
    
    def mouse_scroll(self, clicks: int, x: int = None, y: int = None) -> None:
        self._check_stop()

        if x is not None and y is not None:
            if not self._validate_coordinates(x, y):
                self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if x is not None and y is not None:
            self.mouse_api.move_to(x, y)
            self._mouse_state['position'] = (x, y)
        self.mouse_api.scroll(clicks)

        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_API_CALLS:
            pos_str = f"at ({x}, {y})" if x is not None and y is not None else "at current position"
            self.log(f"API: mouse_scroll {clicks} clicks {pos_str}", "DEBUG")
    
    def wait_for_button_press(self, button: str = 'left', timeout: float = None) -> bool:
        self._check_stop()

        button = self._validate_button(button)
        if timeout is None:
            timeout = self.cfg.WAIT_FOR_BUTTON_TIMEOUT
        else:
            timeout = self._validate_duration(timeout)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.mouse_api.is_button_pressed(button):
                return True
            time.sleep(self.cfg.EXECUTION_CHECK_INTERVAL)
            self._check_stop()
        return False
    
    def wait_for_button_release(self, button: str = 'left', timeout: float = None) -> bool:
        self._check_stop()

        button = self._validate_button(button)
        if timeout is None:
            timeout = self.cfg.WAIT_FOR_BUTTON_TIMEOUT
        else:
            timeout = self._validate_duration(timeout)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not self.mouse_api.is_button_pressed(button):
                return True
            time.sleep(self.cfg.EXECUTION_CHECK_INTERVAL)
            self._check_stop()
        return False