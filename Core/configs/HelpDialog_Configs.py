class DialogConstants:
    # ============================================
    # ABOUT DIALOG
    # ============================================
    ABOUT_TITLE = "About PyAutoClicker"
    ABOUT_TEXT = (
        "<h2>PyClicker "
        "<span style='color:#666; font-size:6px; font-weight:normal;'>"
        "Made by Riley"
        "</span></h2>"
        "<p>A simple auto clicker app</p>"
        "<ul>"
        "<li>Customizable click settings</li>"
        "<li>Multiple themes</li>"
        "<li>Keyboard shortcuts</li>"
        "<li>Position overlay</li>"
        "<li>Hotkey support</li>"
        "</ul>"
        "<p>Use the Help menu to view all keyboard shortcuts.</p>"
        "<p><b>Warning:</b> Do not exceed the recommended click settings. "
        "There will be a warning when reaching those limits. "
        "Excessive click speeds can cause the application or your system to become unstable or crash.</p>"
    )
    
    # ============================================
    # SHORTCUTS DIALOG \ DIMENSIONS & TEXTS
    # ============================================
    SHORTCUTS_TITLE = "Keyboard Shortcuts"
    SHORTCUTS_MIN_WIDTH = 500
    SHORTCUTS_MIN_HEIGHT = 500
    SHORTCUTS_HEADER_TEXT = "Double-click on a shortcut to edit it"
    
    # ============================================
    # BUTTON TEXTS
    # ============================================
    EDIT_TOGGLE_ENABLED_TEXT = "Editing Enabled"
    EDIT_TOGGLE_DISABLED_TEXT = "Enable Editing"
    RESET_BUTTON_TEXT = "Reset to Defaults"
    SAVE_BUTTON_TEXT = "Save Changes"
    CLOSE_BUTTON_TEXT = "Close"
    
    # ============================================
    # CONFIRMATION DIALOGS
    # ============================================
    RESET_CONFIRM_TITLE = "Reset to Defaults"
    RESET_CONFIRM_TEXT = "Are you sure you want to reset all shortcuts to their default values?"
    SAVE_SUCCESS_TITLE = "Shortcuts Updated"
    SAVE_SUCCESS_TEXT = "Keyboard shortcuts have been updated successfully.\nSome changes may require restarting the application to take full effect."
    SAVE_ERROR_TITLE = "Save Failed"
    SAVE_ERROR_TEXT = "Failed to save shortcuts: {error}"
    UNSAVED_CHANGES_TITLE = "Unsaved Changes"
    UNSAVED_CHANGES_TEXT = "You have unsaved changes. Save before closing?"
    
    # ============================================
    # EDITING
    # ============================================
    EDIT_SHORTCUT_TITLE = "Edit Shortcut"
    EDIT_SHORTCUT_PROMPT = "Enter new shortcut for '{action_desc}':\n(Use format like: Ctrl+S, F6, etc.)"
    
    # ============================================
    # SHORTCUTS TABLE
    # ============================================
    TABLE_HEADERS = ["Description", "Shortcut", "Action"]
    NOT_SET_TEXT = "Not set"