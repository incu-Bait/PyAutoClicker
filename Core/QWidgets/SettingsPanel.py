from Core.globals.Base_import import *
from Core.configs.SettingsPanel_Configs import SettingsPanel_Configs
from Core.managers.KeyBindManager import KeybindManager
from Core.managers.FileManager import FileManager
from Core.QWidgets.ui.Settings_Panel_Ui import ClickSettingsUI, TimingSettingsUI, PositionSettingsUI

class SettingsPanel(QWidget):
    apply_triggered = pyqtSignal()
    position_updated = pyqtSignal(int, int)

    def __init__(self, theme_manager: Any, dot_overlay: Any) -> None:
        super().__init__()
        self.theme_manager = theme_manager
        self.dot_overlay = dot_overlay
        self.is_live_capturing = False
        self.keybind_manager = KeybindManager("KeyBinds/key_binds_data.json")
        self.file_manager = FileManager(self.keybind_manager, self)
        self.main_layout = QVBoxLayout(self)
        self._create_warning()
        self.click_ui = ClickSettingsUI(self.main_layout)
        self.timing_ui = TimingSettingsUI(self.main_layout)
        self.position_ui = PositionSettingsUI(self.main_layout, self.file_manager)
        self.main_layout.addStretch()
        self._setup_connections()

    def _create_warning(self) -> None:
        self.warning_frame = QFrame()
        self.warning_frame.setVisible(False)

        layout = QHBoxLayout(self.warning_frame)

        self.warning_icon = QLabel()
        self.warning_icon.setFixedSize(*SettingsPanel_Configs.WARNING_ICON_SIZE)
        self.warning_icon.setObjectName("warning_icon")
        self._load_warning_icon()

        self.warning_label = QLabel()
        self.warning_label.setWordWrap(True)
        self.warning_label.setObjectName("warning_label")

        layout.addWidget(self.warning_icon)
        layout.addWidget(self.warning_label)

        self.main_layout.addWidget(self.warning_frame)

    def _load_warning_icon(self) -> None:
        icon = self._get_warning_icon()
        self.warning_icon.setPixmap(icon.pixmap(20, 20))

    def _get_warning_icon(self) -> QIcon:
        if icon_path := getattr(SettingsPanel_Configs, "WARNING_ICON_PATH", None):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                return QIcon(pixmap)
        return self.style().standardIcon(QStyle.StandardPixmap.SP_MessageBoxWarning)

    def _setup_connections(self) -> None:
        self.position_ui.capture_btn.clicked.connect(self.capture_position)
        self.position_ui.live_capture_btn.toggled.connect(self.toggle_live_capture)
        self.position_ui.overlay_toggle.toggled.connect(self.toggle_overlay)
        self.position_ui.cursor_radio.toggled.connect(self.update_enable_state)
        self.position_ui.fixed_radio.toggled.connect(self.on_fixed_toggled)
        self.timing_ui.interval_spin.valueChanged.connect(self.check_speed_warning)
        self.position_ui.x_spin.valueChanged.connect(self.on_position_changed)
        self.position_ui.y_spin.valueChanged.connect(self.on_position_changed)

    def capture_position(self) -> None:
        x, y = pyautogui.position()
        self.position_ui.x_spin.setValue(x)
        self.position_ui.y_spin.setValue(y)
        self.position_ui.fixed_radio.setChecked(True)

    def toggle_live_capture(self, enabled: bool) -> None:
        if enabled:
            self.capture_timer = QTimer()
            self.capture_timer.timeout.connect(self.live_capture)
            self.capture_timer.start(1000 // SettingsPanel_Configs.LIVE_CAPTURE_FPS)
            self.position_ui.live_capture_btn.setText(SettingsPanel_Configs.LIVE_CAPTURE_STOP_TEXT)
        else:
            if hasattr(self, "capture_timer"):
                self.capture_timer.stop()
            self.position_ui.live_capture_btn.setText(SettingsPanel_Configs.LIVE_CAPTURE_START_TEXT)

    def live_capture(self) -> None:
        x, y = pyautogui.position()
        self.position_ui.x_spin.setValue(x)
        self.position_ui.y_spin.setValue(y)
        self.position_ui.fixed_radio.setChecked(True)

    def toggle_overlay(self, visible: bool) -> None:
        if visible:
            self.dot_overlay.show_overlay()
            self.position_ui.overlay_toggle.setText(SettingsPanel_Configs.OVERLAY_HIDE_TEXT)
            self.update_overlay_position()
        else:
            self.dot_overlay.hide_overlay()
            self.position_ui.overlay_toggle.setText(SettingsPanel_Configs.OVERLAY_SHOW_TEXT)

    def update_overlay_position(self) -> None:
        if self.position_ui.overlay_toggle.isChecked() and self.position_ui.fixed_radio.isChecked():
            x = self.position_ui.x_spin.value()
            y = self.position_ui.y_spin.value()
            self.dot_overlay.set_position(x, y)

    def on_position_changed(self) -> None:
        x = self.position_ui.x_spin.value()
        y = self.position_ui.y_spin.value()
        self.position_ui.pos_label.setText(
            SettingsPanel_Configs.POSITION_LABEL_FORMAT.format(pos=(x, y))
        )
        self.update_overlay_position()
        self.position_updated.emit(x, y)

    def on_fixed_toggled(self, checked: bool) -> None:
        if checked:
            self.update_overlay_position()

    def update_enable_state(self, checked: bool) -> None:
        enabled = self.position_ui.fixed_radio.isChecked()
        self.position_ui.x_spin.setEnabled(enabled)
        self.position_ui.y_spin.setEnabled(enabled)
        self.position_ui.capture_btn.setEnabled(enabled)
        self.position_ui.live_capture_btn.setEnabled(enabled)

    def check_speed_warning(self) -> None:
        interval = self.timing_ui.interval_spin.value()
        if interval <= 0:
            self.warning_frame.setVisible(False)
            return

        cps = 1.0 / interval
        for name in SettingsPanel_Configs.WARNING_ORDER:
            threshold = getattr(SettingsPanel_Configs, f"WARNING_{name}_THRESHOLD")
            level = getattr(SettingsPanel_Configs, f"WARNING_LEVEL_{name}")
            message = getattr(SettingsPanel_Configs, f"WARNING_{name}_MESSAGE")
            if cps >= threshold:
                self.show_warning(level, message.format(cps=cps))
                return

        self.warning_frame.setVisible(False)

    def show_warning(self, level: str, message: str) -> None:
        self.warning_frame.setProperty("warningLevel", level)
        self.warning_frame.style().unpolish(self.warning_frame)
        self.warning_frame.style().polish(self.warning_frame)
        self.warning_frame.update()
        self.warning_frame.setVisible(True)
        self.warning_label.setText(f"{SettingsPanel_Configs.WARNING_TEXT_PREFIX}{message}")

    def get_settings(self) -> Dict[str, Any]:
        return {
            "interval": self.timing_ui.interval_spin.value(),
            "remaining_clicks": self.timing_ui.repeat_spin.value(),
            "button": self.click_ui.button_combo.currentText(),
            "double_click": self.click_ui.double_check.isChecked(),
            "fixed_pos": (
                self.position_ui.x_spin.value(),
                self.position_ui.y_spin.value(),
            )
            if self.position_ui.fixed_radio.isChecked()
            else None,
        }

    def closeEvent(self, event: Any) -> None:
        if hasattr(self, "file_manager"):
            self.file_manager.cleanup()
        super().closeEvent(event)
