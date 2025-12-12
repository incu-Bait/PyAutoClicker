from Core.globals.Base_import import *
from Core.configs.SettingsPanel_Configs import SettingsPanel_Configs
from Core.managers.KeyBindManager import KeybindManager
from Core.managers.FileManager import FileManager

class SettingsPanel(QWidget):
    apply_triggered = pyqtSignal()
    position_updated = pyqtSignal(int, int)
    
    def __init__(self, theme_manager: Any, dot_overlay: Any) -> None:
        super().__init__()
        self.theme_manager: Any = theme_manager
        self.dot_overlay: Any = dot_overlay
        self.is_live_capturing: bool = False
        self.keybind_manager: KeybindManager = KeybindManager("KeyBinds/key_binds_data.json")
        self.file_manager: FileManager = FileManager(self.keybind_manager, self)
        self.main_layout: QVBoxLayout = QVBoxLayout(self)
        self._create_widgets()
        self._setup_connections()
        
    def _create_widgets(self) -> None:
        # ---- Speed Warning Display ----
        self.warning_frame: QFrame = QFrame()
        self.warning_frame.setVisible(False)
        warning_layout: QHBoxLayout = QHBoxLayout(self.warning_frame)
        self.warning_icon: QLabel = QLabel()
        self.warning_icon.setFixedSize(*SettingsPanel_Configs.WARNING_ICON_SIZE)
        self.warning_icon.setObjectName("warning_icon")
        self._load_warning_icon()
        
        warning_layout.addWidget(self.warning_icon)
        self.warning_label: QLabel = QLabel()
        self.warning_label.setWordWrap(True)
        self.warning_label.setObjectName("warning_label")
        warning_layout.addWidget(self.warning_label)
        
        self.main_layout.addWidget(self.warning_frame)
        
        # ---- Click Settings ----
        click_group: QGroupBox = QGroupBox(SettingsPanel_Configs.CLICK_GROUP_TITLE)
        click_layout: QFormLayout = QFormLayout(click_group)
        self.button_combo: QComboBox = QComboBox()
        self.button_combo.addItems(SettingsPanel_Configs.BUTTON_OPTIONS)
        click_layout.addRow("Button:", self.button_combo)
        self.double_check: QCheckBox = QCheckBox(SettingsPanel_Configs.DOUBLE_CLICK_TEXT)
        click_layout.addRow("", self.double_check)
        self.main_layout.addWidget(click_group)
        
        # ---- Timing Settings ----
        timing_group: QGroupBox = QGroupBox(SettingsPanel_Configs.TIMING_GROUP_TITLE)
        timing_layout: QFormLayout = QFormLayout(timing_group)
        
        self.interval_spin: QDoubleSpinBox = QDoubleSpinBox()
        self.interval_spin.setRange(
            SettingsPanel_Configs.MIN_INTERVAL, 
            SettingsPanel_Configs.MAX_INTERVAL
        )
        self.interval_spin.setValue(SettingsPanel_Configs.DEFAULT_INTERVAL)
        self.interval_spin.setSingleStep(SettingsPanel_Configs.INTERVAL_STEP)
        self.interval_spin.setDecimals(SettingsPanel_Configs.INTERVAL_DECIMALS)
        self.interval_spin.setSuffix(SettingsPanel_Configs.INTERVAL_SUFFIX)
        timing_layout.addRow("Interval:", self.interval_spin)
        
        self.repeat_spin: QSpinBox = QSpinBox()
        self.repeat_spin.setRange(0, SettingsPanel_Configs.MAX_REPEAT)
        self.repeat_spin.setValue(0)
        self.repeat_spin.setSpecialValueText(SettingsPanel_Configs.REPEAT_SPECIAL_TEXT)
        timing_layout.addRow("Repeat:", self.repeat_spin)
        self.main_layout.addWidget(timing_group)
        
        # ---- Position Settings ----
        pos_group: QGroupBox = QGroupBox(SettingsPanel_Configs.POSITION_GROUP_TITLE)
        pos_layout: QVBoxLayout = QVBoxLayout(pos_group)
        
        pos_display: QHBoxLayout = QHBoxLayout()
        self.pos_label: QLabel = QLabel(SettingsPanel_Configs.POSITION_LABEL_FORMAT.format(pos=SettingsPanel_Configs.INITIAL_POSITION))
        pos_display.addWidget(self.pos_label)
        self.overlay_toggle: QPushButton = QPushButton(SettingsPanel_Configs.OVERLAY_SHOW_TEXT)
        self.overlay_toggle.setCheckable(True)
        self.overlay_toggle.setChecked(False)
        pos_display.addWidget(self.overlay_toggle)
        pos_layout.addLayout(pos_display)
        
        pos_controls: QHBoxLayout = QHBoxLayout()
        self.cursor_radio: QRadioButton = QRadioButton(SettingsPanel_Configs.CURSOR_RADIO_TEXT)
        self.cursor_radio.setChecked(True)
        self.fixed_radio: QRadioButton = QRadioButton(SettingsPanel_Configs.FIXED_RADIO_TEXT)
        pos_controls.addWidget(self.cursor_radio)
        pos_controls.addWidget(self.fixed_radio)
        pos_layout.addLayout(pos_controls)
        
        pos_form: QFormLayout = QFormLayout()
        self.x_spin: QSpinBox = QSpinBox()
        self.x_spin.setRange(0, SettingsPanel_Configs.MAX_POSITION)
        self.x_spin.setValue(SettingsPanel_Configs.INITIAL_POSITION[0])
        pos_form.addRow("X:", self.x_spin)
        self.y_spin: QSpinBox = QSpinBox()
        self.y_spin.setRange(0, SettingsPanel_Configs.MAX_POSITION)
        self.y_spin.setValue(SettingsPanel_Configs.INITIAL_POSITION[1])
        pos_form.addRow("Y:", self.y_spin)
        pos_layout.addLayout(pos_form)
        
        capture_layout: QHBoxLayout = QHBoxLayout()
        self.capture_btn: QPushButton = QPushButton(SettingsPanel_Configs.CAPTURE_BUTTON_TEXT)
        capture_shortcut: Optional[str] = self.file_manager.get_keybind("capture_position")
        self.capture_btn.setShortcut(capture_shortcut if capture_shortcut else QKeySequence())
        capture_layout.addWidget(self.capture_btn)
        self.live_capture_btn: QPushButton = QPushButton(SettingsPanel_Configs.LIVE_CAPTURE_START_TEXT)
        self.live_capture_btn.setCheckable(True)
        live_shortcut: Optional[str] = self.file_manager.get_keybind("toggle_live_capture")
        self.live_capture_btn.setShortcut(live_shortcut if live_shortcut else QKeySequence())
        capture_layout.addWidget(self.live_capture_btn)
        pos_layout.addLayout(capture_layout)
        self.main_layout.addWidget(pos_group)

        # ---- Apply Button ----
        self.apply_btn: QPushButton = QPushButton(SettingsPanel_Configs.APPLY_BUTTON_TEXT)
        apply_shortcut: Optional[str] = self.file_manager.get_keybind("quick_apply")
        self.apply_btn.setShortcut(apply_shortcut if apply_shortcut else QKeySequence())
        self.main_layout.addWidget(self.apply_btn)
        self.main_layout.addStretch()
    
    def _load_warning_icon(self) -> None:
        icon = self._get_warning_icon()
        self.warning_icon.setPixmap(icon.pixmap(20, 20))
    
    def _get_warning_icon(self) -> QIcon:
        if icon_path := getattr(SettingsPanel_Configs, 'WARNING_ICON_PATH', None):
            custom_pixmap = QPixmap(icon_path)
            if not custom_pixmap.isNull():
                return QIcon(custom_pixmap)
        # ---- fallback to system icon ----
        return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)
    
    def _update_button_shortcuts(self) -> None:
        capture_shortcut: Optional[str] = self.file_manager.get_keybind("capture_position")
        self.capture_btn.setShortcut(capture_shortcut if capture_shortcut else QKeySequence())
        apply_shortcut: Optional[str] = self.file_manager.get_keybind("quick_apply")
        self.apply_btn.setShortcut(apply_shortcut if apply_shortcut else QKeySequence())
        live_shortcut: Optional[str] = self.file_manager.get_keybind("toggle_live_capture")
        self.live_capture_btn.setShortcut(live_shortcut if live_shortcut else QKeySequence())
        
    def _setup_connections(self) -> None:
        self.capture_btn.clicked.connect(self.capture_position)
        self.live_capture_btn.toggled.connect(self.toggle_live_capture)
        self.overlay_toggle.toggled.connect(self.toggle_overlay)
        self.cursor_radio.toggled.connect(self.update_enable_state)
        self.fixed_radio.toggled.connect(self.on_fixed_toggled)
        self.apply_btn.clicked.connect(self.apply_triggered.emit)
        self.interval_spin.valueChanged.connect(self.check_speed_warning)
        self.x_spin.valueChanged.connect(self.on_position_changed)
        self.y_spin.valueChanged.connect(self.on_position_changed)
        self._update_button_shortcuts()
    
    def capture_position(self) -> None:
        x: int
        y: int
        x, y = pyautogui.position()
        self.x_spin.setValue(x)
        self.y_spin.setValue(y)
        self.fixed_radio.setChecked(True)
        
    def toggle_live_capture(self, enabled: bool) -> None:
        if enabled:
            self.capture_timer: QTimer = QTimer()
            self.capture_timer.timeout.connect(self.live_capture)
            self.capture_timer.start(1000 // SettingsPanel_Configs.LIVE_CAPTURE_FPS)
            self.live_capture_btn.setText(SettingsPanel_Configs.LIVE_CAPTURE_STOP_TEXT)
        else:
            if hasattr(self, 'capture_timer'):
                self.capture_timer.stop()
            self.live_capture_btn.setText(SettingsPanel_Configs.LIVE_CAPTURE_START_TEXT)
            
    def live_capture(self) -> None:
        x: int
        y: int
        x, y = pyautogui.position()
        self.x_spin.setValue(x)
        self.y_spin.setValue(y)
        self.fixed_radio.setChecked(True)
        
    def toggle_overlay(self, visible: bool) -> None:
        if visible:
            self.dot_overlay.show_overlay()
            self.overlay_toggle.setText(SettingsPanel_Configs.OVERLAY_HIDE_TEXT)
            self.update_overlay_position()
        else:
            self.dot_overlay.hide_overlay()
            self.overlay_toggle.setText(SettingsPanel_Configs.OVERLAY_SHOW_TEXT)
            
    def update_overlay_position(self) -> None:
        if self.overlay_toggle.isChecked() and self.fixed_radio.isChecked():
            x: int = self.x_spin.value()
            y: int = self.y_spin.value()
            self.dot_overlay.set_position(x, y)
            
    def on_position_changed(self) -> None:
        x: int = self.x_spin.value()
        y: int = self.y_spin.value()
        self.pos_label.setText(SettingsPanel_Configs.POSITION_LABEL_FORMAT.format(pos=(x, y)))
        self.update_overlay_position()
        self.position_updated.emit(x, y)
        
    def on_fixed_toggled(self, checked: bool) -> None:
        if checked:
            self.update_overlay_position()
            
    def update_enable_state(self, checked: bool) -> None:
        enabled: bool = self.fixed_radio.isChecked()
        self.x_spin.setEnabled(enabled)
        self.y_spin.setEnabled(enabled)
        self.capture_btn.setEnabled(enabled)
        self.live_capture_btn.setEnabled(enabled)
        
    def check_speed_warning(self) -> None:
        interval: float = self.interval_spin.value()
        if interval <= 0:
            self.warning_frame.setVisible(False)
            return
        clicks_per_second: float = 1.0 / interval
        if clicks_per_second >= SettingsPanel_Configs.WARNING_INSANE_THRESHOLD:
            message = SettingsPanel_Configs.WARNING_INSANE_MESSAGE.format(cps=clicks_per_second)
            self.show_warning(SettingsPanel_Configs.WARNING_LEVEL_INSANE, message)
        elif clicks_per_second >= SettingsPanel_Configs.WARNING_EXTREME_THRESHOLD:
            message = SettingsPanel_Configs.WARNING_EXTREME_MESSAGE.format(cps=clicks_per_second)
            self.show_warning(SettingsPanel_Configs.WARNING_LEVEL_EXTREME, message)
        elif clicks_per_second >= SettingsPanel_Configs.WARNING_ULTRA_THRESHOLD:
            message = SettingsPanel_Configs.WARNING_ULTRA_MESSAGE.format(cps=clicks_per_second)
            self.show_warning(SettingsPanel_Configs.WARNING_LEVEL_ULTRA, message)
        elif clicks_per_second >= SettingsPanel_Configs.WARNING_FAST_THRESHOLD:
            message = SettingsPanel_Configs.WARNING_FAST_MESSAGE.format(cps=clicks_per_second)
            self.show_warning(SettingsPanel_Configs.WARNING_LEVEL_FAST, message)
        else:
            self.warning_frame.setVisible(False)
          
    def show_warning(self, level: str, message: str) -> None:
        self.warning_frame.setProperty("warningLevel", level)
        self.warning_frame.style().unpolish(self.warning_frame)
        self.warning_frame.style().polish(self.warning_frame)
        self.warning_frame.update()
        if not self.warning_icon.objectName():
            self.warning_icon.setObjectName("warning_icon")
        if not self.warning_label.objectName():
            self.warning_label.setObjectName("warning_label")
        self.warning_frame.setVisible(True)
        self.warning_label.setText(f"{SettingsPanel_Configs.WARNING_TEXT_PREFIX}{message}")
        
    def get_settings(self) -> Dict[str, Any]:
        return {
            "interval": self.interval_spin.value(),
            "remaining_clicks": self.repeat_spin.value(),
            "button": self.button_combo.currentText(),
            "double_click": self.double_check.isChecked(),
            "fixed_pos": (self.x_spin.value(), self.y_spin.value()) if self.fixed_radio.isChecked() else None,
        }
    
    def closeEvent(self, event: Any) -> None:
        if hasattr(self, 'file_manager'):
            self.file_manager.cleanup()
        super().closeEvent(event)