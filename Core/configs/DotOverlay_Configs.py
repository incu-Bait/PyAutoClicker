from Core.globals.Base_import import *

class DotOverlay_Configs:
    RED_SOLID = QColor(255, 0, 0, 220)    
    RED_TRANSLUCENT = QColor(255, 0, 0, 100)  
    WHITE_SOLID = QColor(255, 255, 255, 220)  
    BLACK_SEMI_TRANSPARENT = QColor(0, 0, 0, 180) 
    
    DOT_COLOR = RED_SOLID
    CROSSHAIR_COLOR = RED_TRANSLUCENT
    TEXT_COLOR = WHITE_SOLID
    TEXT_BG_COLOR = BLACK_SEMI_TRANSPARENT
    
    DOT_RADIUS = 2
    DOT_THICKNESS = 2
    CROSSHAIR_LENGTH = 10
    CROSSHAIR_THICKNESS = 1
    CENTER_RADIUS = 1
    TEXT_FONT_SIZE = 10
    TEXT_OFFSET_X = 15
    TEXT_OFFSET_Y = -25
    
    WINDOW_FLAGS = (
        Qt.WindowType.FramelessWindowHint |
        Qt.WindowType.WindowStaysOnTopHint |
        Qt.WindowType.Tool |
        Qt.WindowType.WindowTransparentForInput
    )
    WIDGET_ATTRIBUTES = (
        Qt.WidgetAttribute.WA_TranslucentBackground,
        Qt.WidgetAttribute.WA_ShowWithoutActivating,
    )
    INITIAL_POSITION = QPoint(0, 0)