from Core.globals.Base_import import *
from Core.configs.Windows_Configs import PyClickerConstants, WindowConfig

class WindowManager:
    def __init__(self, main_window):
        self.main_window = main_window
        
    def setup_window(self):
        self.main_window.setWindowTitle(WindowConfig.TITLE)
        self.main_window.setGeometry(*WindowConfig.GEOMETRY)
        self.main_window.statusBar().showMessage(PyClickerConstants.STATUS_READY_MESSAGE)
        self.setup_icon()
        
    def setup_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "..", WindowConfig.ICON_PATH)
        icon_path = os.path.normpath(icon_path)
        if os.path.exists(icon_path):
            self.main_window.setWindowIcon(QIcon(icon_path))
        else:
            self.main_window.setWindowIcon(self.main_window.style().standardIcon(PyClickerConstants.ICON_ALTERNATIVE))

