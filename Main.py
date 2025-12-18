from Core.globals.Base_import import QApplication , sys, pyautogui
from Core.MainWindow import PyClicker

def EntryPoint():

    pyautogui.FAILSAFE = True
    app = QApplication(sys.argv)
    window = PyClicker()
    window.show()
    sys.exit(app.exec()) 
    
if __name__ == "__main__":
    EntryPoint() 