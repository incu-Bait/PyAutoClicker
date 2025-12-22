from Core.globals.Base_import import *

class HotkeyPanel(QWidget):
    hotkey_changed = pyqtSignal(str)    
    def __init__(self, default_hotkey="f6"):
        super().__init__()
        self.hotkey = default_hotkey
        layout = QVBoxLayout(self)
        group_box = QGroupBox("Hotkey Settings")
        group_box_layout = QVBoxLayout()
        # ---- Current hotkey display ----
        self.current_label = QLabel(f"Current Hotkey: {self.hotkey.upper()}")
        group_box_layout.addWidget(self.current_label)
        # ---- Hotkey input ----
        form = QFormLayout()
        self.hotkey_edit = QLineEdit(self.hotkey)
        form.addRow("Set Hotkey:", self.hotkey_edit)
        group_box_layout.addLayout(form)
        # ---- Apply button ----
        self.apply_btn = QPushButton("Apply Hotkey")
        self.apply_btn.clicked.connect(self.apply_hotkey)
        group_box_layout.addWidget(self.apply_btn)
        
        group_box_layout.addStretch()
        group_box.setLayout(group_box_layout)
        layout.addWidget(group_box)

    def apply_hotkey(self):
        new_hotkey = self.hotkey_edit.text().strip().lower()
        if new_hotkey:
            self.hotkey_changed.emit(new_hotkey)