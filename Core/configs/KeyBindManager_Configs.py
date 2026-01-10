class KeybindConfigs:
# ============================================
# FILE \ CONFIG \ OPERATION MSG \ DEFAULT & DISPLAY 
# ============================================
    CONFIG_FILE = "KeyBinds/key_binds_data.json"
    CREATED_FILE_MESSAGE = "Created new keybinds file: {path}"
    SAVED_MESSAGE = "Saved keybinds to: {path}"
    WARNING_SAVE_MESSAGE = "Warning: Could not save keybinds to {file}: {error}"
    
    # "Key" names mapped to default keyboard shortcuts
    # Empty strings mean no default shortcut assigned.
    DEFAULT_KEYBINDS = {
        "toggle_clicking": "F6",
        "capture_position": "Ctrl+C",
        "toggle_settings": "Ctrl+S",
        "toggle_log": "Ctrl+L",
        "toggle_hotkey": "Ctrl+H",
        "toggle_dot": "Ctrl+D",
        "reset_layout": "Ctrl+R",
        "exit_app": "Ctrl+Q",
        "theme_dark": "",
        "theme_light": "", 
        "theme_neon_green": "",  
        "show_shortcuts": "F1",  
        "show_about": "Ctrl+F1"  
    }

    # Maps "Key" names to be
    # used in UI lists and dialogs
    DISPLAY_NAMES = {
        "toggle_clicking": "Start/Stop Clicker",
        "capture_position": "Capture Position",
        "toggle_settings": "Toggle Settings Panel",
        "toggle_log": "Toggle Log Panel",
        "toggle_hotkey": "Toggle Hotkey Panel",
        "toggle_dot": "Toggle Dot Overlay",
        "reset_layout": "Reset Layout",
        "exit_app": "Exit Application",
        "theme_dark": "Switch to Dark Theme",
        "theme_light": "Switch to Light Theme",
        "theme_neon_green": "Switch to Neon Green Theme",
        "show_shortcuts": "Show Keyboard Shortcuts",
        "show_about": "Show About Dialog"
    }