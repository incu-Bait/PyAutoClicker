from Core.globals.Base_import import QMainWindow, keyboard
from Core.managers.ThemeManager import ThemeManager 
from Core.QThread.ClickThread import ClickerThread
from Core.managers.KeyBindManager import KeybindManager
from Core.configs.Windows_Configs import QMW_UIConfig
from Core.managers.Ui_Manager import UIManager
from Core.managers.WindowManager import WindowManager
from Core.Event_Handler import QMW_EventHandler
from Core.managers.FileManager import FileManager


class PyClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.keybind_manager = KeybindManager("KeyBinds/key_binds_data.json")
        self.event_handler = QMW_EventHandler(self)
        self.window_manager = WindowManager(self)
        self.ui_manager = UIManager(self, self.theme_manager)
        self.file_manager = FileManager(self.keybind_manager, self.event_handler)
        self.clicker = ClickerThread()
        self.hotkey = self.keybind_manager.get_keybind("toggle_clicking") or QMW_UIConfig.DEFAULT_CLICK_BIND
        self.window_manager.setup_window()
        self.ui_manager.create_widgets()
        self.ui_manager.create_menus()
        self.ui_manager.create_docks()
        self._setup_connections()
        self.event_handler.apply_initial_theme()
        self.event_handler.update_keybind_shortcuts()
        
    def _setup_connections(self):
        self.ui_manager.control_panel.toggle_button.clicked.connect(self.event_handler.toggle_clicking)
        self.ui_manager.settings_panel.apply_triggered.connect(self.event_handler.apply_settings)
        self.ui_manager.hotkey_panel.hotkey_changed.connect(self.event_handler.change_hotkey)
        self.clicker.click_count_update.connect(self.event_handler.on_count)
        self.ui_manager.settings_panel.position_updated.connect(self.event_handler.on_position_updated)
        keyboard.add_hotkey(self.hotkey.lower(), self.event_handler.toggle_clicking)
        
    def closeEvent(self, event):
        self.clicker.is_running = False
        if self.clicker.isRunning():
            self.clicker.wait(1000)  # \\ This i guess should give thread time to finish ... 
        self.ui_manager.dot_overlay.hide_overlay()
        self.file_manager.cleanup()
        try:
            keyboard.remove_hotkey(self.hotkey.lower())
        except (KeyError, ValueError):
            pass  # \\ if the hotkey wasn't registered or already removed
        
        event.accept()