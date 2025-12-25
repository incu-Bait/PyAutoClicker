from Core.globals.Base_import import *

class SettingsPanel_Configs:
    # ============================================
    # UI DIMENSIONS
    # ============================================
    MIN_WIDTH = 325
    MIN_HEIGHT = 325
    
    # ============================================
    # UI OBJECT NAMES
    # ============================================
    WARNING_FRAME_OBJECT_NAME = "warningFrame"
    WARNING_ICON_OBJECT_NAME = "warningIcon"
    WARNING_LABEL_OBJECT_NAME = "warningLabel"
    
    CLICK_GROUP_OBJECT_NAME = "clickSettingsGroup"
    BUTTON_COMBO_OBJECT_NAME = "buttonComboBox"
    DOUBLE_CHECK_OBJECT_NAME = "doubleClickCheckBox"
    
    TIMING_GROUP_OBJECT_NAME = "timingSettingsGroup"
    INTERVAL_SPIN_OBJECT_NAME = "intervalSpinBox"
    REPEAT_SPIN_OBJECT_NAME = "repeatSpinBox"
    
    POSITION_GROUP_OBJECT_NAME = "positionSettingsGroup"
    POSITION_LABEL_OBJECT_NAME = "positionLabel"
    OVERLAY_TOGGLE_OBJECT_NAME = "overlayToggleButton"
    CURSOR_RADIO_OBJECT_NAME = "cursorPositionRadio"
    FIXED_RADIO_OBJECT_NAME = "fixedPositionRadio"
    X_SPIN_OBJECT_NAME = "xPositionSpinBox"
    Y_SPIN_OBJECT_NAME = "yPositionSpinBox"
    CAPTURE_BUTTON_OBJECT_NAME = "captureButton"
    LIVE_CAPTURE_BUTTON_OBJECT_NAME = "liveCaptureButton"
    
    # ============================================
    # LIMITS & DEFAULTS
    # ============================================
    # NOTE: The MIN_INTERVAL when set past 0.001 
    # Will crash the app and maybe your PC
    # But that is a risk im willing to take for FAST CLCIKING !!!!!
    MIN_INTERVAL = 0.0001 
    MAX_INTERVAL = 999999.0  
    DEFAULT_INTERVAL = 0.1
    MAX_REPEAT = 999999
    MAX_POSITION = 999999
    INITIAL_POSITION = (0, 0)
    LIVE_CAPTURE_FPS = 30
    
    # ============================================
    # CLICK SETTINGS
    # ============================================
    CLICK_GROUP_TITLE = "Click Settings"
    BUTTON_LABEL_TEXT = "Button:"
    BUTTON_OPTIONS = ["left", "right", "middle"]
    DOUBLE_CLICK_TEXT = "Double click"
    
    # ============================================
    # TIMING SETTINGS
    # ============================================
    TIMING_GROUP_TITLE = "Timing"
    INTERVAL_LABEL_TEXT = "Interval:"
    INTERVAL_SUFFIX = " s"
    INTERVAL_DECIMALS = 4
    INTERVAL_STEP = 0.001
    REPEAT_LABEL_TEXT = "Repeat:"
    REPEAT_SPECIAL_TEXT = "Infinite"
    
    # ============================================
    # POSITION SETTINGS
    # ============================================
    POSITION_GROUP_TITLE = "Position"
    POSITION_LABEL_FORMAT = "Screen Position: {pos}"
    X_LABEL_TEXT = "X:"
    Y_LABEL_TEXT = "Y:"
    OVERLAY_SHOW_TEXT = "Show Dot"
    OVERLAY_HIDE_TEXT = "Hide Dot"
    CURSOR_RADIO_TEXT = "Current Position"
    FIXED_RADIO_TEXT = "Fixed Position"
    CAPTURE_BUTTON_TEXT = "Capture Current"
    LIVE_CAPTURE_START_TEXT = "Live Capture"
    LIVE_CAPTURE_STOP_TEXT = "Stop Live"
    
    # ============================================
    # PERFORMANCE WARNING THRESHOLDS
    # ============================================
    WARNING_INSANE_THRESHOLD = 1000    # \\ 1000 CPS
    WARNING_EXTREME_THRESHOLD = 200    # \\ 200-999 CPS
    WARNING_ULTRA_THRESHOLD = 100      # \\ 100-199 CPS
    WARNING_FAST_THRESHOLD = 50        # \\ 50-99 CPS
    
    # ============================================
    # WARNING MESSAGES
    # ============================================
    WARNING_INSANE_MESSAGE = "{cps:,.0f} clicks/second - BEWARE MAY CRASH SYSTEM PAST THIS POINT !!!!"
    WARNING_EXTREME_MESSAGE = "{cps:.0f} clicks/second - Very fast MAY CRASH SYSTEM !!!!"
    WARNING_ULTRA_MESSAGE = "{cps:.0f} clicks/second - Fast MAY CRASH SYSTEM !!!!"
    WARNING_FAST_MESSAGE = "{cps:.0f} clicks/second - Moderate speed"
    
    # ============================================
    # WARNING LEVELS & DISPLAY
    # ============================================
    WARNING_LEVEL_INSANE = "insane"
    WARNING_LEVEL_EXTREME = "extreme"
    WARNING_LEVEL_ULTRA = "ultra"
    WARNING_LEVEL_FAST = "fast"

    WARNING_TEXT_PREFIX = "-> "
    WARNING_ICON_PATH = r"Assets\WarningLogo.png"
    WARNING_ICON_SIZE = (20, 20)
    
    # ============================================
    # NOTE: Order matters for warning priority.
    # Highest priority warnings first for the 
    # loop to iterate through warning levels in
    # check_speed_warning() method
    # ============================================
    WARNING_ORDER = (
        "INSANE",    # \\ Highest priority
        "EXTREME",   # \\ Second priority
        "ULTRA",     # \\ Third priority
        "FAST",      # \\ Lowest priority
    )
    
    # ============================================
    # SIZE POLICIES
    # ============================================
    SIZE_POLICY_PREFERRED = QSizePolicy.Policy.Preferred
    SIZE_POLICY_EXPANDING = QSizePolicy.Policy.Expanding