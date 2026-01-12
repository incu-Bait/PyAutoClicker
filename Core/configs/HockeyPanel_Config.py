from Core.globals.Base_import import *


class HotkeyPanelConfig:
    # ======================
    # DEFAULT SETTINGS
    # ======================
    DEFAULT_HOTKEY = "Shift+E"
    
    # ======================
    # UI DIMENSIONS
    # ======================
    MIN_WIDTH = 230
    MIN_HEIGHT = 230
    
    # ======================
    # UI OBJECT NAMES
    # ======================
    GROUP_BOX_OBJECT_NAME = "hotkeyGroupBox"
    CURRENT_LABEL_OBJECT_NAME = "currentHotkeyLabel"
    HOTKEY_EDIT_OBJECT_NAME = "hotkeyLineEdit"
    APPLY_BUTTON_OBJECT_NAME = "applyHotkeyButton"
    
    # ======================
    # TEXT FORMATS
    # ======================
    GROUP_BOX_TITLE = "Hotkey Settings"
    CURRENT_HOTKEY_LABEL_FORMAT = "Current Hotkey: {hotkey}"
    FORM_LABEL_TEXT = "Set Hotkey:"
    APPLY_BUTTON_TEXT = "Apply Hotkey"
    
    # ======================
    # SIZE POLICIES
    # ======================
    CURRENT_LABEL_SIZE_POLICY_H = QSizePolicy.Policy.Maximum
    CURRENT_LABEL_SIZE_POLICY_V = QSizePolicy.Policy.Preferred

    # ============================================
    # CURSOR
    # ============================================
    TOGGLE_BUTTON_CURSOR = Qt.CursorShape.PointingHandCursor