from Core.globals.Base_import import *
from Core.managers.ThemeManager import * 
from Core.configs.Theme_Configs import *
from Core.QWidgets.DotOverlay import ScreenDotOverlay
from Core.QThread.ClickThread import ClickerThread
from Core.QWidgets.SettingsPanel import SettingsPanel
from Core.QWidgets.HotKeyPanel import HotkeyPanel
from Core.managers.KeyBindManager import KeybindManager
from Core.QDialog.HelpDialog import ShortcutsDialog, AboutDialog
from Core.configs.Windows_Configs import PyClickerConstants, WindowConfig

class PyClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.theme_manager = ThemeManager()
        self.dot_overlay = ScreenDotOverlay()
        self.clicker = ClickerThread()
        self.keybind_manager = KeybindManager("KeyBinds/key_binds_data.json")
        self.hotkey = self.keybind_manager.get_keybind("toggle_clicking") or PyClickerConstants.DEFAULT_CLICK_BIND
        self._setup_window()
        self._create_widgets()
        self._create_menus()
        self._create_docks()
        self._setup_connections()
        self._apply_initial_theme()
        
    def _setup_window(self):
        self.setWindowTitle(WindowConfig.TITLE)
        self.setGeometry(*WindowConfig.GEOMETRY)
        self.statusBar().showMessage(PyClickerConstants.STATUS_READY_MESSAGE)
        self.icon_dir_setup()

    def icon_dir_setup(self):
        icon_path = os.path.join(os.path.dirname(__file__), "..", WindowConfig.ICON_PATH)
        icon_path = os.path.normpath(icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            self.setWindowIcon(self.style().standardIcon(PyClickerConstants.ICON_ALTERNATIVE))

    def _create_widgets(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # ---- Status display ----
        status_layout = QHBoxLayout()
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(PyClickerConstants.STATUS_ICON_SIZE, PyClickerConstants.STATUS_ICON_SIZE)
        self.status_label = QLabel(PyClickerConstants.STATUS_STOPPED_TEXT)
        self.status_label.setObjectName(PyClickerConstants.STATUS_LABEL_OBJECT_NAME)

        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label)
        status_layout.addSpacing(10) 

        self.count_label = QLabel("Clicks: 0")
        self.count_label.setObjectName(PyClickerConstants.COUNT_LABEL_OBJECT_NAME)
        status_layout.addWidget(self.count_label)
        status_layout.addStretch()
        
        main_layout.addLayout(status_layout)
        
        self.stop_icon = self.style().standardIcon(PyClickerConstants.STOP_ICON)
        self.play_icon = self.style().standardIcon(PyClickerConstants.PLAY_ICON)
        self.update_status_ui(False)
        
        # ---- Main toggle button ----
        self.toggle_btn = QPushButton(PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=self.hotkey.upper()))
        self.toggle_btn.setObjectName(PyClickerConstants.TOGGLE_BUTTON_OBJECT_NAME)
        self.toggle_btn.setMinimumHeight(PyClickerConstants.TOGGLE_BUTTON_MIN_HEIGHT)
        main_layout.addWidget(self.toggle_btn)

        main_layout.addStretch()
        
    def _create_menus(self):
        menubar = self.menuBar()
        
        # # # ---- File menu ----
        # # file_menu = menubar.addMenu(PyClickerConstants.MENU_FILE) # \\ This is Not Needed Right Now
        
        # ---- View menu ----
        view_menu = menubar.addMenu(PyClickerConstants.MENU_VIEW)
        
        self.settings_toggle = QAction(PyClickerConstants.ACTION_SETTINGS_PANEL_TEXT, self)
        self.settings_toggle.setCheckable(True)
        self.settings_toggle.setChecked(True)
        settings_shortcut = self.keybind_manager.get_keybind("toggle_settings")
        if settings_shortcut:
            self.settings_toggle.setShortcut(settings_shortcut)
        self.settings_toggle.triggered.connect(self.toggle_settings_panel)
        view_menu.addAction(self.settings_toggle)
        
        self.log_toggle = QAction(PyClickerConstants.ACTION_LOG_PANEL_TEXT, self)
        self.log_toggle.setCheckable(True)
        self.log_toggle.setChecked(True)
        log_shortcut = self.keybind_manager.get_keybind("toggle_log")
        if log_shortcut:
            self.log_toggle.setShortcut(log_shortcut)
        self.log_toggle.triggered.connect(self.toggle_log_panel)
        view_menu.addAction(self.log_toggle)
        
        self.hotkey_toggle = QAction(PyClickerConstants.ACTION_HOTKEY_PANEL_TEXT, self)
        self.hotkey_toggle.setCheckable(True)
        self.hotkey_toggle.setChecked(True)
        hotkey_shortcut = self.keybind_manager.get_keybind("toggle_hotkey")
        if hotkey_shortcut:
            self.hotkey_toggle.setShortcut(hotkey_shortcut)
        self.hotkey_toggle.triggered.connect(self.toggle_hotkey_panel)
        view_menu.addAction(self.hotkey_toggle)
        view_menu.addSeparator()
        
        self.dot_toggle = QAction(PyClickerConstants.ACTION_TOGGLE_DOT_TEXT, self)
        self.dot_toggle.setCheckable(True)
        dot_shortcut = self.keybind_manager.get_keybind("toggle_dot")
        if dot_shortcut:
            self.dot_toggle.setShortcut(dot_shortcut)
        self.dot_toggle.triggered.connect(self.toggle_dot_overlay)
        view_menu.addAction(self.dot_toggle)
        
        reset_action = QAction(PyClickerConstants.ACTION_RESET_LAYOUT_TEXT, self)
        reset_shortcut = self.keybind_manager.get_keybind("reset_layout")
        if reset_shortcut:
            reset_action.setShortcut(reset_shortcut)
        reset_action.triggered.connect(self.reset_layout)
        view_menu.addAction(reset_action)
        
        # ---- Theme menu ----
        theme_menu = menubar.addMenu(PyClickerConstants.MENU_THEME)
        for theme_name in self.theme_manager.get_available_themes():
            action = QAction(theme_name.title(), self)
            theme_shortcut = self.keybind_manager.get_keybind(f"theme_{theme_name.replace(' ', '_').lower()}")
            if theme_shortcut:
                action.setShortcut(theme_shortcut)
            action.triggered.connect(lambda checked, name=theme_name: self.apply_theme(name))
            theme_menu.addAction(action)
            
        # ---- Help menu with shortcuts ----
        help_menu = menubar.addMenu(PyClickerConstants.MENU_HELP)
        shortcuts_action = QAction(PyClickerConstants.ACTION_KEYBOARD_SHORTCUTS_TEXT, self)
        shortcuts_action.triggered.connect(self.show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)
        help_menu.addSeparator()
        about_action = QAction(PyClickerConstants.ACTION_ABOUT_TEXT, self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
            
    def _create_docks(self):
        # ---- Settings dock ----
        self.settings_dock = QDockWidget(PyClickerConstants.DOCK_SETTINGS_TITLE, self)
        self.settings_panel = SettingsPanel(self.theme_manager, self.dot_overlay)
        self.settings_dock.setWidget(self.settings_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.settings_dock)
        # ---- Hotkey dock ---- 
        self.hotkey_dock = QDockWidget(PyClickerConstants.DOCK_HOTKEY_TITLE, self)
        self.hotkey_panel = HotkeyPanel(self.hotkey)
        self.hotkey_dock.setWidget(self.hotkey_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.hotkey_dock)
        # ---- Log dock ---- 
        self.log_dock = QDockWidget(PyClickerConstants.DOCK_LOG_TITLE, self)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(PyClickerConstants.LOG_MAX_HEIGHT)
        self.log_dock.setWidget(self.log_text)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.log_dock)
        
    def _setup_connections(self):
        self.toggle_btn.clicked.connect(self.toggle_clicking)
        self.settings_panel.apply_triggered.connect(self.apply_settings)
        self.hotkey_panel.hotkey_changed.connect(self.change_hotkey)
        self.clicker.status_update.connect(self.on_status)
        self.clicker.click_count_update.connect(self.on_count)
        self.settings_panel.position_updated.connect(self.on_position_updated)
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
            if hasattr(self, 'settings_panel'):
                self.settings_panel.update()
                
    def log(self, message):
        timestamp = QDateTime.currentDateTime().toString(PyClickerConstants.LOG_TIMESTAMP_FORMAT)
        self.log_text.append(f"[{timestamp}] {message}")
        
    def apply_settings(self):
        settings = self.settings_panel.get_settings()
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
            self.toggle_btn.setText(PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper()))
            self.hotkey_panel.current_label.setText(PyClickerConstants.CURRENT_HOTKEY_LABEL_FORMAT.format(hotkey=hotkey.upper()))
            self.keybind_manager.keybinds["toggle_clicking"] = hotkey.upper()
            self.keybind_manager.save_keybinds_to_file(self.keybind_manager.keybinds)
            self.log(PyClickerConstants.LOG_HOTKEY_CHANGED_FORMAT.format(hotkey=hotkey))
        except Exception as e:
            self.log(PyClickerConstants.LOG_HOTKEY_FAILED_FORMAT.format(error=e))
            
    def toggle_clicking(self):
        if self.clicker.is_running:
            self.clicker.is_running = False
            self.update_ui(False)
            self.log(PyClickerConstants.LOG_STOPPED)
        else:
            self.apply_settings()
            self.clicker.is_running = True
            if not self.clicker.isRunning():
                self.clicker.start()
            self.update_ui(True)
            self.log(PyClickerConstants.LOG_STARTED)
                
    def update_status_ui(self, running):
        if running:
            self.status_icon.setPixmap(self.play_icon.pixmap(16, 16))
            self.status_label.setText(PyClickerConstants.STATUS_RUNNING_TEXT)
        else:
            self.status_icon.setPixmap(self.stop_icon.pixmap(16, 16))
            self.status_label.setText(PyClickerConstants.STATUS_STOPPED_TEXT)
            
    def update_ui(self, running):
        if running:
            self.status_label.setText(PyClickerConstants.STATUS_RUNNING_TEXT)
            self.toggle_btn.setText(PyClickerConstants.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=self.hotkey.upper()))
        else:
            self.status_label.setText(PyClickerConstants.STATUS_STOPPED_TEXT)
            self.toggle_btn.setText(PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=self.hotkey.upper()))
        self.update_status_ui(running)
    
    def update_keybind_shortcuts(self):
        exit_shortcut = self.keybind_manager.get_keybind("exit_app")
        if exit_shortcut:
            for action in self.findChildren(QAction):
                if action.text() == PyClickerConstants.ACTION_EXIT_TEXT:
                    action.setShortcut(exit_shortcut)

        settings_shortcut = self.keybind_manager.get_keybind("toggle_settings")
        if settings_shortcut:
            self.settings_toggle.setShortcut(settings_shortcut)
        
        log_shortcut = self.keybind_manager.get_keybind("toggle_log")
        if log_shortcut:
            self.log_toggle.setShortcut(log_shortcut)
        
        hotkey_shortcut = self.keybind_manager.get_keybind("toggle_hotkey")
        if hotkey_shortcut:
            self.hotkey_toggle.setShortcut(hotkey_shortcut)
        
        dot_shortcut = self.keybind_manager.get_keybind("toggle_dot")
        if dot_shortcut:
            self.dot_toggle.setShortcut(dot_shortcut)
        
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
            self.toggle_btn.setText(PyClickerConstants.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=hotkey.upper()))
        else:
            self.toggle_btn.setText(PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper()))
        
        self.hotkey = hotkey
        self.log(PyClickerConstants.LOG_KEYBIND_UPDATED) 
    def on_status(self, message):
        self.log(message)
        self.statusBar().showMessage(message)
        if PyClickerConstants.LOG_STATUS_STOPPED_KEYWORD in message:
            self.update_ui(False)
            
    def on_count(self, count):
        self.count_label.setText(PyClickerConstants.COUNT_LABEL_FORMAT.format(count=count))
        
    def on_position_updated(self, x, y):
        pass
        
    def toggle_dot_overlay(self, checked):
        if checked:
            self.dot_overlay.show_overlay()
            self.log(PyClickerConstants.LOG_DOT_ENABLED)
        else:
            self.dot_overlay.hide_overlay()
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
        self.settings_toggle.setChecked(True)
        self.log_toggle.setChecked(True)
        self.hotkey_toggle.setChecked(True)
        self.dot_toggle.setChecked(False)
        self.statusBar().showMessage(PyClickerConstants.LAYOUT_RESET_MESSAGE)
        
    def show_keyboard_shortcuts(self):
        keybinds = self.keybind_manager.get_all_keybinds()
        ShortcutsDialog(self.keybind_manager, self).exec()
            
    def show_about(self):
        AboutDialog(self).exec()
        
    def closeEvent(self, event):
        # ---- Clean up ----
        self.clicker.is_running = False
        if self.clicker.isRunning():
            self.clicker.wait(1000)
        # keyboard.remove_hotkey(self.hotkey)
        self.dot_overlay.hide_overlay()
        event.accept()