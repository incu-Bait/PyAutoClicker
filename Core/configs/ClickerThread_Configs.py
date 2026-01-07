from Core.globals.Base_import import List

class ClickerThread_Configs:
    DEFAULT_INTERVAL: float = 0.1
    DEFAULT_RANDOM_RANGE: float = 0.05
    MIN_SLEEP_TIME: float = 0.001 
    MAX_SLEEP_TIME: float = 0.05
    MOVE_THRESHOLD: float = 0.01 
    CPS_UPDATE_INTERVAL: float = 0.1  
    PERFORMANCE_THRESHOLD: float = 0.005 
    MIN_INTERVAL_LIMIT: float = 0.0001  
    CLICK_EMIT_THRESHOLD: float = 0.01  
    CLICK_EMIT_FREQUENCY: int = 10  
    CLICK_MOVE_DURATION: float = 0
    BUTTONS: List[str] = ["left", "right", "middle"]
    INITIAL_CLICKS: int = 0
    STATUS_STOPPED: str = "Stopped"
    STATUS_FINISHED: str = "Finished (click limit reached)"
    BUSY_WAIT_CHECK_INTERVAL: float = 0.0001