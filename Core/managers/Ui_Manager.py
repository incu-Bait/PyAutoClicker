# ============================================
# UI Manager
# ============================================
# Manages all UI creation and updates
# Creates menus, docks, and central widgets
# then funnels events to EventHandler
# ============================================
from Core.globals.Base_import import *
from Core.managers.ThemeManager import ThemeManager
from Core.configs.Theme_Configs import *
from Core.QWidgets.DotOverlay import ScreenDotOverlay
from Core.configs.Windows_Configs import QMW_UIConfig
from Core.QWidgets.SettingsPanel import SettingsPanel
from Core.QWidgets.HotKeyPanel import HotkeyPanel
from Core.QWidgets.ControlPanel import ControlPanel
from Core.CustomWidgets.QGroupBox.PyGroupBox import PyGroupBox


class UIManager:
    def __init__(self, main_window, theme_manager: ThemeManager) -> None:
        self.main_window = main_window
        self.theme_manager = theme_manager
        self.dot_overlay = ScreenDotOverlay()
        self.settings_panel: Optional[SettingsPanel] = None
        self.hotkey_panel: Optional[HotkeyPanel] = None
        self.control_panel: Optional[ControlPanel] = None
        self.is_settings_visible = True
        self.is_hotkey_visible = True
        self.is_dot_visible = False
        self.settings_toggle: Optional[QAction] = None
        self.hotkey_toggle: Optional[QAction] = None
        self.dot_toggle: Optional[QAction] = None
        self.toggle_btn: Optional[QPushButton] = None  
    
    def create_widgets(self) -> None:
        # Central widget with control panel
        central = QWidget()
        central.setObjectName(QMW_UIConfig.CENTRAL_WIDGET_OBJECT_NAME)
        self.main_window.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        margin = QMW_UIConfig.CENTRAL_LAYOUT_MARGIN
        main_layout.setContentsMargins(margin, margin, margin, margin)
        control_frame = self._create_control_panel()
        main_layout.addWidget(control_frame)
        main_layout.addStretch()
    
    def _create_control_panel(self) -> PyGroupBox:
        frame = PyGroupBox(title="Control Panel")
        frame.update()
        
        layout = QVBoxLayout(frame)
        self.control_panel = ControlPanel(self.main_window)
        layout.addWidget(self.control_panel)

        self.toggle_btn = self.control_panel.toggle_button
        
        return frame
    
    def create_menus(self) -> None:
        menubar = self.main_window.menuBar()
        menubar.setObjectName(QMW_UIConfig.MENUBAR_OBJECT_NAME)
        
        self._create_file_menu(menubar)
        self._create_view_menu(menubar)
        self._create_theme_menu(menubar)
        self._create_help_menu(menubar)
    
    def _create_file_menu(self, menubar):
        file_menu = menubar.addMenu(QMW_UIConfig.MENU_FILE)
        file_menu.setObjectName(QMW_UIConfig.FILE_MENU_OBJECT_NAME)
        
        exit_action = QAction(QMW_UIConfig.ACTION_EXIT_TEXT, self.main_window)
        shortcut = self.main_window.keybind_manager.get_keybind(QMW_UIConfig.KEYBIND_EXIT_APP)
        if shortcut:
            exit_action.setShortcut(shortcut)
        exit_action.triggered.connect(self.main_window.close)
        file_menu.addAction(exit_action)
    
    def _create_view_menu(self, menubar):
        view_menu = menubar.addMenu(QMW_UIConfig.MENU_VIEW)
        view_menu.setObjectName(QMW_UIConfig.VIEW_MENU_OBJECT_NAME)
        
        self.settings_toggle = self._create_checkable_action(
            QMW_UIConfig.ACTION_SETTINGS_PANEL_TEXT,
            self.main_window.event_handler.toggle_settings_panel,
            QMW_UIConfig.KEYBIND_TOGGLE_SETTINGS
        )
        self.hotkey_toggle = self._create_checkable_action(
            QMW_UIConfig.ACTION_HOTKEY_PANEL_TEXT,
            self.main_window.event_handler.toggle_hotkey_panel,
            QMW_UIConfig.KEYBIND_TOGGLE_HOTKEY
        )
        
        view_menu.addAction(self.settings_toggle)
        view_menu.addAction(self.hotkey_toggle)
        view_menu.addSeparator()
        
        reset_action = QAction(QMW_UIConfig.ACTION_RESET_LAYOUT_TEXT, self.main_window)
        shortcut = self.main_window.keybind_manager.get_keybind(QMW_UIConfig.KEYBIND_RESET_LAYOUT)
        if shortcut:
            reset_action.setShortcut(shortcut)
        reset_action.triggered.connect(self.main_window.event_handler.reset_layout)
        view_menu.addAction(reset_action)
    
    def _create_theme_menu(self, menubar):
        theme_menu = menubar.addMenu(QMW_UIConfig.MENU_THEME)
        theme_menu.setObjectName(QMW_UIConfig.THEME_MENU_OBJECT_NAME)
        
        for theme_name in self.theme_manager.get_available_themes():
            action = QAction(theme_name.title(), self.main_window)
            
            theme_key = f"theme_{theme_name.replace(' ', '_').lower()}"
            shortcut = self.main_window.keybind_manager.get_keybind(theme_key)
            if shortcut:
                action.setShortcut(shortcut)
            
            action.triggered.connect(
                lambda _, name=theme_name: self.main_window.event_handler.apply_theme(name)
            )
            theme_menu.addAction(action)
    
    def _create_help_menu(self, menubar):
        help_menu = menubar.addMenu(QMW_UIConfig.MENU_HELP)
        help_menu.setObjectName(QMW_UIConfig.HELP_MENU_OBJECT_NAME)
        
        shortcuts_action = QAction(QMW_UIConfig.ACTION_KEYBOARD_SHORTCUTS_TEXT, self.main_window)
        shortcut = self.main_window.keybind_manager.get_keybind(QMW_UIConfig.KEYBIND_SHOW_SHORTCUTS)
        if shortcut:
            shortcuts_action.setShortcut(shortcut)
        shortcuts_action.triggered.connect(self.main_window.event_handler.show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)
        help_menu.addSeparator()
        
        about_action = QAction(QMW_UIConfig.ACTION_ABOUT_TEXT, self.main_window)
        shortcut = self.main_window.keybind_manager.get_keybind(QMW_UIConfig.KEYBIND_SHOW_ABOUT)
        if shortcut:
            about_action.setShortcut(shortcut)
        about_action.triggered.connect(self.main_window.event_handler.show_about)
        help_menu.addAction(about_action)
    
    def _create_checkable_action(self, text, callback, keybind_name) -> QAction:
        action = QAction(text, self.main_window)
        action.setCheckable(True)
        action.setChecked(True)
        
        shortcut = self.main_window.keybind_manager.get_keybind(keybind_name)
        if shortcut:
            action.setShortcut(shortcut)
        
        action.triggered.connect(callback)
        return action
    
    def create_docks(self) -> None:
        self._create_settings_dock()
        self._create_hotkey_dock()
        self.main_window.resizeDocks(
            [self.main_window.settings_dock, self.main_window.hotkey_dock],
            QMW_UIConfig.INITIAL_DOCK_WIDTHS,
            QMW_UIConfig.DOCK_HORIZONTAL
        )
        central = self.main_window.centralWidget()
        if central:
            central.setMinimumSize(
                QMW_UIConfig.CENTRAL_WIDGET_MIN_WIDTH, 
                QMW_UIConfig.CENTRAL_WIDGET_MIN_HEIGHT
            )
    
    def _create_settings_dock(self):
        self.main_window.settings_dock = QDockWidget(
            QMW_UIConfig.DOCK_SETTINGS_TITLE, 
            self.main_window
        )
        self.main_window.settings_dock.setObjectName(QMW_UIConfig.SETTINGS_DOCK_OBJECT_NAME)
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
            QMW_UIConfig.DOCK_AREA_LEFT, 
            self.main_window.settings_dock
        )
    
    def _create_hotkey_dock(self):
        self.main_window.hotkey_dock = QDockWidget(
            QMW_UIConfig.DOCK_HOTKEY_TITLE, 
            self.main_window
        )
        self.main_window.hotkey_dock.setObjectName(QMW_UIConfig.HOTKEY_DOCK_OBJECT_NAME)
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
            QMW_UIConfig.DOCK_AREA_RIGHT, 
            self.main_window.hotkey_dock
        )

    def update_ui(self, running: bool) -> None:
        if self.control_panel:
            self.control_panel.update_ui(running)
            self.control_panel.update_status_ui(running)
    
    def update_count_ui(self, count: int) -> None:
        if self.control_panel:
            self.control_panel.update_count_ui(count)
    
    def update_hotkey_ui(self, hotkey: str) -> None:
        if self.control_panel:
            self.control_panel.update_hotkey_ui(hotkey)
        
        if self.hotkey_panel:
            self.hotkey_panel.current_label.setText(
                QMW_UIConfig.CURRENT_HOTKEY_LABEL_FORMAT.format(hotkey=hotkey.upper())
            )