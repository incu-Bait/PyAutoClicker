# ============================================
# WINDOW CONFIGURATION
# ============================================
from Core.globals.Base_import import *

class WindowConfig:
    WINDOWS_X = 100 
    WINDOWS_Y = 100 
    WINDOWS_WIDTH = 700
    WINDOWS_HEIGHT = 500
    TITLE = "PyClicker"
    GEOMETRY = (WINDOWS_X, WINDOWS_Y, WINDOWS_WIDTH, WINDOWS_HEIGHT)
    WIDGET_RESIZABLE = True
    DEFAULT_THEME = "dark"
    ICON_PATH = "Assets\PyClickerApp_Logo.ico"

class PyClickerConstants:
    DEFAULT_CLICK_BIND = "F6"
    STATUS_READY_MESSAGE = "Ready"
    ICON_ALTERNATIVE = QStyle.StandardPixmap.SP_ComputerIcon
    STATUS_ICON_SIZE = 25
    STATUS_LABEL_OBJECT_NAME = "statusLabel"
    COUNT_LABEL_OBJECT_NAME = "countLabel"
    TOGGLE_BUTTON_OBJECT_NAME = "toggleButton"
    TOGGLE_BUTTON_MIN_HEIGHT = 60
    STOP_ICON = QStyle.StandardPixmap.SP_MediaPause
    PLAY_ICON = QStyle.StandardPixmap.SP_MediaPlay
    STATUS_STOPPED_TEXT = "STOPPED"
    STATUS_RUNNING_TEXT = "RUNNING"
    MENU_FILE = "&File"
    ACTION_EXIT_TEXT = "E&xit"
    MENU_VIEW = "&View"
    ACTION_SETTINGS_PANEL_TEXT = "Settings Panel"
    ACTION_LOG_PANEL_TEXT = "Log Panel"
    ACTION_HOTKEY_PANEL_TEXT = "Hotkey Panel"
    ACTION_TOGGLE_DOT_TEXT = "Toggle Dot Overlay"
    ACTION_RESET_LAYOUT_TEXT = "Reset Layout"
    MENU_THEME = "&Theme"
    MENU_HELP = "&Help"
    ACTION_KEYBOARD_SHORTCUTS_TEXT = "Keyboard Shortcuts"
    ACTION_ABOUT_TEXT = "About PyClicker"
    DOCK_SETTINGS_TITLE = "Settings"
    DOCK_HOTKEY_TITLE = "Hotkey"
    DOCK_LOG_TITLE = "Log"
    LOG_MAX_HEIGHT = 200
    LOG_TIMESTAMP_FORMAT = "hh:mm:ss"
    THEME_CHANGE_MESSAGE_FORMAT = "Theme changed to {theme_name}"
    LOG_THEME_FORMAT = "Theme: {theme_name}"
    LOG_SETTINGS_APPLIED = "Settings applied"
    LOG_HOTKEY_CHANGED_FORMAT = "Hotkey changed to {hotkey}"
    LOG_HOTKEY_FAILED_FORMAT = "Failed to apply hotkey: {error}"
    LOG_STOPPED = "Stopped"
    LOG_STARTED = "Started"
    TOGGLE_START_TEXT_FORMAT = "START ({hotkey})"
    TOGGLE_STOP_TEXT_FORMAT = "STOP ({hotkey})"
    CURRENT_HOTKEY_LABEL_FORMAT = "Current Hotkey: {hotkey}"
    LOG_STATUS_STOPPED_KEYWORD = "Stopped"
    COUNT_LABEL_FORMAT = "Clicks: {count:,}"
    LOG_DOT_ENABLED = "Dot overlay enabled"
    LOG_DOT_DISABLED = "Dot overlay disabled"
    LAYOUT_RESET_MESSAGE = "Layout reset"
    LOG_KEYBIND_UPDATED = "Keybind shortcuts updated"
