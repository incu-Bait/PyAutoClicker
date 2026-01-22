from Core.globals.Base_import import Tuple, Dict, List, Optional, TypedDict


class MouseState(TypedDict):
    position: Tuple[int, int]
    pressed: Dict[str, bool]
    last_click: Optional[Tuple[float, str]]
    drag_start: Optional[Tuple[int, int]]
    drag_active: bool


class PyScriptConfig:
    MAX_SCRIPT_EXECUTION_TIME: int = 300
    AUTO_STOP_ON_ERROR: bool = True
    ENABLE_EVENT_SYSTEM: bool = True
    DEFAULT_LOG_LEVEL: str = "INFO"
    
    MOUSE_MOVE_DURATION_DEFAULT: float = 0.0
    DOUBLE_CLICK_INTERVAL: float = 0.1
    DRAG_DURATION_DEFAULT: float = 0.0
    WAIT_FOR_BUTTON_TIMEOUT: float = 10.0
    
    BUTTON_MAPPING: Dict[str, str] = {
        'left': 'left',
        'right': 'right',
        'middle': 'middle',
        'l': 'left',
        'r': 'right',
        'm': 'middle'
    }
    
    VK_LBUTTON: int = 0x01
    VK_RBUTTON: int = 0x02
    VK_MBUTTON: int = 0x04
    
    MOUSE_POSITION_DEFAULT: Tuple[int, int] = (0, 0)
    MOUSE_PRESSED_DEFAULTS: Dict[str, bool] = {
        'left': False,
        'right': False, 
        'middle': False
    }
    
    EXECUTION_CHECK_INTERVAL: float = 0.05
    MAX_ITERATIONS_WITHOUT_CHECK: int = 1000
    ENABLE_STOP_ITERATION: bool = True
    
    ALLOWED_BUILTINS: List[str] = [
        'range', 'len', 'str', 'int', 'float', 'bool',
        'list', 'dict', 'tuple', 'set', 'min', 'max',
        'sum', 'abs', 'round', 'zip', 'enumerate', 'sorted'
    ]
    
    ALLOWED_MODULES: List[str] = ['random', 'time']
    
    PYSCRIPT_METHODS: List[str] = [
        'click', 'move', 'wait', 'get_position',
        'drag_to', 'mouse_down', 'mouse_up',
        'mouse_scroll', 'wait_for_button_press',
        'wait_for_button_release',
        'get_mouse_state', 'is_button_pressed',
        'get_button_state', 'get_mouse_position',
        'get_last_click_info', 'is_dragging',
        'get_drag_info',
        'stop', 'is_running',
        'log',
        'on', 'emit'
    ]
    
    LOG_FORMAT: str = "[{level}] {message}"
    ERROR_FORMAT: str = "Error: {error}\n{traceback}"
    
    SCRIPT_START_MESSAGE: str = "=== PyScript Started ==="
    SCRIPT_COMPLETE_MESSAGE: str = "=== PyScript Completed ==="
    SCRIPT_STOPPED_MESSAGE: str = "=== PyScript Stopped ==="
    EMPTY_SCRIPT_MESSAGE: str = "No script to execute"
    
    DEFAULT_EVENTS: List[str] = [
        'mouse_click', 'mouse_move', 'mouse_drag_start',
        'mouse_drag_end', 'key_press', 'script_start',
        'script_stop', 'script_error'
    ]
    
    THREAD_WAIT_TIMEOUT: int = 2000
    FORCE_TERMINATE_THREAD: bool = True
    
    DRAG_START_THRESHOLD: int = 5
    DRAG_UPDATE_INTERVAL: float = 0.1
    
    MAX_CLICKS_PER_SECOND: int = 100
    MAX_MOVEMENTS_PER_SECOND: int = 100
    MAX_WAIT_TIME: int = 3600
    
    STATE_UPDATE_INTERVAL: float = 0.1
    ENABLE_MOUSE_STATE_CACHING: bool = True
    CACHE_DURATION: float = 0.05
    
    VALIDATE_COORDINATES: bool = True
    VALIDATE_BUTTON_NAMES: bool = True
    VALIDATE_DURATION_VALUES: bool = True
    
    SCREEN_WIDTH: Optional[int] = None
    SCREEN_HEIGHT: Optional[int] = None
    
    DEBUG_ENABLED: bool = False
    DEBUG_LOG_MOUSE_STATE: bool = False
    DEBUG_LOG_EVENTS: bool = False
    DEBUG_LOG_API_CALLS: bool = False
    
    LOG_SIGNAL_NAME: str = "log_signal"
    ERROR_SIGNAL_NAME: str = "error_signal"
    FINISHED_SIGNAL_NAME: str = "finished_signal"
    
