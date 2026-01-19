from Core.globals.Base_import import *


class PyLineEdit(QLineEdit):
    KEY_NAMES = {}
    KEY_NAMES.update({Qt.Key.Key_F1 + i - 1: f"F{i}" for i in range(1, 13)})  # \\ F-keys (F1-F12)
    KEY_NAMES.update({Qt.Key.Key_0 + i: str(i) for i in range(10)})  # \\ Number keys (0-9)
    KEY_NAMES.update({Qt.Key.Key_A + i: chr(ord('A') + i) for i in range(26)})  # \\ Letter keys (A-Z)
    KEY_NAMES.update({
        # -- Navigation --
        Qt.Key.Key_Up: "Up",
        Qt.Key.Key_Down: "Down",
        Qt.Key.Key_Left: "Left",
        Qt.Key.Key_Right: "Right",
        Qt.Key.Key_Home: "Home",
        Qt.Key.Key_End: "End",
        Qt.Key.Key_PageUp: "PageUp",
        Qt.Key.Key_PageDown: "PageDown",
        # -- Editing --
        Qt.Key.Key_Backspace: "Backspace",
        Qt.Key.Key_Delete: "Delete",
        Qt.Key.Key_Insert: "Insert",
        Qt.Key.Key_Tab: "Tab",
        Qt.Key.Key_Return: "Enter",
        Qt.Key.Key_Space: "Space",
        # -- Locks --
        Qt.Key.Key_CapsLock: "CapsLock",
        Qt.Key.Key_NumLock: "NumLock",
        Qt.Key.Key_ScrollLock: "ScrollLock",
        # -- System --
        Qt.Key.Key_Escape: "Escape",
        Qt.Key.Key_Print: "PrintScreen",
        Qt.Key.Key_Pause: "Pause",
    })

    MODIFIER_KEYS = frozenset({
        Qt.Key.Key_Control,
        Qt.Key.Key_Alt,
        Qt.Key.Key_Shift,
        Qt.Key.Key_Meta,
        Qt.Key.Key_AltGr,
    })
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.is_listening = False
        self.setReadOnly(True)
        self.installEventFilter(self)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_listening()
        super().mousePressEvent(event)
        
    def start_listening(self):
        self.is_listening = True
        self.setText("Press Any Key...")

    def stop_listening(self):
        self.is_listening = False
        self.setStyleSheet("")
        
    def eventFilter(self, obj, event):
        if obj == self and self.is_listening and event.type() == QEvent.Type.KeyPress:
            self.handle_key_press(event)
            return True
        return super().eventFilter(obj, event)
        
    def handle_key_press(self, event):
        key = event.key()
        if key in self.MODIFIER_KEYS:
            return
        if key == Qt.Key.Key_Escape:
            self.setText("")
            self.stop_listening()
            return
        key_name = self.KEY_NAMES.get(key)
        
        # --- Fallback ---
        if not key_name:
            key_text = event.text()
            if key_text and key_text.isprintable():
                key_name = key_text.upper()
            else:
                self.setText("Unsupported key")
                self.stop_listening()
                return
        # -----------------

        modifiers = event.modifiers()
        parts = []
        if modifiers & Qt.KeyboardModifier.ControlModifier:
            parts.append("Ctrl")
        if modifiers & Qt.KeyboardModifier.AltModifier:
            parts.append("Alt")
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            parts.append("Shift")
        parts.append(key_name)
        self.setText("+".join(parts))
        self.stop_listening()
        
    def focusOutEvent(self, event):
        if self.is_listening:
            self.stop_listening()
            if self.text() == "Press Any Key...":
                self.setText("")
        super().focusOutEvent(event)