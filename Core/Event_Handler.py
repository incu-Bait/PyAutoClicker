from Core.globals.Base_import import QDateTime, keyboard, QAction
from Core.configs.Theme_Configs import DEFAULT_THEME
from Core.QDialog.HelpDialog import ShortcutsDialog, AboutDialog
from Core.configs.Windows_Configs import PyClickerConstants

## "QMW" (QMainWindow) Just in case i make more then one event handler like a dumbass 
## remember That means "QMainWindow" and handles Main Window Events ... or should at lease 

class QMW_EventHandler:
    def __init__(self, main):
        self.main = main

    def _apply_initial_theme(self):
        default_theme = DEFAULT_THEME
        self.apply_theme(default_theme)
        
    def apply_theme(self, theme_name):
        if self.main.theme_manager.set_theme(theme_name):
            stylesheet = self.main.theme_manager.PyStyleSheet(theme_name)
            self.main.setStyleSheet(stylesheet)
            message = PyClickerConstants.THEME_CHANGE_MESSAGE_FORMAT.format(theme_name=theme_name.title())
            self.main.statusBar().showMessage(message)
            self.main.update() 
            if hasattr(self.main.ui_manager, 'settings_panel'):
                self.main.ui_manager.settings_panel.update()
                
    def apply_settings(self):
        settings = self.main.ui_manager.settings_panel.get_settings()
        self.main.clicker.interval = settings["interval"]
        self.main.clicker.remaining_clicks = settings["remaining_clicks"]
        self.main.clicker.button = settings["button"]
        self.main.clicker.double_click = settings["double_click"]
        self.main.clicker.fixed_pos = settings["fixed_pos"]

    def change_hotkey(self, hotkey):

        keyboard.remove_hotkey(self.main.hotkey)
        keyboard.add_hotkey(hotkey.lower(), self.toggle_clicking)
        self.main.hotkey = hotkey
        self.main.ui_manager.update_hotkey_ui(hotkey)
        self.main.keybind_manager.keybinds["toggle_clicking"] = hotkey.upper()
        self.main.keybind_manager.save_keybinds_to_file(self.main.keybind_manager.keybinds)
            
    def toggle_clicking(self):
        if self.main.clicker.is_running:
            self.main.clicker.is_running = False
            self.main.ui_manager.update_ui(False)
        else:
            self.apply_settings()
            self.main.clicker.is_running = True
            if not self.main.clicker.isRunning():
                self.main.clicker.start()
            self.main.ui_manager.update_ui(True)
    
    def update_keybind_shortcuts(self):
        # # exit_shortcut = self.main.keybind_manager.get_keybind("exit_app")
        # # if exit_shortcut:
        # #     for action in self.main.findChildren(QAction):
        # #         if action.text() == PyClickerConstants.ACTION_EXIT_TEXT:
        # #             action.setShortcut(exit_shortcut)

        settings_shortcut = self.main.keybind_manager.get_keybind("toggle_settings")
        if settings_shortcut:
            self.main.ui_manager.settings_toggle.setShortcut(settings_shortcut)

        hotkey_shortcut = self.main.keybind_manager.get_keybind("toggle_hotkey")
        if hotkey_shortcut:
            self.main.ui_manager.hotkey_toggle.setShortcut(hotkey_shortcut)
        
        dot_shortcut = self.main.keybind_manager.get_keybind("toggle_dot")
        if dot_shortcut:
            self.main.ui_manager.dot_toggle.setShortcut(dot_shortcut)
        
        reset_shortcut = self.main.keybind_manager.get_keybind("reset_layout")
        if reset_shortcut:
            for action in self.main.findChildren(QAction):
                if action.text() == PyClickerConstants.ACTION_RESET_LAYOUT_TEXT:
                    action.setShortcut(reset_shortcut)

        for theme_name in self.main.theme_manager.get_available_themes():
            theme_key = f"theme_{theme_name.lower().replace(' ', '_')}"
            theme_shortcut = self.main.keybind_manager.get_keybind(theme_key)
            if theme_shortcut:
                for action in self.main.menuBar().actions():
                    if action.menu():
                        menu = action.menu()
                        for menu_action in menu.actions():
                            # Match by theme name (case-insensitive)
                            if menu_action.text().lower() == theme_name.lower():
                                menu_action.setShortcut(theme_shortcut)
                                break

        hotkey = self.main.keybind_manager.get_keybind("toggle_clicking") or PyClickerConstants.DEFAULT_CLICK_BIND
        if self.main.clicker.is_running:
            self.main.ui_manager.toggle_btn.setText(PyClickerConstants.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=hotkey.upper()))
        else:
            self.main.ui_manager.toggle_btn.setText(PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper()))
        
        self.main.hotkey = hotkey
         
    def on_count(self, count):
        self.main.ui_manager.update_count_ui(count)
        
    def on_position_updated(self, x, y):
        pass
        
    def toggle_dot_overlay(self, checked):
        if checked:
            self.main.ui_manager.dot_overlay.show_overlay()
        else:
            self.main.ui_manager.dot_overlay.hide_overlay()
            
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
        self.main.ui_manager.dot_toggle.setChecked(False)
        self.main.statusBar().showMessage(PyClickerConstants.LAYOUT_RESET_MESSAGE)
        
    def show_keyboard_shortcuts(self):
        ShortcutsDialog(self.main.keybind_manager, self.main).exec()
            
    def show_about(self):
        AboutDialog(self.main).exec()