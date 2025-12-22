from Core.globals.Base_import import *
from Core.managers.ThemeManager import ThemeManager
from Core.configs.Theme_Configs import *
from Core.QWidgets.DotOverlay import ScreenDotOverlay
from Core.configs.Windows_Configs import WindowConfig, QMW_UIConfig
from Core.QWidgets.SettingsPanel import SettingsPanel
from Core.QWidgets.HotKeyPanel import HotkeyPanel


class UIManager:
    def __init__(self, main_window, theme_manager: ThemeManager) -> None:
        self.main_window = main_window
        self.theme_manager: ThemeManager = theme_manager
        self.dot_overlay: ScreenDotOverlay = ScreenDotOverlay()
        self.settings_panel: Optional[SettingsPanel] = None
        self.hotkey_panel: Optional[HotkeyPanel] = None
        self.is_settings_visible: bool = True
        self.is_hotkey_visible: bool = True
        self.is_dot_visible: bool = False
        self.toggle_btn: Optional[QPushButton] = None
        self.status_icon: Optional[QLabel] = None
        self.status_label: Optional[QLabel] = None
        self.count_label: Optional[QLabel] = None
        self.settings_toggle: Optional[QAction] = None
        self.hotkey_toggle: Optional[QAction] = None
        self.dot_toggle: Optional[QAction] = None
        self.stop_icon = self.main_window.style().standardIcon(QMW_UIConfig.STOP_ICON)
        self.play_icon = self.main_window.style().standardIcon(QMW_UIConfig.PLAY_ICON)

    def create_widgets(self) -> None:
        central = QWidget()
        self.main_window.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Status display ---
        status_layout = QHBoxLayout()
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(
            QMW_UIConfig.STATUS_ICON_SIZE, 
            QMW_UIConfig.STATUS_ICON_SIZE
        )
        self.status_label = QLabel(QMW_UIConfig.STATUS_STOPPED_TEXT)
        self.status_label.setObjectName(QMW_UIConfig.STATUS_LABEL_OBJECT_NAME)

        status_layout.addWidget(self.status_icon)
        status_layout.addWidget(self.status_label)
        status_layout.addSpacing(10)

        self.count_label = QLabel("Clicks: 0")
        self.count_label.setObjectName(QMW_UIConfig.COUNT_LABEL_OBJECT_NAME)
        status_layout.addWidget(self.count_label)
        status_layout.addStretch()

        main_layout.addLayout(status_layout)
        self.update_status_ui(False)

        # --- Main toggle button ---
        self.toggle_btn = QPushButton(
            QMW_UIConfig.TOGGLE_START_TEXT_FORMAT.format(
                hotkey=self.main_window.hotkey.upper()
            )
        )
        self.toggle_btn.setObjectName(QMW_UIConfig.TOGGLE_BUTTON_OBJECT_NAME)
        self.toggle_btn.setMinimumHeight(QMW_UIConfig.TOGGLE_BUTTON_MIN_HEIGHT)
        main_layout.addWidget(self.toggle_btn)

        main_layout.addStretch()

    def create_menus(self) -> None:
        menubar = self.main_window.menuBar()
        
        # --- File menu ---
        file_menu = menubar.addMenu(QMW_UIConfig.MENU_FILE)
        exit_action = QAction("Exit", self.main_window)
        exit_shortcut = self.main_window.keybind_manager.get_keybind("exit_app")
        if exit_shortcut:
            exit_action.setShortcut(exit_shortcut)
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
    
        # --- View menu ---
        view_menu = menubar.addMenu(QMW_UIConfig.MENU_VIEW)

        self.settings_toggle = QAction(
            QMW_UIConfig.ACTION_SETTINGS_PANEL_TEXT, 
            self.main_window
        )
        self.settings_toggle.setCheckable(True)
        self.settings_toggle.setChecked(True)
        settings_shortcut = self.main_window.keybind_manager.get_keybind("toggle_settings")
        if settings_shortcut:
            self.settings_toggle.setShortcut(settings_shortcut)
        self.settings_toggle.triggered.connect(self.main_window.event_handler.toggle_settings_panel)
        view_menu.addAction(self.settings_toggle)

        self.hotkey_toggle = QAction(
            QMW_UIConfig.ACTION_HOTKEY_PANEL_TEXT, 
            self.main_window
        )
        self.hotkey_toggle.setCheckable(True)
        self.hotkey_toggle.setChecked(True)
        hotkey_shortcut = self.main_window.keybind_manager.get_keybind("toggle_hotkey")
        if hotkey_shortcut:
            self.hotkey_toggle.setShortcut(hotkey_shortcut)
        self.hotkey_toggle.triggered.connect(self.main_window.event_handler.toggle_hotkey_panel)
        view_menu.addAction(self.hotkey_toggle)
        view_menu.addSeparator()

        self.dot_toggle = QAction(
            QMW_UIConfig.ACTION_TOGGLE_DOT_TEXT, 
            self.main_window
        )
        self.dot_toggle.setCheckable(True)
        dot_shortcut = self.main_window.keybind_manager.get_keybind("toggle_dot")
        if dot_shortcut:
            self.dot_toggle.setShortcut(dot_shortcut)
        self.dot_toggle.triggered.connect(self.main_window.event_handler.toggle_dot_overlay)
        view_menu.addAction(self.dot_toggle)

        reset_action = QAction(
            QMW_UIConfig.ACTION_RESET_LAYOUT_TEXT, 
            self.main_window
        )
        reset_shortcut = self.main_window.keybind_manager.get_keybind("reset_layout")
        if reset_shortcut:
            reset_action.setShortcut(reset_shortcut)
        reset_action.triggered.connect(self.main_window.event_handler.reset_layout)
        view_menu.addAction(reset_action)

        # --- Theme menu ---
        theme_menu = menubar.addMenu(QMW_UIConfig.MENU_THEME)
        for theme_name in self.theme_manager.get_available_themes():
            action = QAction(theme_name.title(), self.main_window)
            theme_shortcut = self.main_window.keybind_manager.get_keybind(
                f"theme_{theme_name.replace(' ', '_').lower()}"
            )
            if theme_shortcut:
                action.setShortcut(theme_shortcut)
            action.triggered.connect(
                lambda checked, name=theme_name: self.main_window.event_handler.apply_theme(name)
            )
            theme_menu.addAction(action)

        # --- Help menu with shortcuts ---
        help_menu = menubar.addMenu(QMW_UIConfig.MENU_HELP)
        shortcuts_action = QAction(
            QMW_UIConfig.ACTION_KEYBOARD_SHORTCUTS_TEXT, 
            self.main_window
        )
        shortcuts_shortcut = self.main_window.keybind_manager.get_keybind("show_shortcuts")
        if shortcuts_shortcut:
            shortcuts_action.setShortcut(shortcuts_shortcut)
        shortcuts_action.triggered.connect(self.main_window.event_handler.show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)
        help_menu.addSeparator()
        about_action = QAction(
            QMW_UIConfig.ACTION_ABOUT_TEXT, 
            self.main_window
        )
        about_shortcut = self.main_window.keybind_manager.get_keybind("show_about")
        if about_shortcut:
            about_action.setShortcut(about_shortcut)
        about_action.triggered.connect(self.main_window.event_handler.show_about)
        help_menu.addAction(about_action)
    
    def create_docks(self) -> None:
        # --- Settings dock ---
        self.main_window.settings_dock = QDockWidget(
            QMW_UIConfig.DOCK_SETTINGS_TITLE, 
            self.main_window
        )
        self.settings_panel = SettingsPanel(self.theme_manager, self.dot_overlay)
        self.main_window.settings_dock.setWidget(self.settings_panel)
        self.main_window.settings_dock.setFeatures(QMW_UIConfig.DOCK_FEATURES)
        self.main_window.settings_dock.setAllowedAreas(QMW_UIConfig.DOCK_ALLOWED_LEFT_RIGHT)

        self.settings_panel.setSizePolicy(
            QMW_UIConfig.SIZE_POLICY_PREFERRED, 
            QMW_UIConfig.SIZE_POLICY_PREFERRED
        )
        self.settings_panel.setMinimumWidth(QMW_UIConfig.SETTINGS_PANEL_MIN_WIDTH)
        self.settings_panel.setMinimumHeight(QMW_UIConfig.SETTINGS_PANEL_MIN_HEIGHT)
        
        self.main_window.addDockWidget(
            Qt.DockWidgetArea.LeftDockWidgetArea, 
            self.main_window.settings_dock
        )
        # --- Hotkey dock ---
        self.main_window.hotkey_dock = QDockWidget(
            QMW_UIConfig.DOCK_HOTKEY_TITLE, 
            self.main_window
        )
        self.hotkey_panel = HotkeyPanel(self.main_window.hotkey)
        self.main_window.hotkey_dock.setWidget(self.hotkey_panel)
        self.main_window.hotkey_dock.setFeatures(QMW_UIConfig.DOCK_FEATURES)
        self.main_window.hotkey_dock.setAllowedAreas(QMW_UIConfig.DOCK_ALLOWED_LEFT_RIGHT)
        
        self.hotkey_panel.setSizePolicy(
            QMW_UIConfig.SIZE_POLICY_PREFERRED, 
            QMW_UIConfig.SIZE_POLICY_PREFERRED
        )
        self.hotkey_panel.setMinimumWidth(QMW_UIConfig.HOTKEY_PANEL_MIN_WIDTH)
        self.hotkey_panel.setMinimumHeight(QMW_UIConfig.HOTKEY_PANEL_MIN_HEIGHT)
        
        self.main_window.addDockWidget(
            Qt.DockWidgetArea.RightDockWidgetArea, 
            self.main_window.hotkey_dock
        )
        self.main_window.resizeDocks(
            [self.main_window.settings_dock, self.main_window.hotkey_dock],
            QMW_UIConfig.INITIAL_DOCK_WIDTHS,
            QMW_UIConfig.DOCK_HORIZONTAL
        )
        central_widget = self.main_window.centralWidget()
        if central_widget:
            central_widget.setMinimumSize(
                QMW_UIConfig.CENTRAL_WIDGET_MIN_WIDTH, 
                QMW_UIConfig.CENTRAL_WIDGET_MIN_HEIGHT
            )

    def update_status_ui(self, running: bool) -> None:
        if running:
            self.status_icon.setPixmap(self.play_icon.pixmap(16, 16))
            self.status_label.setText(QMW_UIConfig.STATUS_RUNNING_TEXT)
        else:
            self.status_icon.setPixmap(self.stop_icon.pixmap(16, 16))
            self.status_label.setText(QMW_UIConfig.STATUS_STOPPED_TEXT)

    def update_ui(self, running: bool) -> None:
        if running:
            self.toggle_btn.setText(
                QMW_UIConfig.TOGGLE_STOP_TEXT_FORMAT.format(
                    hotkey=self.main_window.hotkey.upper()
                )
            )
        else:
            self.toggle_btn.setText(
                QMW_UIConfig.TOGGLE_START_TEXT_FORMAT.format(
                    hotkey=self.main_window.hotkey.upper()
                )
            )
        self.update_status_ui(running)

    def update_count_ui(self, count: int) -> None:
        self.count_label.setText(QMW_UIConfig.COUNT_LABEL_FORMAT.format(count=count))

    def update_hotkey_ui(self, hotkey: str) -> None:
        self.toggle_btn.setText(
            QMW_UIConfig.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey.upper())
        )
        if self.hotkey_panel:
            self.hotkey_panel.current_label.setText(
                QMW_UIConfig.CURRENT_HOTKEY_LABEL_FORMAT.format(hotkey=hotkey.upper())
            )