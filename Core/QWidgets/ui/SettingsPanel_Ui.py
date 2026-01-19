from Core.globals.Base_import import *
from Core.configs.SettingsPanel_Configs import SettingsPanel_Configs
from Core.managers.FileManager import FileManager
from Core.custom_widgets.QGroupBox.PyGroupBox import PyGroupBox


class ClickSettingsUI:
    def __init__(self, parent: QVBoxLayout):
        self.group = PyGroupBox(SettingsPanel_Configs.CLICK_GROUP_TITLE)
        self.group.setObjectName(SettingsPanel_Configs.CLICK_GROUP_OBJECT_NAME)
        self.group.setCursor(SettingsPanel_Configs.TOGGLE_BUTTON_CURSOR)
        layout = QFormLayout(self.group)

        self.button_combo = QComboBox()
        self.button_combo.setObjectName(SettingsPanel_Configs.BUTTON_COMBO_OBJECT_NAME)
        self.button_combo.addItems(SettingsPanel_Configs.BUTTON_OPTIONS)
        self.double_check = QCheckBox(SettingsPanel_Configs.DOUBLE_CLICK_TEXT)
        self.double_check.setObjectName(SettingsPanel_Configs.DOUBLE_CHECK_OBJECT_NAME)

        layout.addRow(SettingsPanel_Configs.BUTTON_LABEL_TEXT, self.button_combo)
        layout.addRow("", self.double_check)

        parent.addWidget(self.group)


class TimingSettingsUI:
    def __init__(self, parent: QVBoxLayout):
        self.group = PyGroupBox(SettingsPanel_Configs.TIMING_GROUP_TITLE)
        self.group.setObjectName(SettingsPanel_Configs.TIMING_GROUP_OBJECT_NAME)
        self.group.setCursor(SettingsPanel_Configs.TOGGLE_BUTTON_CURSOR)        
        layout = QFormLayout(self.group)

        self.interval_spin = QDoubleSpinBox()
        self.interval_spin.setObjectName(SettingsPanel_Configs.INTERVAL_SPIN_OBJECT_NAME)
        self.interval_spin.setRange(
            SettingsPanel_Configs.MIN_INTERVAL,
            SettingsPanel_Configs.MAX_INTERVAL,
        )
        self.interval_spin.setValue(SettingsPanel_Configs.DEFAULT_INTERVAL)
        self.interval_spin.setSingleStep(SettingsPanel_Configs.INTERVAL_STEP)
        self.interval_spin.setDecimals(SettingsPanel_Configs.INTERVAL_DECIMALS)
        self.interval_spin.setSuffix(SettingsPanel_Configs.INTERVAL_SUFFIX)

        self.repeat_spin = QSpinBox()
        self.repeat_spin.setObjectName(SettingsPanel_Configs.REPEAT_SPIN_OBJECT_NAME)
        self.repeat_spin.setRange(0, SettingsPanel_Configs.MAX_REPEAT)
        self.repeat_spin.setValue(0)
        self.repeat_spin.setSpecialValueText(SettingsPanel_Configs.REPEAT_SPECIAL_TEXT)

        layout.addRow(SettingsPanel_Configs.INTERVAL_LABEL_TEXT, self.interval_spin)
        layout.addRow(SettingsPanel_Configs.REPEAT_LABEL_TEXT, self.repeat_spin)

        parent.addWidget(self.group)


class PositionSettingsUI:
    def __init__(self, parent: QVBoxLayout, file_manager: FileManager):
        self.group = PyGroupBox(SettingsPanel_Configs.POSITION_GROUP_TITLE)
        self.group.setObjectName(SettingsPanel_Configs.POSITION_GROUP_OBJECT_NAME)
        self.group.setCursor(SettingsPanel_Configs.TOGGLE_BUTTON_CURSOR)        
        layout = QVBoxLayout(self.group)

        top = QHBoxLayout()
        self.pos_label = QLabel(
            SettingsPanel_Configs.POSITION_LABEL_FORMAT.format(
                pos=SettingsPanel_Configs.INITIAL_POSITION
            )
        )
        self.pos_label.setObjectName(SettingsPanel_Configs.POSITION_LABEL_OBJECT_NAME)

        self.overlay_toggle = QPushButton(SettingsPanel_Configs.OVERLAY_SHOW_TEXT)
        self.overlay_toggle.setObjectName(SettingsPanel_Configs.OVERLAY_TOGGLE_OBJECT_NAME)
        self.overlay_toggle.setCheckable(True)

        top.addWidget(self.pos_label)
        top.addWidget(self.overlay_toggle)
        layout.addLayout(top)

        radios = QHBoxLayout()
        self.cursor_radio = QRadioButton(SettingsPanel_Configs.CURSOR_RADIO_TEXT)
        self.cursor_radio.setObjectName(SettingsPanel_Configs.CURSOR_RADIO_OBJECT_NAME)
        self.cursor_radio.setChecked(True)
        
        self.fixed_radio = QRadioButton(SettingsPanel_Configs.FIXED_RADIO_TEXT)
        self.fixed_radio.setObjectName(SettingsPanel_Configs.FIXED_RADIO_OBJECT_NAME)

        radios.addWidget(self.cursor_radio)
        radios.addWidget(self.fixed_radio)
        layout.addLayout(radios)

        form = QFormLayout()
        self.x_spin = QSpinBox()
        self.x_spin.setObjectName(SettingsPanel_Configs.X_SPIN_OBJECT_NAME)
        self.x_spin.setRange(0, SettingsPanel_Configs.MAX_POSITION)
        self.x_spin.setValue(SettingsPanel_Configs.INITIAL_POSITION[0])

        self.y_spin = QSpinBox()
        self.y_spin.setObjectName(SettingsPanel_Configs.Y_SPIN_OBJECT_NAME)
        self.y_spin.setRange(0, SettingsPanel_Configs.MAX_POSITION)
        self.y_spin.setValue(SettingsPanel_Configs.INITIAL_POSITION[1])

        form.addRow(SettingsPanel_Configs.X_LABEL_TEXT, self.x_spin)
        form.addRow(SettingsPanel_Configs.Y_LABEL_TEXT, self.y_spin)
        layout.addLayout(form)

        buttons = QHBoxLayout()
        self.capture_btn = QPushButton(SettingsPanel_Configs.CAPTURE_BUTTON_TEXT)
        self.capture_btn.setObjectName(SettingsPanel_Configs.CAPTURE_BUTTON_OBJECT_NAME)
        capture_shortcut = file_manager.get_keybind("capture_position")
        self.capture_btn.setShortcut(capture_shortcut or QKeySequence())

        self.live_capture_btn = QPushButton(SettingsPanel_Configs.LIVE_CAPTURE_START_TEXT)
        self.live_capture_btn.setObjectName(SettingsPanel_Configs.LIVE_CAPTURE_BUTTON_OBJECT_NAME)
        self.live_capture_btn.setCheckable(True)
        live_shortcut = file_manager.get_keybind("toggle_live_capture")
        self.live_capture_btn.setShortcut(live_shortcut or QKeySequence())

        buttons.addWidget(self.capture_btn)
        buttons.addWidget(self.live_capture_btn)
        layout.addLayout(buttons)

        parent.addWidget(self.group)