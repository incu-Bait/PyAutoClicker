from Core.globals.Base_import import *


class ControlPanel_Config:    
    # ======================
    # CONTROL PANEL LAYOUT
    # ======================
    LEFT_m = 25
    TOP_m = 25
    RIGHT_m = 25
    BOTTOM_m = 25
    CONTROL_PANEL_MARGINS = (LEFT_m, TOP_m, RIGHT_m, BOTTOM_m) 
    CONTROL_PANEL_SPACING = 20
    SEPARATOR_SPACING = 10  
    
    # ======================
    # STATUS SECTION
    # ======================
    STATUS_LAYOUT_SPACING = 10
    
    STATUS_ICON_SIZE = 25
    STATUS_ICON_SIZE_RENDER = 16
    STATUS_ICON_OBJECT_NAME = "statusIcon"

    STATUS_LABEL_OBJECT_NAME = "statusLabel"
    STATUS_STOPPED_TEXT = "STOPPED"
    STATUS_RUNNING_TEXT = "RUNNING"

    COUNT_LABEL_OBJECT_NAME = "countLabel"
    COUNT_DEFAULT_TEXT = "Clicks: 0"
    COUNT_LABEL_FORMAT = "Clicks: {count:,}"
    
    # ======================
    # TOGGLE BUTTON SECTION
    # ======================
    TOGGLE_BUTTON_OBJECT_NAME = "toggleButton"
    TOGGLE_BUTTON_MIN_HEIGHT = 60
    TOGGLE_BUTTON_CURSOR = Qt.CursorShape.PointingHandCursor

    TOGGLE_START_TEXT_FORMAT = "START ({hotkey})"
    TOGGLE_STOP_TEXT_FORMAT = "STOP ({hotkey})"
    
    # ======================
    # SEPARATOR STYLING
    # ======================
    SEPARATOR_OBJECT_NAME = "separator"
    SEPARATOR_FRAME_SHAPE = "HLine"  
    SEPARATOR_FRAME_SHADOW = "Sunken"  
    
    # ======================
    # ICON REFERENCES
    # ======================
    STOP_ICON = "SP_MediaPause" 
    PLAY_ICON = "SP_MediaPlay"   
    
    # ======================
    # ALIGNMENTS
    # ======================
    ICON_ALIGNMENT = Qt.AlignmentFlag.AlignCenter
    STATUS_TEXT_ALIGNMENT = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
    COUNT_TEXT_ALIGNMENT = Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
    
    # ======================
    # LAYOUT POLICIES
    # ======================
    STATUS_SECTION_HAS_STRETCH = True
    CONTROL_PANEL_HAS_STRETCH = True
    
    # ===========================
    # CONTROL PANEL PROP METHODS
    # ===========================
    @staticmethod
    def get_margins():
        margins = ControlPanel_Config.CONTROL_PANEL_MARGINS
        return QMargins(*margins)
    @staticmethod 
    def get_icon_constant(icon_name: str):
        icon_map = {
            "SP_MediaPause": QStyle.StandardPixmap.SP_MediaPause,
            "SP_MediaPlay": QStyle.StandardPixmap.SP_MediaPlay,
        }
        return icon_map.get(icon_name, QStyle.StandardPixmap.SP_ComputerIcon)