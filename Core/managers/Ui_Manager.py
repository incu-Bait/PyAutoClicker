from Core.globals.Base_import import *  
from Core.managers.ThemeManager import ThemeManager
from Core.configs.Theme_Configs import *  
from Core.QWidgets.DotOverlay import ScreenDotOverlay
from Core.configs.Windows_Configs import PyClickerConstants
from Core.QWidgets.SettingsPanel import SettingsPanel
from Core.QWidgets.HotKeyPanel import HotkeyPanel

class UIManager:
    def __init__(self, main_window, theme_manager: ThemeManager):
        self.main_window = main_window
        self.theme_manager = theme_manager
        self.dot_overlay = ScreenDotOverlay()
        self.settings_panel: SettingsPanel | None = None
        self.hotkey_panel: HotkeyPanel | None = None
        self.log_text: QTextEdit | None = None
        self.is_settings_visible = True
        self.is_log_visible = True
        self.is_hotkey_visible = True
        self.is_dot_visible = False
        self.toggle_btn: QPushButton | None = None
        self.status_icon: QLabel | None = None
        self.status_label: QLabel | None = None
        self.count_label: QLabel | None = None
        self.settings_toggle: QAction | None = None
        self.log_toggle: QAction | None = None
        self.hotkey_toggle: QAction | None = None
        self.dot_toggle: QAction | None = None
        self.stop_icon = self.main_window.style().standardIcon(PyClickerConstants.STOP_ICON)
        self.play_icon = self.main_window.style().standardIcon(PyClickerConstants.PLAY_ICON)

    def create_widgets(self):
        central = QWidget()
        self.main_window.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Status display ---
        status_layout = QHBoxLayout()
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(
            PyClickerConstants.STATUS_ICON_SIZE, PyClickerConstants.STATUS_ICON_SIZE
        )
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
        self.update_status_ui(False)

        # --- Main toggle button ---
        self.toggle_btn = QPushButton(
            PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(
                hotkey=self.main_window.hotkey.upper()
            )
        )
        self.toggle_btn.setObjectName(PyClickerConstants.TOGGLE_BUTTON_OBJECT_NAME)
        self.toggle_btn.setMinimumHeight(PyClickerConstants.TOGGLE_BUTTON_MIN_HEIGHT)
        main_layout.addWidget(self.toggle_btn)

        main_layout.addStretch()

    def create_menus(self):
        menubar = self.main_window.menuBar()

        # --- View menu ---
        view_menu = menubar.addMenu(PyClickerConstants.MENU_VIEW)

        self.settings_toggle = QAction(
            PyClickerConstants.ACTION_SETTINGS_PANEL_TEXT, self.main_window
        )
        self.settings_toggle.setCheckable(True)
        self.settings_toggle.setChecked(True)
        settings_shortcut = self.main_window.keybind_manager.get_keybind("toggle_settings")
        if settings_shortcut:
            self.settings_toggle.setShortcut(settings_shortcut)
        self.settings_toggle.triggered.connect(self.main_window.toggle_settings_panel)
        view_menu.addAction(self.settings_toggle)

        self.log_toggle = QAction(PyClickerConstants.ACTION_LOG_PANEL_TEXT, self.main_window)
        self.log_toggle.setCheckable(True)
        self.log_toggle.setChecked(True)
        log_shortcut = self.main_window.keybind_manager.get_keybind("toggle_log")
        if log_shortcut:
            self.log_toggle.setShortcut(log_shortcut)
        self.log_toggle.triggered.connect(self.main_window.toggle_log_panel)
        view_menu.addAction(self.log_toggle)

        self.hotkey_toggle = QAction(
            PyClickerConstants.ACTION_HOTKEY_PANEL_TEXT, self.main_window
        )
        self.hotkey_toggle.setCheckable(True)
        self.hotkey_toggle.setChecked(True)
        hotkey_shortcut = self.main_window.keybind_manager.get_keybind("toggle_hotkey")
        if hotkey_shortcut:
            self.hotkey_toggle.setShortcut(hotkey_shortcut)
        self.hotkey_toggle.triggered.connect(self.main_window.toggle_hotkey_panel)
        view_menu.addAction(self.hotkey_toggle)
        view_menu.addSeparator()

        self.dot_toggle = QAction(PyClickerConstants.ACTION_TOGGLE_DOT_TEXT, self.main_window)
        self.dot_toggle.setCheckable(True)
        dot_shortcut = self.main_window.keybind_manager.get_keybind("toggle_dot")
        if dot_shortcut:
            self.dot_toggle.setShortcut(dot_shortcut)
        self.dot_toggle.triggered.connect(self.main_window.toggle_dot_overlay)
        view_menu.addAction(self.dot_toggle)

        reset_action = QAction(PyClickerConstants.ACTION_RESET_LAYOUT_TEXT, self.main_window)
        reset_shortcut = self.main_window.keybind_manager.get_keybind("reset_layout")
        if reset_shortcut:
            reset_action.setShortcut(reset_shortcut)
        reset_action.triggered.connect(self.main_window.reset_layout)
        view_menu.addAction(reset_action)

        # --- Theme menu ---
        theme_menu = menubar.addMenu(PyClickerConstants.MENU_THEME)
        for theme_name in self.theme_manager.get_available_themes():
            action = QAction(theme_name.title(), self.main_window)
            theme_shortcut = self.main_window.keybind_manager.get_keybind(
                f"theme_{theme_name.replace(' ', '_').lower()}"
            )
            if theme_shortcut:
                action.setShortcut(theme_shortcut)
            action.triggered.connect(
                lambda checked, name=theme_name: self.main_window.apply_theme(name)
            )
            theme_menu.addAction(action)

        # --- Help menu with shortcuts ---
        help_menu = menubar.addMenu(PyClickerConstants.MENU_HELP)
        shortcuts_action = QAction(
            PyClickerConstants.ACTION_KEYBOARD_SHORTCUTS_TEXT, self.main_window
        )
        shortcuts_action.triggered.connect(self.main_window.show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)
        help_menu.addSeparator()
        about_action = QAction(PyClickerConstants.ACTION_ABOUT_TEXT, self.main_window)
        about_action.triggered.connect(self.main_window.show_about)
        help_menu.addAction(about_action)

    def create_docks(self):
        # --- Settings dock ---
        self.main_window.settings_dock = QDockWidget(
            PyClickerConstants.DOCK_SETTINGS_TITLE, self.main_window
        )
        self.settings_panel = SettingsPanel(self.theme_manager, self.dot_overlay)
        self.main_window.settings_dock.setWidget(self.settings_panel)
        self.main_window.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea, self.main_window.settings_dock
        )
        # --- Hotkey dock ---
        self.main_window.hotkey_dock = QDockWidget(
            PyClickerConstants.DOCK_HOTKEY_TITLE, self.main_window
        )
        self.hotkey_panel = HotkeyPanel(self.main_window.hotkey)
        self.main_window.hotkey_dock.setWidget(self.hotkey_panel)
        self.main_window.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea, self.main_window.hotkey_dock
        )
        # --- Log dock ---
        self.main_window.log_dock = QDockWidget(
            PyClickerConstants.DOCK_LOG_TITLE, self.main_window
        )
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(PyClickerConstants.LOG_MAX_HEIGHT)
        self.main_window.log_dock.setWidget(self.log_text)
        self.main_window.addDockWidget(
            Qt.DockWidgetArea.BottomDockWidgetArea, self.main_window.log_dock
        )

    def update_status_ui(self, running: bool):
        if running:
            self.status_icon.setPixmap(self.play_icon.pixmap(16, 16))
            self.status_label.setText(PyClickerConstants.STATUS_RUNNING_TEXT)
        else:
            self.status_icon.setPixmap(self.stop_icon.pixmap(16, 16))
            self.status_label.setText(PyClickerConstants.STATUS_STOPPED_TEXT)

    def update_ui(self, running: bool):
        if running:
            self.toggle_btn.setText(
                PyClickerConstants.TOGGLE_STOP_TEXT_FORMAT.format(
                    hotkey=self.main_window.hotkey.upper()
                )
            )
        else:
            self.toggle_btn.setText(
                PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(
                    hotkey=self.main_window.hotkey.upper()
                )
            )
        self.update_status_ui(running)

    def update_count_ui(self, count: int):
        self.count_label.setText(PyClickerConstants.COUNT_LABEL_FORMAT.format(count=count))

    def update_hotkey_ui(self, hotkey: str):
        self.toggle_btn.setText(
            PyClickerConstants.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper())
        )
        if self.hotkey_panel:
            self.hotkey_panel.current_label.setText(
                PyClickerConstants.CURRENT_HOTKEY_LABEL_FORMAT.format(hotkey=hotkey.upper())
            )