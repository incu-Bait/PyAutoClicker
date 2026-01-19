from Core.globals.Base_import import *
from PyQt6.QtCore import Qt


class WindowConfig:
    # ======================
    # WINDOW GEOMETRY
    # ======================
    WINDOW_X = 100 
    WINDOW_Y = 100 
    WINDOW_WIDTH = 900
    WINDOW_HEIGHT = 510
    GEOMETRY = (WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
    
    # ======================
    # WINDOW PROPERTIES
    # ======================
    TITLE = "PyClicker"
    WIDGET_RESIZABLE = True
    DEFAULT_THEME = "dark"
    ICON_PATH = "Assets/PyClickerApp_Logo.ico"


class QMW_UIConfig: # \\ QMW = QMainWindow 
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
    # LAYOUT MARGINS
    # ======================
    CENTRAL_LAYOUT_MARGIN = 20
    STATUS_LAYOUT_SPACING = 10
    
    # ======================
    # UI OBJECT NAMES
    # ======================
    CENTRAL_WIDGET_OBJECT_NAME = "centralWidget"
    STATUS_ICON_OBJECT_NAME = "statusIcon"
    STATUS_LABEL_OBJECT_NAME = "statusLabel"
    COUNT_LABEL_OBJECT_NAME = "countLabel"
    TOGGLE_BUTTON_OBJECT_NAME = "toggleButton"
    
    SETTINGS_DOCK_OBJECT_NAME = "settingsDock"
    HOTKEY_DOCK_OBJECT_NAME = "hotkeyDock"
    
    MENUBAR_OBJECT_NAME = "mainMenuBar"
    FILE_MENU_OBJECT_NAME = "fileMenu"
    VIEW_MENU_OBJECT_NAME = "viewMenu"
    THEME_MENU_OBJECT_NAME = "themeMenu"
    HELP_MENU_OBJECT_NAME = "helpMenu"
    
    # ======================
    # STATUS DISPLAY
    # ======================
    STATUS_STOPPED_TEXT = "STOPPED"
    STATUS_RUNNING_TEXT = "RUNNING"
    LAYOUT_RESET_MESSAGE = "Layout reset"
    COUNT_DEFAULT_TEXT = "Clicks: 0"
    
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
    # MENU SYSTEM - TITLES
    # ======================
    MENU_FILE = "&File"
    MENU_VIEW = "&View"
    MENU_THEME = "&Theme"
    MENU_HELP = "&Help"
    
    # ======================
    # MENU SYSTEM - ACTIONS
    # ======================
    ACTION_EXIT_TEXT = "Exit"
    ACTION_SETTINGS_PANEL_TEXT = "Settings Panel"
    ACTION_LOG_PANEL_TEXT = "Log Panel"
    ACTION_HOTKEY_PANEL_TEXT = "Hotkey Panel"
    ACTION_TOGGLE_DOT_TEXT = "Toggle Dot Overlay"
    ACTION_RESET_LAYOUT_TEXT = "Reset Layout"
    ACTION_KEYBOARD_SHORTCUTS_TEXT = "Keyboard Shortcuts"
    ACTION_ABOUT_TEXT = "About PyClicker"
   
    # ======================
    # DOCK WIDGETS - TITLES
    # ======================
    DOCK_SETTINGS_TITLE = "Settings"
    DOCK_HOTKEY_TITLE = "Hotkey"
    DOCK_LOG_TITLE = "Log"
    
    # ======================
    # DOCK WIDGETS - FEATURES
    # ======================
    DOCK_MOVABLE = QDockWidget.DockWidgetFeature.DockWidgetMovable
    DOCK_FLOATABLE = QDockWidget.DockWidgetFeature.DockWidgetFloatable
    DOCK_CLOSABLE = QDockWidget.DockWidgetFeature.DockWidgetClosable
    DOCK_FEATURES = DOCK_MOVABLE | DOCK_FLOATABLE | DOCK_CLOSABLE
    
    # ======================
    # DOCK WIDGETS - AREAS
    # ======================
    DOCK_ALLOWED_LEFT_RIGHT = (
        Qt.DockWidgetArea.LeftDockWidgetArea | 
        Qt.DockWidgetArea.RightDockWidgetArea
    )
    DOCK_AREA_LEFT = Qt.DockWidgetArea.LeftDockWidgetArea
    DOCK_AREA_RIGHT = Qt.DockWidgetArea.RightDockWidgetArea
    
    # ======================
    # SIZE POLICIES
    # ======================
    SIZE_POLICY_PREFERRED = QSizePolicy.Policy.Preferred
    SIZE_POLICY_EXPANDING = QSizePolicy.Policy.Expanding
    SIZE_POLICY_MINIMUM = QSizePolicy.Policy.Minimum
    SIZE_POLICY_MAXIMUM = QSizePolicy.Policy.Maximum
    
    # ======================
    # ORIENTATIONS
    # ======================
    DOCK_HORIZONTAL = Qt.Orientation.Horizontal
    DOCK_VERTICAL = Qt.Orientation.Vertical
    
    # ======================
    # ICON REFERENCES
    # ======================
    ICON_ALTERNATIVE = QStyle.StandardPixmap.SP_ComputerIcon
    STOP_ICON = QStyle.StandardPixmap.SP_MediaPause
    PLAY_ICON = QStyle.StandardPixmap.SP_MediaPlay
    STATUS_ICON_SIZE_RENDER = 16
    CURSOR_ICON = Qt.CursorShape.PointingHandCursor
    # ======================
    # KEYBIND KEYS
    # ======================
    KEYBIND_EXIT_APP = "exit_app"
    KEYBIND_TOGGLE_SETTINGS = "toggle_settings"
    KEYBIND_TOGGLE_HOTKEY = "toggle_hotkey"
    KEYBIND_TOGGLE_DOT = "toggle_dot"
    KEYBIND_RESET_LAYOUT = "reset_layout"
    KEYBIND_SHOW_SHORTCUTS = "show_shortcuts"
    KEYBIND_SHOW_ABOUT = "show_about"
    KEYBIND_TOGGLE_CLICKING = "toggle_clicking"
    
    # ======================
    # LOG MESSAGES
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