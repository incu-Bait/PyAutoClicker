from Core.globals.Base_import import *
from Core.managers.ThemeManager import * 
from Core.configs.Theme_Configs import *
from Core.configs.Windows_Configs import *
from Core.MainWindow import PyClicker

def EntryPoint():

    pyautogui.FAILSAFE = True
    app = QApplication(sys.argv)
    window = PyClicker()
    window.show()
    sys.exit(app.exec()) 
    
if __name__ == "__main__":
    EntryPoint() 