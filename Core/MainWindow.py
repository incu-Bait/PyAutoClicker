from Core.globals.Base_import import QMainWindow, keyboard
from Core.managers.ThemeManager import ThemeManager 
from Core.QThread.ClickThread import ClickerThread
from Core.managers.KeyBindManager import KeybindManager
from Core.configs.Windows_Configs import PyClickerConstants
from Core.managers.Ui_Manager import UIManager
from Core.managers.WindowManager import WindowManager
from Core.Event_Handler import QMW_EventHandler

class PyClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.clicker = ClickerThread()
        self.window_manager = WindowManager(self)
        self.event_handler = QMW_EventHandler(self)        
        self.ui_manager = UIManager(self, self.theme_manager)       
        self.keybind_manager = KeybindManager("KeyBinds/key_binds_data.json")
        self.hotkey = self.keybind_manager.get_keybind("toggle_clicking") or PyClickerConstants.DEFAULT_CLICK_BIND
        self.window_manager.setup_window()
        self.ui_manager.create_widgets()
        self.ui_manager.create_menus()
        self.ui_manager.create_docks()
        self._setup_connections()
        self.event_handler._apply_initial_theme()
        
    def _setup_connections(self):
        self.ui_manager.toggle_btn.clicked.connect(self.event_handler.toggle_clicking)
        self.ui_manager.settings_panel.apply_triggered.connect(self.event_handler.apply_settings)
        self.ui_manager.hotkey_panel.hotkey_changed.connect(self.event_handler.change_hotkey)
        self.clicker.status_update.connect(self.event_handler.on_status)
        self.clicker.click_count_update.connect(self.event_handler.on_count)
        self.ui_manager.settings_panel.position_updated.connect(self.event_handler.on_position_updated)
        keyboard.add_hotkey(self.hotkey.lower(), self.event_handler.toggle_clicking)
        
    def closeEvent(self, event):
        # ---- Clean up ----
        self.clicker.is_running = False
        if self.clicker.isRunning():
            self.clicker.wait(1000)
        self.ui_manager.dot_overlay.hide_overlay()
        event.accept()