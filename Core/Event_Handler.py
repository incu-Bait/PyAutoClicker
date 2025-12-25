# ============================================
# QMW (QMainWindow) Event Handler
# ============================================
# NOTE: "QMW" stands for QMainWindow
# This handles all Main Window events
# OR it should at lease ... 
# ============================================

from Core.globals.Base_import import QDateTime, keyboard, QAction
from Core.configs.Theme_Configs import DEFAULT_THEME
from Core.QDialog.HelpDialog import ShortcutsDialog, AboutDialog
from Core.configs.Windows_Configs import QMW_UIConfig

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
            message = QMW_UIConfig.THEME_CHANGE_MESSAGE_FORMAT.format(
                theme_name=theme_name.title()
            )
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
        try:
            keyboard.remove_hotkey(self.main.hotkey)
            keyboard.add_hotkey(hotkey.lower(), self.toggle_clicking)
            self.main.hotkey = hotkey
            self.main.ui_manager.update_hotkey_ui(hotkey)
            self.main.keybind_manager.keybinds[QMW_UIConfig.KEYBIND_TOGGLE_CLICKING] = hotkey.upper()
            self.main.keybind_manager.save_keybinds_to_file(self.main.keybind_manager.keybinds)
            # --- Show success message ---
            message = QMW_UIConfig.LOG_HOTKEY_CHANGED_FORMAT.format(hotkey=hotkey.upper())
            self.main.statusBar().showMessage(message)
        except Exception as e:
            # --- Show error message ---
            error_message = QMW_UIConfig.LOG_HOTKEY_FAILED_FORMAT.format(error=str(e))
            self.main.statusBar().showMessage(error_message)
            
    def toggle_clicking(self):
        if self.main.clicker.is_running:
            self.main.clicker.is_running = False
            self.main.ui_manager.update_ui(False)
            self.main.statusBar().showMessage(QMW_UIConfig.LOG_STOPPED)
        else:
            self.apply_settings()
            self.main.clicker.is_running = True
            if not self.main.clicker.isRunning():
                self.main.clicker.start()
            self.main.ui_manager.update_ui(True)
            self.main.statusBar().showMessage(QMW_UIConfig.LOG_STARTED)
    
    def update_keybind_shortcuts(self):
        # --- settings panel shortcut ---
        settings_shortcut = self.main.keybind_manager.get_keybind(
            QMW_UIConfig.KEYBIND_TOGGLE_SETTINGS
        )
        if settings_shortcut:
            self.main.ui_manager.settings_toggle.setShortcut(settings_shortcut)
        # --- hotkey panel shortcut ---
        hotkey_shortcut = self.main.keybind_manager.get_keybind(
            QMW_UIConfig.KEYBIND_TOGGLE_HOTKEY
        )
        if hotkey_shortcut:
            self.main.ui_manager.hotkey_toggle.setShortcut(hotkey_shortcut)
        #  --- dot overlay shortcut ---
        dot_shortcut = self.main.keybind_manager.get_keybind(
            QMW_UIConfig.KEYBIND_TOGGLE_DOT
        )
        if dot_shortcut:
            self.main.ui_manager.dot_toggle.setShortcut(dot_shortcut)
        # --- reset layout shortcut ---
        reset_shortcut = self.main.keybind_manager.get_keybind(
            QMW_UIConfig.KEYBIND_RESET_LAYOUT
        )
        if reset_shortcut:
            for action in self.main.findChildren(QAction):
                if action.text() == QMW_UIConfig.ACTION_RESET_LAYOUT_TEXT:
                    action.setShortcut(reset_shortcut)
        # --- theme shortcuts ---
        for theme_name in self.main.theme_manager.get_available_themes():
            theme_key = f"theme_{theme_name.lower().replace(' ', '_')}"
            theme_shortcut = self.main.keybind_manager.get_keybind(theme_key)
            if theme_shortcut:
                for action in self.main.menuBar().actions():
                    if action.menu():
                        menu = action.menu()
                        for menu_action in menu.actions():
                            if menu_action.text().lower() == theme_name.lower():
                                menu_action.setShortcut(theme_shortcut)
                                break
        # --- toggle clicking hotkey ---
        hotkey = self.main.keybind_manager.get_keybind(
            QMW_UIConfig.KEYBIND_TOGGLE_CLICKING
        ) or QMW_UIConfig.DEFAULT_CLICK_BIND
        
        if self.main.clicker.is_running:
            self.main.ui_manager.toggle_btn.setText(
                QMW_UIConfig.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=hotkey.upper())
            )
        else:
            self.main.ui_manager.toggle_btn.setText(
                QMW_UIConfig.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper())
            )
        self.main.hotkey = hotkey
        self.main.statusBar().showMessage(QMW_UIConfig.LOG_KEYBIND_UPDATED)
         
    def on_count(self, count):
        self.main.ui_manager.update_count_ui(count)
        
    def on_position_updated(self, x, y):
        pass # \\ Placeholder for now
        
    def toggle_dot_overlay(self, checked):
        if checked:
            self.main.ui_manager.dot_overlay.show_overlay()
            self.main.statusBar().showMessage(QMW_UIConfig.LOG_DOT_ENABLED)
        else:
            self.main.ui_manager.dot_overlay.hide_overlay()
            self.main.statusBar().showMessage(QMW_UIConfig.LOG_DOT_DISABLED)
            
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
        self.main.addDockWidget(
            QMW_UIConfig.DOCK_AREA_LEFT,
            self.main.settings_dock
        )
        self.main.addDockWidget(
            QMW_UIConfig.DOCK_AREA_RIGHT,
            self.main.hotkey_dock
        )
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