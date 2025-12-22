from Core.globals.Base_import import *
from Core.configs.DotOverlay_Configs import DotOverlay_Configs

class ScreenDotOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.screen_pos = DotOverlay_Configs.INITIAL_POSITION
        self.visible = False
        self.dot_color = DotOverlay_Configs.DOT_COLOR
        self.crosshair_color = DotOverlay_Configs.CROSSHAIR_COLOR
        self.text_color = DotOverlay_Configs.TEXT_COLOR
        self.text_bg_color = DotOverlay_Configs.TEXT_BG_COLOR
        self.setWindowFlags(DotOverlay_Configs.WINDOW_FLAGS)
        
        for attr in DotOverlay_Configs.WIDGET_ATTRIBUTES:
            self.setAttribute(attr)
        
        self.screen_geometry = self.get_combined_screen_geometry()
        self.setGeometry(self.screen_geometry)
        self.screen_offset_x = self.screen_geometry.x()
        self.screen_offset_y = self.screen_geometry.y()
        
    def get_combined_screen_geometry(self):
        screens = QGuiApplication.screens()
        combined = screens[0].geometry() if screens else QGuiApplication.primaryScreen().geometry()
        
        for screen in screens[1:]:
            combined = combined.united(screen.geometry())
        
        return combined
        
    def set_position(self, x, y):
        adjusted_x = x - self.screen_offset_x
        adjusted_y = y - self.screen_offset_y
        self.screen_pos = QPoint(adjusted_x, adjusted_y)
        self.update()
        
    def show_overlay(self):
        if not self.visible:
            self.visible = True
            self.screen_geometry = self.get_combined_screen_geometry()
            self.setGeometry(self.screen_geometry)
            self.screen_offset_x = self.screen_geometry.x()
            self.screen_offset_y = self.screen_geometry.y()
            self.show()
            self.raise_()
            
    def hide_overlay(self):
        if self.visible:
            self.visible = False
            self.hide()
            
    def toggle_overlay(self):
        if self.visible:
            self.hide_overlay()
        else:
            self.show_overlay()
            
    def update_theme_colors(self, accent_color):
        if accent_color.startswith('#'):
            color = QColor(accent_color)
            self.dot_color = color
            self.dot_color.setAlpha(220)
            self.crosshair_color = color
            self.crosshair_color.setAlpha(100)
        
    def paintEvent(self, event):
        if not self.visible:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        widget_x = self.screen_pos.x()
        widget_y = self.screen_pos.y()
        # ---- crosshair ----
        painter.setPen(QPen(self.crosshair_color, DotOverlay_Configs.CROSSHAIR_THICKNESS))
        painter.drawLine(
            widget_x - DotOverlay_Configs.CROSSHAIR_LENGTH, 
            widget_y, 
            widget_x + DotOverlay_Configs.CROSSHAIR_LENGTH, 
            widget_y
        )
        painter.drawLine(
            widget_x, 
            widget_y - DotOverlay_Configs.CROSSHAIR_LENGTH,
            widget_x, 
            widget_y + DotOverlay_Configs.CROSSHAIR_LENGTH
        )
        # ---- outer dot ----
        painter.setPen(QPen(self.dot_color, DotOverlay_Configs.DOT_THICKNESS))
        painter.setBrush(self.dot_color)
        painter.drawEllipse(
            widget_x - DotOverlay_Configs.DOT_RADIUS,
            widget_y - DotOverlay_Configs.DOT_RADIUS,
            DotOverlay_Configs.DOT_RADIUS * 2,
            DotOverlay_Configs.DOT_RADIUS * 2
        )
        # ---- center dot ----
        center_color = QColor(255, 255, 255, 200)
        painter.setPen(QPen(center_color, 1))
        painter.setBrush(center_color)
        painter.drawEllipse(
            widget_x - DotOverlay_Configs.CENTER_RADIUS,
            widget_y - DotOverlay_Configs.CENTER_RADIUS,
            DotOverlay_Configs.CENTER_RADIUS * 2,
            DotOverlay_Configs.CENTER_RADIUS * 2
        )
        # ---- coordinate text ----
        screen_x = widget_x + self.screen_offset_x
        screen_y = widget_y + self.screen_offset_y
        label_text = f"({screen_x}, {screen_y})"
        painter.setPen(QPen(self.text_color, 1))
        font = painter.font()
        font.setPointSize(DotOverlay_Configs.TEXT_FONT_SIZE)
        font.setBold(True)
        painter.setFont(font)
        text_rect = painter.boundingRect(
            widget_x + DotOverlay_Configs.TEXT_OFFSET_X,
            widget_y + DotOverlay_Configs.TEXT_OFFSET_Y,
            100, 20,
            Qt.AlignmentFlag.AlignLeft,
            label_text
        )
        painter.fillRect(text_rect, self.text_bg_color)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, label_text)