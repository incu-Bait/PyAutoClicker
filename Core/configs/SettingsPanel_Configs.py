class SettingsPanel_Configs:
    # ============================================
    # LIMITS & DEFAULTS
    # ============================================
    MIN_INTERVAL = 0.001
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
    BUTTON_OPTIONS = ["left", "right", "middle"]
    DOUBLE_CLICK_TEXT = "Double click"
    
    # ============================================
    # TIMING SETTINGS
    # ============================================
    TIMING_GROUP_TITLE = "Timing"
    INTERVAL_SUFFIX = " s"
    INTERVAL_DECIMALS = 4
    INTERVAL_STEP = 0.001
    REPEAT_SPECIAL_TEXT = "Infinite"
    
    # ============================================
    # POSITION SETTINGS
    # ============================================
    POSITION_GROUP_TITLE = "Position"
    POSITION_LABEL_FORMAT = "Screen Position: {pos}"
    OVERLAY_SHOW_TEXT = "Show Dot"
    OVERLAY_HIDE_TEXT = "Hide Dot"
    CURSOR_RADIO_TEXT = "Current Position"
    FIXED_RADIO_TEXT = "Fixed Position"
    CAPTURE_BUTTON_TEXT = "Capture Current"
    LIVE_CAPTURE_START_TEXT = "Live Capture"
    LIVE_CAPTURE_STOP_TEXT = "Stop Live"
    APPLY_BUTTON_TEXT = "APPLY SETTINGS"
    
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
    # NOTE: Order dose matter.  
    # Highest priority warnings first 
    # for the Simply for loop to iterate 
    # through warning levels ---> check_speed_warning()
    # in "SettingsPanel.py"
    # ============================================   
    # WARNING ORDER 
    # ============================================
    WARNING_ORDER = (
        "INSANE",    # \\ Highest priority
        "EXTREME",   # \\ Second priority
        "ULTRA",     # \\ Third priority
        "FAST",      # \\ Lowest priority
    )