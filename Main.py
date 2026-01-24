from Core.patch.DPI_Patch import PatchedQt
PatchedQt.patch_qt_dpi()

from Core.globals.Base_import import QApplication , sys, pyautogui, QCoreApplication
from Core.MainWindow import PyClicker
from Core.configs.AppVersion import APP_NAME, APP_VERSION


def EntryPoint():

    pyautogui.FAILSAFE = True
    app = QApplication(sys.argv)
    QApplication.setApplicationVersion(APP_VERSION)
    window = PyClicker()
    window.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
    window.show()
    sys.exit(app.exec()) 
    
if __name__ == "__main__":
    EntryPoint() 