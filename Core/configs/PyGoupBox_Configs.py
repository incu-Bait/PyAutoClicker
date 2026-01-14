from Core.globals.Base_import import *


class Configs:
    # ======================
    # BORDER ANIMATION DEFAULTS
    # ======================
    BORDER_WIDTH = 2
    BORDER_COLOR = "#888888"
    CORNER_RADIUS = 8
    DASH_PATTERN = [4, 4]  # \\ [dash_length, gap_length]
    
    # ======================
    # ANIMATION TIMING
    # ======================
    ANIMATION_TIMER_INTERVAL = 40 
    DEFAULT_DASH_SPEED = 1.0
    MIN_DASH_SPEED = 0.1
    MAX_DASH_SPEED = 5.0
    
    # ======================
    # TITLE OFFSETS & SPACING
    # ======================
    TITLE_HORIZONTAL_PADDING = 10  
    
    # ======================
    # GROUPBOX STYLES
    # ======================
    GROUPBOX_MARGIN_TOP = "1.2ex"
    GROUPBOX_PADDING_TOP = 10  
    
    # ======================
    # COLOR PRESETS
    # ======================
    COLOR_PRESETS = {
        "default": "#8D8D8D",
        "blue": "#2196F3",
        "green": "#4CAF50",
        "red": "#F44336",
        "orange": "#FF9800",
        "purple": "#9C27B0",
        "cyan": "#00BCD4",
        "yellow": "#FFEB3B"
    }
    
    # ======================
    # ANIMATION PATTERNS
    # ======================
    ANIMATION_PATTERNS = {
        "slow_dash": [6, 4],
        "medium_dash": [4, 4],
        "fast_dash": [2, 2],
        "dotted": [1, 3],
        "long_dash": [8, 4],
        "dash_dot": [4, 2, 1, 2]
    }
    
    # ======================
    # ANIMATION STATES
    # ======================
    ANIMATION_STATE_RUNNING = "running"
    ANIMATION_STATE_STOPPED = "stopped"
    ANIMATION_STATE_PAUSED = "paused"
    
    # ======================
    # BORDER STYLES (Qt Constants)
    # ======================
    PEN_STYLE_DASHED = Qt.PenStyle.DashLine
    PEN_STYLE_SOLID = Qt.PenStyle.SolidLine
    PEN_STYLE_DOTTED = Qt.PenStyle.DotLine
    PEN_STYLE_DASH_DOT = Qt.PenStyle.DashDotLine
    PEN_STYLE_CUSTOM = Qt.PenStyle.CustomDashLine
    
    # ======================
    # RENDER HINTS
    # ======================
    RENDER_ANTIALIASING = QPainter.RenderHint.Antialiasing
    
    # ======================
    # ANIMATION OBJECT NAMES
    # ======================
    BORDER_TIMER_OBJECT_NAME = "borderAnimationTimer"
    
    # ======================
    # ERROR MESSAGES
    # ======================
    ERROR_INVALID_COLOR = "Invalid color format. Use hex (#RRGGBB) or named Qt colors."
    ERROR_INVALID_SPEED = "Animation speed must be between {min} and {max}."
    ERROR_INVALID_PATTERN = "Dash pattern must be a list of positive numbers."
    
    # ======================
    # VALIDATION RANGES
    # ======================
    BORDER_WIDTH_MIN = 1
    BORDER_WIDTH_MAX = 10
    CORNER_RADIUS_MIN = 0
    CORNER_RADIUS_MAX = 50
    ANIMATION_INTERVAL_MIN = 10  
    ANIMATION_INTERVAL_MAX = 1000 

    # ======================
    # TITLE CONFIGURATION
    # ======================
    TITLE_SUBCONTROL_ORIGIN = "margin"
    TITLE_SUBCONTROL_POSITION = "top center"
    
    # ======================
    # INITIAL VALUES
    # ======================
    INITIAL_DASH_OFFSET = 0.0
    INITIAL_BORDER_COLOR = BORDER_COLOR
    INITIAL_BORDER_WIDTH = 2
    INITIAL_DASH_PATTERN = [4, 4]
    INITIAL_CORNER_RADIUS = 8
    INITIAL_DASH_SPEED = 1.0
    
    # ======================
    # TIMER CONFIGURATION
    # ======================
    TIMER_SINGLE_SHOT = False
    TIMER_PRECISION = Qt.TimerType.PreciseTimer
    
    # ======================
    # DRAWING CONSTANTS
    # ======================
    PEN_CAP_STYLE = Qt.PenCapStyle.FlatCap
    PEN_JOIN_STYLE = Qt.PenJoinStyle.MiterJoin
    BRUSH_STYLE = Qt.BrushStyle.NoBrush
    
    # ======================
    # FONT METRICS
    # ======================
    EXTRA_SPACING = 8  
    
    # ======================
    # RECTANGLE CALCULATION
    # ======================
    RECTANGLE_INSET = 1