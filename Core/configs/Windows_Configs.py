# ============================================
# WINDOW CONFIGURATION
# ============================================
from Core.globals.Base_import import *
from PyQt6.QtCore import Qt

class WindowConfig:
    WINDOW_X = 100 
    WINDOW_Y = 100 
    WINDOW_WIDTH = 800
    WINDOW_HEIGHT = 500
    GEOMETRY = (WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
    TITLE = "PyClicker"
    WIDGET_RESIZABLE = True
    DEFAULT_THEME = "dark"
    ICON_PATH = "Assets/PyClickerApp_Logo.ico" 


class QMW_UIConfig:  ## \\ QMW = QMainWindow 
    # ======================
    # DEFAULT / APP SETTINGS 
    # ======================
    DEFAULT_CLICK_BIND = "F6"
    STATUS_READY_MESSAGE = "Ready"
    
    # ======================
    # UI DIMENSIONS
    # ======================
    STATUS_ICON_SIZE = 25
    TOGGLE_BUTTON_MIN_HEIGHT = 60
    LOG_MAX_HEIGHT = 200
    SETTINGS_PANEL_MIN_WIDTH = 325
    SETTINGS_PANEL_MIN_HEIGHT = 325
    HOTKEY_PANEL_MIN_WIDTH = 230
    HOTKEY_PANEL_MIN_HEIGHT = 230
    CENTRAL_WIDGET_MIN_WIDTH = 300
    CENTRAL_WIDGET_MIN_HEIGHT = 200
    INITIAL_DOCK_WIDTHS = [300, 200]
    
    # ======================
    # UI OBJECT NAMES
    # ======================
    STATUS_LABEL_OBJECT_NAME = "statusLabel"
    COUNT_LABEL_OBJECT_NAME = "countLabel"
    TOGGLE_BUTTON_OBJECT_NAME = "toggleButton"
    
    # ======================
    # STATUS DISPLAY
    # ======================
    STATUS_STOPPED_TEXT = "STOPPED"
    STATUS_RUNNING_TEXT = "RUNNING"
    LAYOUT_RESET_MESSAGE = "Layout reset"
    
    # ======================
    # TEXT FORMATS
    # ======================
    TOGGLE_START_TEXT_FORMAT = "START ({hotkey})"
    TOGGLE_STOP_TEXT_FORMAT = "STOP ({hotkey})"
    CURRENT_HOTKEY_LABEL_FORMAT = "Current Hotkey: {hotkey}"
    COUNT_LABEL_FORMAT = "Clicks: {count:,}"
    THEME_CHANGE_MESSAGE_FORMAT = "Theme changed to {theme_name}"
    LOG_TIMESTAMP_FORMAT = "hh:mm:ss"
    
    # ======================
    # MENU SYSTEM
    # ======================
    MENU_FILE = "&File"
    MENU_VIEW = "&View"
    MENU_THEME = "&Theme"
    MENU_HELP = "&Help"

    ACTION_SETTINGS_PANEL_TEXT = "Settings Panel"
    ACTION_LOG_PANEL_TEXT = "Log Panel"
    ACTION_HOTKEY_PANEL_TEXT = "Hotkey Panel"
    ACTION_TOGGLE_DOT_TEXT = "Toggle Dot Overlay"
    ACTION_RESET_LAYOUT_TEXT = "Reset Layout"
    ACTION_KEYBOARD_SHORTCUTS_TEXT = "Keyboard Shortcuts"
    ACTION_ABOUT_TEXT = "About PyClicker"
    ACTION_EXIT_TEXT = "EXIT APP"  
   
    # ======================
    # DOCK WIDGETS
    # ======================
    DOCK_SETTINGS_TITLE = "Settings"
    DOCK_HOTKEY_TITLE = "Hotkey"
    DOCK_LOG_TITLE = "Log"
    # Dock Features \ Combines them \ Allowed areas \ Policy
    DOCK_MOVABLE = QDockWidget.DockWidgetFeature.DockWidgetMovable
    DOCK_FLOATABLE = QDockWidget.DockWidgetFeature.DockWidgetFloatable
    DOCK_CLOSABLE = QDockWidget.DockWidgetFeature.DockWidgetClosable
    DOCK_FEATURES = DOCK_MOVABLE | DOCK_FLOATABLE | DOCK_CLOSABLE # \\ Combines
    DOCK_ALLOWED_LEFT_RIGHT = (
        Qt.DockWidgetArea.LeftDockWidgetArea | 
        Qt.DockWidgetArea.RightDockWidgetArea
    )
    SIZE_POLICY_PREFERRED = QSizePolicy.Policy.Preferred
    DOCK_HORIZONTAL = Qt.Orientation.Horizontal
    
    # ======================
    # ICON REFERENCES
    # ======================
    ICON_ALTERNATIVE = QStyle.StandardPixmap.SP_ComputerIcon
    STOP_ICON = QStyle.StandardPixmap.SP_MediaPause
    PLAY_ICON = QStyle.StandardPixmap.SP_MediaPlay

    # ======================
    # TODO --> Most if not all these const are unused after removing "LogPanel" 
    # TODO --> gotta find out for sure before removing any of them 
    # ======================
    # LOG MESSAGES <-- 
    # ======================
    LOG_STATUS_STOPPED_KEYWORD = "Stopped"
    LOG_THEME_FORMAT = "Theme: {theme_name}"
    LOG_SETTINGS_APPLIED = "Settings applied"
    LOG_STOPPED = "Stopped"
    LOG_STARTED = "Started"
    LOG_DOT_ENABLED = "Dot overlay enabled"
    LOG_DOT_DISABLED = "Dot overlay disabled"
    LOG_KEYBIND_UPDATED = "Keybind shortcuts updated"
    LOG_HOTKEY_CHANGED_FORMAT = "Hotkey changed to {hotkey}"
    LOG_HOTKEY_FAILED_FORMAT = "Failed to apply hotkey: {error}"