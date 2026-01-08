from Core.globals.Base_import import *
from Core.QDialog.QDialog_Base import BaseDialog
from Core.configs.HelpDialog_Configs import  *


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
