from Core.globals.Base_import import *
from Core.configs.HelpDialog_Configs import  *


class BaseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setModal(True)


class AboutDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(DialogConstants.ABOUT_TITLE)
        layout = QVBoxLayout(self)
        label = QLabel(DialogConstants.ABOUT_TEXT)
        label.setTextFormat(Qt.TextFormat.RichText)
        label.setWordWrap(True)
        layout.addWidget(label)
        
        close_btn = QPushButton(DialogConstants.CLOSE_BUTTON_TEXT)
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class ShortcutsDialog(BaseDialog):
    def __init__(self, keybind_manager, parent=None):
        super().__init__(parent)
        self.keybind_manager = keybind_manager
        self.setWindowTitle(DialogConstants.SHORTCUTS_TITLE)
        self.setMinimumWidth(DialogConstants.SHORTCUTS_MIN_WIDTH)
        self.setMinimumHeight(DialogConstants.SHORTCUTS_MIN_HEIGHT)
        layout = QVBoxLayout(self)
        
        header_layout = QHBoxLayout()
        header_label = QLabel(DialogConstants.SHORTCUTS_HEADER_TEXT)
        header_layout.addWidget(header_label)
        header_layout.addStretch()
        
        self.edit_toggle = QPushButton(DialogConstants.EDIT_TOGGLE_DISABLED_TEXT)
        self.edit_toggle.setCheckable(True)
        self.edit_toggle.clicked.connect(self.toggle_editing)
        header_layout.addWidget(self.edit_toggle)
        layout.addLayout(header_layout)
        
        self.keybinds = self.keybind_manager.get_all_keybinds()
        self.table = QTableWidget(len(self.keybinds), 3)
        self.table.setHorizontalHeaderLabels(DialogConstants.TABLE_HEADERS)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        
        for row, (action, desc, shortcut) in enumerate(self.keybinds):
            desc_item = QTableWidgetItem(desc)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 0, desc_item)

            shortcut_item = QTableWidgetItem(shortcut if shortcut else DialogConstants.NOT_SET_TEXT)
            shortcut_item.setFlags(shortcut_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            shortcut_item.setData(Qt.ItemDataRole.UserRole, action) 
            self.table.setItem(row, 1, shortcut_item)
            
            action_item = QTableWidgetItem(action)
            action_item.setFlags(action_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.table.setItem(row, 2, action_item)

        self.table.setColumnHidden(2, True)
        
        self.table.cellDoubleClicked.connect(self.edit_shortcut_cell)
        layout.addWidget(self.table)
        
        button_layout = QHBoxLayout()
        
        self.reset_btn = QPushButton(DialogConstants.RESET_BUTTON_TEXT)
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_btn)
        
        button_layout.addStretch()
        
        self.save_btn = QPushButton(DialogConstants.SAVE_BUTTON_TEXT)
        self.save_btn.clicked.connect(self.save_changes)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        close_btn = QPushButton(DialogConstants.CLOSE_BUTTON_TEXT)
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.changes_made = False
        self.editing_enabled = False
        
    def toggle_editing(self):
        self.editing_enabled = self.edit_toggle.isChecked()
        if self.editing_enabled:
            self.edit_toggle.setText(DialogConstants.EDIT_TOGGLE_ENABLED_TEXT)
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 1)
                if item:
                    item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
        else:
            self.edit_toggle.setText(DialogConstants.EDIT_TOGGLE_DISABLED_TEXT)
            self.edit_toggle.setStyleSheet("")
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 1)
                if item:
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    
    def edit_shortcut_cell(self, row, column):
        if column == 1 and self.editing_enabled: 
            item = self.table.item(row, 1)
            if item:
                current_shortcut = item.text() if item.text() != DialogConstants.NOT_SET_TEXT else ""
                action_desc = self.table.item(row, 0).text()
                new_shortcut, ok = QInputDialog.getText(
                    self,
                    DialogConstants.EDIT_SHORTCUT_TITLE,
                    DialogConstants.EDIT_SHORTCUT_PROMPT.format(action_desc=action_desc),
                    QLineEdit.EchoMode.Normal,
                    current_shortcut
                )
                if ok:
                    new_shortcut = new_shortcut.strip()
                    if new_shortcut:
                        item.setText(new_shortcut)
                        self.changes_made = True
                        self.save_btn.setEnabled(True)
                    else:
                        item.setText(DialogConstants.NOT_SET_TEXT)
                        self.changes_made = True
                        self.save_btn.setEnabled(True)
    
    def reset_to_defaults(self):
        reply = QMessageBox.question(
            self, 
            DialogConstants.RESET_CONFIRM_TITLE,
            DialogConstants.RESET_CONFIRM_TEXT,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            default_keybinds = self.keybind_manager.get_default_keybinds()
            
            for row in range(self.table.rowCount()):
                action_item = self.table.item(row, 2)
                if action_item:
                    action = action_item.text()
                    default_shortcut = default_keybinds.get(action, "")
                    
                    shortcut_item = self.table.item(row, 1)
                    if shortcut_item:
                        shortcut_item.setText(default_shortcut if default_shortcut else DialogConstants.NOT_SET_TEXT)
            
            self.changes_made = True
            self.save_btn.setEnabled(True)
    
    def save_changes(self):
        updated_keybinds = {}
        for row in range(self.table.rowCount()):
            action_item = self.table.item(row, 2)
            shortcut_item = self.table.item(row, 1)
            
            if action_item and shortcut_item:
                action = action_item.text()
                shortcut = shortcut_item.text().strip()
                if shortcut == DialogConstants.NOT_SET_TEXT:
                    shortcut = ""
                updated_keybinds[action] = shortcut
        try:
            self.keybind_manager.keybinds.update(updated_keybinds)
            self.keybind_manager.save_keybinds_to_file(self.keybind_manager.keybinds)
            if hasattr(self.parent(), 'update_keybind_shortcuts'):
                self.parent().update_keybind_shortcuts()
            QMessageBox.information(
                self,
                DialogConstants.SAVE_SUCCESS_TITLE,
                DialogConstants.SAVE_SUCCESS_TEXT
            )
            self.changes_made = False
            self.save_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(
                self,
                DialogConstants.SAVE_ERROR_TITLE,
                DialogConstants.SAVE_ERROR_TEXT.format(error=str(e))
            )

    def closeEvent(self, event):
        if self.changes_made:
            reply = QMessageBox.question(
                self,
                DialogConstants.UNSAVED_CHANGES_TITLE,
                DialogConstants.UNSAVED_CHANGES_TEXT,
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No |
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_changes()
                event.accept()
            elif reply == QMessageBox.StandardButton.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()