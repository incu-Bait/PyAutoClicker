from Core.globals.Base_import import *
from Core.configs.Windows_Configs import WindowConfig, QMW_UIConfig

class WindowManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.app_dir = os.path.dirname(os.path.abspath(sys.argv[0])) # \\ This should fix the issue with not being able to find Asset directory 
                                                                     # just gets the app directory where "Main.py" is. Might run in to some issues with this tho if "Main.py"
        self.main_window.setWindowFlags(self.main_window.windowFlags() & ~Qt.WindowType.WindowMaximizeButtonHint) # \\ Removed Maximize Button                                                       
        self.main_window.setFixedSize(WindowConfig.GEOMETRY[2], WindowConfig.GEOMETRY[3])

    def setup_window(self):
        self.main_window.setWindowTitle(WindowConfig.TITLE)
        self.main_window.setGeometry(*WindowConfig.GEOMETRY)
        self.center_window()
        self.main_window.statusBar().showMessage(QMW_UIConfig.STATUS_READY_MESSAGE)
        self.setup_icon()
        
    def center_window(self):
        window_with_frame = self.main_window.frameGeometry()
        available_screen_center = QGuiApplication.primaryScreen().availableGeometry().center()
        window_with_frame.moveCenter(available_screen_center)
        self.main_window.move(window_with_frame.topLeft())
        
    def setup_icon(self):
        icon_path = os.path.join(self.app_dir, WindowConfig.ICON_PATH)
        icon_path = os.path.normpath(icon_path)
        if os.path.exists(icon_path):
            self.main_window.setWindowIcon(QIcon(icon_path))
        else:
            self.main_window.setWindowIcon(self.main_window.style().standardIcon(QMW_UIConfig.ICON_ALTERNATIVE))