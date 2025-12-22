from Core.globals.Base_import import os
# This sets the DPI awareness to prevent DPI warning
# becasue i cant code properly apparently 
class PatchedQt:
    def patch_qt_dpi():
        # --- Tells Qt to use our settings --- 
        os.environ["QT_QPA_PLATFORM"] = "windows:dpiawareness=0"
        os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false"
PatchedQt.patch_qt_dpi()
