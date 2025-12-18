from Core.globals.Base_import import *
from Core.managers.ThemeManager import * 
from Core.configs.Theme_Configs import *
from Core.QThread.ClickThread import ClickerThread
from Core.managers.KeyBindManager import KeybindManager
from Core.QDialog.HelpDialog import ShortcutsDialog, AboutDialog
from Core.configs.Windows_Configs import PyClickerConstants
from Core.managers.Ui_Manager import UIManager
from Core.managers.WindowManager import WindowManager

class PyClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.clicker = ClickerThread()
        self.keybind_manager = KeybindManager("KeyBinds/key_binds_data.json")
        self.hotkey = self.keybind_manager.get_keybind("toggle_clicking") or PyClickerConstants.DEFAULT_CLICK_BIND
        self.window_manager = WindowManager(self)
        self.ui_manager = UIManager(self, self.theme_manager)
        self.window_manager.setup_window()
        self.ui_manager.create_widgets()
        self.ui_manager.create_menus()
        self.ui_manager.create_docks()
        self._setup_connections()
        self._apply_initial_theme()
        
    def _setup_connections(self):
        self.ui_manager.toggle_btn.clicked.connect(self.toggle_clicking)
        self.ui_manager.settings_panel.apply_triggered.connect(self.apply_settings)
        self.ui_manager.hotkey_panel.hotkey_changed.connect(self.change_hotkey)
        self.clicker.status_update.connect(self.on_status)
        self.clicker.click_count_update.connect(self.on_count)
        self.ui_manager.settings_panel.position_updated.connect(self.on_position_updated)
        keyboard.add_hotkey(self.hotkey.lower(), self.toggle_clicking)
        
    def _apply_initial_theme(self):
        default_theme = DEFAULT_THEME
        self.apply_theme(default_theme)
        
    def apply_theme(self, theme_name):
        if self.theme_manager.set_theme(theme_name):
            stylesheet = self.theme_manager.PyStyleSheet(theme_name)
            self.setStyleSheet(stylesheet)
            message = PyClickerConstants.THEME_CHANGE_MESSAGE_FORMAT.format(theme_name=theme_name.title())
            self.statusBar().showMessage(message)
            self.log(PyClickerConstants.LOG_THEME_FORMAT.format(theme_name=theme_name))
            self.update() 
            if hasattr(self.ui_manager, 'settings_panel'):
                self.ui_manager.settings_panel.update()
                
    def log(self, message):
        timestamp = QDateTime.currentDateTime().toString(PyClickerConstants.LOG_TIMESTAMP_FORMAT)
        self.ui_manager.log_text.append(f"[{timestamp}] {message}")
        
    def apply_settings(self):
        settings = self.ui_manager.settings_panel.get_settings()
        self.clicker.interval = settings["interval"]
        self.clicker.remaining_clicks = settings["remaining_clicks"]
        self.clicker.button = settings["button"]
        self.clicker.double_click = settings["double_click"]
        self.clicker.fixed_pos = settings["fixed_pos"]
        self.log(PyClickerConstants.LOG_SETTINGS_APPLIED)
        
    def change_hotkey(self, hotkey):
        try:
            keyboard.remove_hotkey(self.hotkey)
            keyboard.add_hotkey(hotkey.lower(), self.toggle_clicking)
            self.hotkey = hotkey
            self.ui_manager.update_hotkey_ui(hotkey)
            self.keybind_manager.keybinds["toggle_clicking"] = hotkey.upper()
            self.keybind_manager.save_keybinds_to_file(self.keybind_manager.keybinds)
            self.log(PyClickerConstants.LOG_HOTKEY_CHANGED_FORMAT.format(hotkey=hotkey))
        except Exception as e:
            self.log(PyClickerConstants.LOG_HOTKEY_FAILED_FORMAT.format(error=e))
            
    def toggle_clicking(self):
        if self.clicker.is_running:
            self.clicker.is_running = False
            self.ui_manager.update_ui(False)
            self.log(PyClickerConstants.LOG_STOPPED)
        else:
            self.apply_settings()
            self.clicker.is_running = True
            if not self.clicker.isRunning():
                self.clicker.start()
            self.ui_manager.update_ui(True)
            self.log(PyClickerConstants.LOG_STARTED)
    
    def update_keybind_shortcuts(self):
        exit_shortcut = self.keybind_manager.get_keybind("exit_app")
        if exit_shortcut:
            for action in self.findChildren(QAction):
                if action.text() == PyClickerConstants.ACTION_EXIT_TEXT:
                    action.setShortcut(exit_shortcut)

        settings_shortcut = self.keybind_manager.get_keybind("toggle_settings")
        if settings_shortcut:
            self.ui_manager.settings_toggle.setShortcut(settings_shortcut)
        
        log_shortcut = self.keybind_manager.get_keybind("toggle_log")
        if log_shortcut:
            self.ui_manager.log_toggle.setShortcut(log_shortcut)
        
        hotkey_shortcut = self.keybind_manager.get_keybind("toggle_hotkey")
        if hotkey_shortcut:
            self.ui_manager.hotkey_toggle.setShortcut(hotkey_shortcut)
        
        dot_shortcut = self.keybind_manager.get_keybind("toggle_dot")
        if dot_shortcut:
            self.ui_manager.dot_toggle.setShortcut(dot_shortcut)
        
        reset_shortcut = self.keybind_manager.get_keybind("reset_layout")
        if reset_shortcut:
            for action in self.findChildren(QAction):
                if action.text() == PyClickerConstants.ACTION_RESET_LAYOUT_TEXT:
                    action.setShortcut(reset_shortcut)

        for theme_name in self.theme_manager.get_available_themes():
            theme_key = f"theme_{theme_name.replace(' ', '_').lower()}"
            theme_shortcut = self.keybind_manager.get_keybind(theme_key)
            for action in self.menuBar().actions():
                if action.menu():
                    menu = action.menu()
                    for menu_action in menu.actions():
                        if menu_action.text().lower() == theme_name.lower():
                            if theme_shortcut:
                                menu_action.setShortcut(theme_shortcut)

        hotkey = self.keybind_manager.get_keybind("toggle_clicking") or PyClickerConstants.DEFAULT_CLICK_BIND
        if self.clicker.is_running:
            self.ui_manager.toggle_btn.setText(PyClickerConstants.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=hotkey.upper()))
        else:
            self.ui_manager.toggle_btn.setText(PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper()))
        
        self.hotkey = hotkey
        self.log(PyClickerConstants.LOG_KEYBIND_UPDATED) 
        
    def on_status(self, message):
        self.log(message)
        self.statusBar().showMessage(message)
        if PyClickerConstants.LOG_STATUS_STOPPED_KEYWORD in message:
            self.ui_manager.update_ui(False)
            
    def on_count(self, count):
        self.ui_manager.update_count_ui(count)
        
    def on_position_updated(self, x, y):
        pass
        
    def toggle_dot_overlay(self, checked):
        if checked:
            self.ui_manager.dot_overlay.show_overlay()
            self.log(PyClickerConstants.LOG_DOT_ENABLED)
        else:
            self.ui_manager.dot_overlay.hide_overlay()
            self.log(PyClickerConstants.LOG_DOT_DISABLED)
            
    def toggle_settings_panel(self, visible):
        if visible:
            self.settings_dock.show()
        else:
            self.settings_dock.hide()
            
    def toggle_log_panel(self, visible):
        if visible:
            self.log_dock.show()
        else:
            self.log_dock.hide()
            
    def toggle_hotkey_panel(self, visible):
        if visible:
            self.hotkey_dock.show()
        else:
            self.hotkey_dock.hide()
            
    def reset_layout(self):
        self.settings_dock.show()
        self.log_dock.show()
        self.hotkey_dock.show()
        self.ui_manager.settings_toggle.setChecked(True)
        self.ui_manager.log_toggle.setChecked(True)
        self.ui_manager.hotkey_toggle.setChecked(True)
        self.ui_manager.dot_toggle.setChecked(False)
        self.statusBar().showMessage(PyClickerConstants.LAYOUT_RESET_MESSAGE)
        
    def show_keyboard_shortcuts(self):
        ShortcutsDialog(self.keybind_manager, self).exec()
            
    def show_about(self):
        AboutDialog(self).exec()
        
    def closeEvent(self, event):
        # ---- Clean up ----
        self.clicker.is_running = False
        if self.clicker.isRunning():
            self.clicker.wait(1000)
        self.ui_manager.dot_overlay.hide_overlay()
        event.accept()