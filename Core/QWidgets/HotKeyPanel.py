from Core.globals.Base_import import *
from Core.configs.HockeyPanel_Config import *
from Core.CustomWidgets.QGroupBox.PyGroupBox import PyGroupBox


class HotkeyPanel(QWidget):
    hotkey_changed = pyqtSignal(str)
    def __init__(self, default_hotkey: str = None):
        super().__init__()
        
        if default_hotkey is None:
            default_hotkey = HotkeyPanelConfig.DEFAULT_HOTKEY

        layout = QVBoxLayout(self)

        self.group = PyGroupBox(HotkeyPanelConfig.GROUP_BOX_TITLE)
        self.group.setObjectName(HotkeyPanelConfig.GROUP_BOX_OBJECT_NAME)
        self.group.setCursor(HotkeyPanelConfig.TOGGLE_BUTTON_CURSOR)
        group_layout = QVBoxLayout(self.group)

        # --- Current hotkey ---
        top = QHBoxLayout()
        self.current_label = QLabel(
            HotkeyPanelConfig.CURRENT_HOTKEY_LABEL_FORMAT.format(
                hotkey=default_hotkey.upper()
            )
        )
        self.current_label.setObjectName(HotkeyPanelConfig.CURRENT_LABEL_OBJECT_NAME)
        self.current_label.setSizePolicy(
            HotkeyPanelConfig.CURRENT_LABEL_SIZE_POLICY_H,
            HotkeyPanelConfig.CURRENT_LABEL_SIZE_POLICY_V,
        )
        top.addWidget(self.current_label)
        top.addStretch()
        group_layout.addLayout(top)

        # --- Hotkey input ---
        form = QFormLayout()
        self.hotkey_edit = QLineEdit(default_hotkey)
        self.hotkey_edit.setObjectName(HotkeyPanelConfig.HOTKEY_EDIT_OBJECT_NAME)
        form.addRow(HotkeyPanelConfig.FORM_LABEL_TEXT, self.hotkey_edit)
        group_layout.addLayout(form)

        # --- Apply button ---
        buttons = QHBoxLayout()
        buttons.addStretch()
        self.apply_btn = QPushButton(HotkeyPanelConfig.APPLY_BUTTON_TEXT)
        self.apply_btn.setObjectName(HotkeyPanelConfig.APPLY_BUTTON_OBJECT_NAME)
        self.apply_btn.clicked.connect(self.apply_hotkey)
        buttons.addWidget(self.apply_btn)
        buttons.addStretch()
        group_layout.addLayout(buttons)

        layout.addWidget(self.group)
        layout.addStretch()
        
        self.setMinimumWidth(HotkeyPanelConfig.MIN_WIDTH)
        self.setMinimumHeight(HotkeyPanelConfig.MIN_HEIGHT)

    def apply_hotkey(self):
        hotkey = self.hotkey_edit.text().strip().lower()
        if hotkey:
            self.current_label.setText(
                HotkeyPanelConfig.CURRENT_HOTKEY_LABEL_FORMAT.format(
                    hotkey=hotkey.upper()
                )
            )
            self.hotkey_changed.emit(hotkey)