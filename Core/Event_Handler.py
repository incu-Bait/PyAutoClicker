# =================================================================
# QMW (QMainWindow) Event Handler is a
# centralized event handler for all application events
# and funnels to appropriate managers while handling UI coordination
# ===================================================================
from Core.globals.Base_import import keyboard, QAction
from Core.configs.Theme_Configs import DEFAULT_THEME
from Core.QDialog.ShortcutsDialog import ShortcutsDialog
from Core.QDialog.AboutDialog import AboutDialog
from Core.configs.Windows_Configs import QMW_UIConfig
from Core.CustomWidgets.QGroupBox.PyGroupBox import PyGroupBox


class QMW_EventHandler: 
    def __init__(self, main):
        self.main = main
    
    def apply_initial_theme(self):
        self.apply_theme(DEFAULT_THEME)
        
    def apply_theme(self, theme_name):

        if not self.main.theme_manager.set_theme(theme_name):
            return

        stylesheet = self.main.theme_manager.PyStyleSheet(theme_name)
        self.main.setStyleSheet(stylesheet)
        
        for widget in self.main.findChildren(PyGroupBox):
            widget.update_theme(self.main.theme_manager)
        
        if hasattr(self.main.ui_manager, 'settings_panel'): 
            self.main.ui_manager.settings_panel.update()
        self.main.update()
       
        message = QMW_UIConfig.THEME_CHANGE_MESSAGE_FORMAT.format(
            theme_name=theme_name.title()
        )
        self.main.statusBar().showMessage(message)

    def apply_settings(self):
        settings = self.main.ui_manager.settings_panel.get_settings()
        clicker = self.main.clicker
        
        clicker.interval = settings["interval"]
        clicker.remaining_clicks = settings["remaining_clicks"]
        clicker.button = settings["button"]
        clicker.double_click = settings["double_click"]
        clicker.fixed_pos = settings["fixed_pos"]
    
    def change_hotkey(self, hotkey):
        try:
            if not self._validate_hotkey_format(hotkey):
                error_message = f"Invalid hotkey format: {hotkey}"
                self.main.statusBar().showMessage(error_message)
                return
            
            hotkey = hotkey.lower()
            if hasattr(self.main, 'hotkey') and self.main.hotkey:
                try:
                    keyboard.remove_hotkey(self.main.hotkey)
                except (KeyError, ValueError):
                    pass

            keyboard.add_hotkey(hotkey, self.toggle_clicking)
            self.main.hotkey = hotkey
            
            if QMW_UIConfig.KEYBIND_TOGGLE_CLICKING in self.main.keybind_manager.keybinds:
                self.main.keybind_manager.keybinds[QMW_UIConfig.KEYBIND_TOGGLE_CLICKING] = hotkey.upper()
                self.main.keybind_manager.save_keybinds_to_file(self.main.keybind_manager.keybinds)

            self.main.ui_manager.update_hotkey_ui(hotkey)
            self._update_toggle_button_text(hotkey)
            
            message = QMW_UIConfig.LOG_HOTKEY_CHANGED_FORMAT.format(hotkey=hotkey.upper())
            self.main.statusBar().showMessage(message)
            
        except Exception as e:
            error_message = QMW_UIConfig.LOG_HOTKEY_FAILED_FORMAT.format(error=str(e))
            self.main.statusBar().showMessage(error_message)
    
    def _validate_hotkey_format(self, hotkey):
        if not hotkey or not hotkey.strip():
            return False

        parts = hotkey.lower().split('+')
        modifiers = {'ctrl', 'control', 'alt', 'shift', 'win', 'windows', 'cmd', 'super', 'meta'}
        regular_keys = [part for part in parts if part not in modifiers]

        if not regular_keys:
            return False
        
        for key in regular_keys:
            if len(key) > 1 and not key.startswith('f') and not key.isdigit():
                special_keys = {
                    'enter', 'return', 'space', 'tab', 'backspace', 'delete', 
                    'insert', 'home', 'end', 'pageup', 'pagedown',
                    'up', 'down', 'left', 'right', 'escape', 'esc'
                }
                if key not in special_keys:
                    return False
        
        return True
    
    def _update_toggle_button_text(self, hotkey):
        if self.main.clicker.is_running:
            text = QMW_UIConfig.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=hotkey.upper())

    def toggle_clicking(self):
        clicker = self.main.clicker
        if clicker.is_running:
            clicker.is_running = False
            self.main.ui_manager.update_ui(False)
            self.main.statusBar().showMessage(QMW_UIConfig.LOG_STOPPED)
        else:
            self.apply_settings()
            clicker.is_running = True
            
            if not clicker.isRunning():
                clicker.start()
            
            self.main.ui_manager.update_ui(True)
            self.main.statusBar().showMessage(QMW_UIConfig.LOG_STARTED)
    
    def on_count(self, count):
        self.main.ui_manager.update_count_ui(count)
    
    def on_position_updated(self, x, y):
        pass
    
    def update_keybind_shortcuts(self):
        self._update_action_shortcut(
            QMW_UIConfig.ACTION_RESET_LAYOUT_TEXT,
            QMW_UIConfig.KEYBIND_RESET_LAYOUT
        )
        shortcuts_map = {
            QMW_UIConfig.KEYBIND_TOGGLE_SETTINGS: self.main.ui_manager.settings_toggle,
            QMW_UIConfig.KEYBIND_TOGGLE_HOTKEY: self.main.ui_manager.hotkey_toggle,
            QMW_UIConfig.KEYBIND_TOGGLE_DOT: self.main.ui_manager.dot_toggle,
        }
        
        for keybind_name, ui_element in shortcuts_map.items():
            shortcut = self.main.keybind_manager.get_keybind(keybind_name)
            if shortcut and hasattr(ui_element, 'setShortcut'):
                ui_element.setShortcut(shortcut)
        
        for theme_name in self.main.theme_manager.get_available_themes():
            theme_key = f"theme_{theme_name.lower().replace(' ', '_')}"
            theme_shortcut = self.main.keybind_manager.get_keybind(theme_key)
            if theme_shortcut:
                self._update_menu_action_shortcut("Theme", theme_name, theme_key)
        
        hotkey = self.main.keybind_manager.get_keybind(
            QMW_UIConfig.KEYBIND_TOGGLE_CLICKING
        ) or QMW_UIConfig.DEFAULT_CLICK_BIND
        
        self._update_toggle_button_text(hotkey)
        self.main.hotkey = hotkey
        
        self.main.statusBar().showMessage(QMW_UIConfig.LOG_KEYBIND_UPDATED)
    
    def _update_action_shortcut(self, action_text, keybind_name):
        shortcut = self.main.keybind_manager.get_keybind(keybind_name)
        if not shortcut:
            return
        
        for action in self.main.findChildren(QAction):
            if action.text() == action_text:
                action.setShortcut(shortcut)
                return
    
    def _update_menu_action_shortcut(self, menu_text, action_text, keybind_name):
        shortcut = self.main.keybind_manager.get_keybind(keybind_name)
        if not shortcut:
            return
        
        for action in self.main.menuBar().actions():
            if action.menu() and action.text() == menu_text:
                menu = action.menu()
                for menu_action in menu.actions():
                    if menu_action.text().lower() == action_text.lower():
                        menu_action.setShortcut(shortcut)
                        return
    
    def toggle_dot_overlay(self, enabled):
        if enabled:
            self.main.ui_manager.dot_overlay.show_overlay()
            message = QMW_UIConfig.LOG_DOT_ENABLED
        else:
            self.main.ui_manager.dot_overlay.hide_overlay()
            message = QMW_UIConfig.LOG_DOT_DISABLED
        
        self.main.statusBar().showMessage(message)
    
    def toggle_settings_panel(self, visible):
        if visible:
            self.main.settings_dock.show()
        else:
            self.main.settings_dock.hide()
    
    def toggle_hotkey_panel(self, visible):
        if visible:
            self.main.hotkey_dock.show()
        else:
            self.main.hotkey_dock.hide()
    
    def reset_layout(self):
        self.main.settings_dock.show()
        self.main.hotkey_dock.show()
        self.main.ui_manager.settings_toggle.setChecked(True)
        self.main.ui_manager.hotkey_toggle.setChecked(True)
        # --- Position docks ---
        self.main.addDockWidget(
            QMW_UIConfig.DOCK_AREA_LEFT,
            self.main.settings_dock
        )
        self.main.addDockWidget(
            QMW_UIConfig.DOCK_AREA_RIGHT,
            self.main.hotkey_dock
        )
        # --- Resize docks ---
        self.main.resizeDocks(
            [self.main.settings_dock, self.main.hotkey_dock],
            QMW_UIConfig.INITIAL_DOCK_WIDTHS,
            QMW_UIConfig.DOCK_HORIZONTAL
        )
        self.main.statusBar().showMessage(QMW_UIConfig.LAYOUT_RESET_MESSAGE)
    
    def show_keyboard_shortcuts(self):
        ShortcutsDialog(self.main.keybind_manager, self.main).exec()
    
    def show_about(self):
        AboutDialog(self.main).exec()

    def on_keybind_file_changed(self):
        try:
            self.main.keybind_manager.reload_keybinds()
            if hasattr(self.main.ui_manager, 'settings_panel'):
                settings_panel = self.main.ui_manager.settings_panel
                if hasattr(settings_panel, 'keybind_labels'):
                    for action, label_widget in settings_panel.keybind_labels.items():
                        keybind_text = self.main.keybind_manager.get_keybind(action)
                        label_widget.setText(f"<b>{keybind_text}</b>" if keybind_text else "Not set")
                if hasattr(settings_panel, '_update_button_shortcuts'):
                    settings_panel._update_button_shortcuts()
            self.update_keybind_shortcuts()
            self.main.statusBar().showMessage("Keybinds reloaded from file")
            print(f"Keybinds reloaded: {self.main.keybind_manager.keybinds}")
            
        except Exception as e:
            error_msg = f"Error reloading keybinds: {e}"
            self.main.statusBar().showMessage(error_msg)
            print(error_msg)