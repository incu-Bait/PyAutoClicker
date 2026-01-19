from Core.globals.Base_import import *
from Core.script_engine.configs.PyScript_Configs import PyScriptConfig


class PyScript:
    def __init__(self, clicker_thread, script_engine):
        self.cfg = PyScriptConfig
        self.clicker = clicker_thread
        self.engine = script_engine
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
            pyautogui.click(x, y, button=button, clicks=2 if double else 1)
        else:
            pyautogui.click(button=button, clicks=2 if double else 1)
        
        self._mouse_state['last_click'] = (time.time(), button)

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
        else:
            duration = self._validate_duration(duration)
        
        pyautogui.moveTo(x, y, duration=duration)
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
        return pyautogui.position()
    
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
        
        current_x, current_y = pyautogui.position()
        self._mouse_state['position'] = (current_x, current_y)

        left_pressed = ctypes.windll.user32.GetAsyncKeyState(self.cfg.VK_LBUTTON) & 0x8000 != 0
        right_pressed = ctypes.windll.user32.GetAsyncKeyState(self.cfg.VK_RBUTTON) & 0x8000 != 0
        middle_pressed = ctypes.windll.user32.GetAsyncKeyState(self.cfg.VK_MBUTTON) & 0x8000 != 0
        
        self._mouse_state['pressed']['left'] = left_pressed
        self._mouse_state['pressed']['right'] = right_pressed
        self._mouse_state['pressed']['middle'] = middle_pressed

        self._last_state_update = current_time
        self._cached_state = self._mouse_state.copy()
        
        if self.cfg.DEBUG_ENABLED and self.cfg.DEBUG_LOG_MOUSE_STATE:
            self.log(f"Mouse state: pos=({current_x}, {current_y}), pressed={self._mouse_state['pressed']}", "DEBUG")
        
        return self._cached_state.copy()
    
    def is_button_pressed(self, button: str = 'left') -> bool:
        state = self.get_mouse_state()
        button = self._validate_button(button)
        return state['pressed'].get(button, False)
    
    def get_button_state(self) -> dict:
        state = self.get_mouse_state()
        return state['pressed'].copy()
    
    def get_mouse_position(self) -> Tuple[int, int]:
        state = self.get_mouse_state()
        return state['position']
    
    def get_last_click_info(self) -> Optional[Tuple[float, str]]:
        return self._mouse_state.get('last_click')
    
    def drag_to(self, x: int, y: int, duration: float = None, button: str = 'left') -> None:
        self._check_stop()

        button = self._validate_button(button)
        if not self._validate_coordinates(x, y):
            self.log(f"Warning: Coordinates ({x}, {y}) may be outside screen bounds", "WARNING")
        
        if duration is None:
            duration = self.cfg.DRAG_DURATION_DEFAULT
        else:
            duration = self._validate_duration(duration)
        
        current_x, current_y = pyautogui.position()
        self._mouse_state['drag_start'] = (current_x, current_y)
        self._mouse_state['drag_active'] = True

        self.emit('mouse_drag_start', {'start': (current_x, current_y), 'button': button})
        pyautogui.dragTo(x, y, duration=duration, button=button)
        
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
            pyautogui.moveTo(x, y)
            self._mouse_state['position'] = (x, y)
        
        pyautogui.mouseDown(button=button)
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
            pyautogui.moveTo(x, y)
            self._mouse_state['position'] = (x, y)
        
        pyautogui.mouseUp(button=button)
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
            pyautogui.moveTo(x, y)
            self._mouse_state['position'] = (x, y)
        
        pyautogui.scroll(clicks)

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
            if self.is_button_pressed(button):
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
            if not self.is_button_pressed(button):
                return True
            time.sleep(self.cfg.EXECUTION_CHECK_INTERVAL)
            self._check_stop()
        return False