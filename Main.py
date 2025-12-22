from Core.patch.DPI_Patch import PatchedQt
PatchedQt.patch_qt_dpi()

from Core.globals.Base_import import QApplication , sys, pyautogui, os
from Core.MainWindow import PyClicker

def EntryPoint():

    pyautogui.FAILSAFE = True
    app = QApplication(sys.argv)
    window = PyClicker()
    window.show()
    sys.exit(app.exec()) 
    
if __name__ == "__main__":
    EntryPoint() 