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

    # ----------------- Screen Geometry ----------------- 
    def get_combined_screen_geometry(self):
        screens = QGuiApplication.screens()
        if not screens:
            return QGuiApplication.primaryScreen().geometry()
        combined = screens[0].geometry()
        for screen in screens[1:]:
            combined = combined.united(screen.geometry())
        return combined

    # ----------------- Overlay Control ----------------- 
    def set_position(self, x: int, y: int) -> None:
        self.screen_pos = QPoint(x - self.screen_offset_x, y - self.screen_offset_y)
        self.update()

    def show_overlay(self) -> None:
        if not self.visible:
            self.visible = True
            self._refresh_geometry()
            self.show()
            self.raise_()

    def hide_overlay(self) -> None:
        if self.visible:
            self.visible = False
            self.hide()

    def toggle_overlay(self) -> None:
        if self.visible:
            self.hide_overlay()
        else:
            self.show_overlay()

    def _refresh_geometry(self) -> None:
        self.screen_geometry = self.get_combined_screen_geometry()
        self.setGeometry(self.screen_geometry)
        self.screen_offset_x = self.screen_geometry.x()
        self.screen_offset_y = self.screen_geometry.y()

    # ----------------- Paint Event ----------------- 
    def paintEvent(self, event) -> None:
        if not self.visible:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        x, y = self.screen_pos.x(), self.screen_pos.y()
        self._draw_crosshair(painter, x, y)
        self._draw_dot(painter, x, y)
        self._draw_center_dot(painter, x, y)
        self._draw_coordinates(painter, x, y)

    def _draw_crosshair(self, painter: QPainter, x: int, y: int) -> None:
        painter.setPen(QPen(self.crosshair_color, DotOverlay_Configs.CROSSHAIR_THICKNESS))
        length = DotOverlay_Configs.CROSSHAIR_LENGTH
        painter.drawLine(x - length, y, x + length, y)
        painter.drawLine(x, y - length, x, y + length)

    def _draw_dot(self, painter: QPainter, x: int, y: int) -> None:
        painter.setPen(QPen(self.dot_color, DotOverlay_Configs.DOT_THICKNESS))
        painter.setBrush(self.dot_color)
        radius = DotOverlay_Configs.DOT_RADIUS
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def _draw_center_dot(self, painter: QPainter, x: int, y: int) -> None:
        center_color = QColor(255, 255, 255, 200)
        painter.setPen(QPen(center_color, 1))
        painter.setBrush(center_color)
        radius = DotOverlay_Configs.CENTER_RADIUS
        painter.drawEllipse(x - radius, y - radius, radius * 2, radius * 2)

    def _draw_coordinates(self, painter: QPainter, x: int, y: int) -> None:
        screen_x = x + self.screen_offset_x
        screen_y = y + self.screen_offset_y
        label_text = f"({screen_x}, {screen_y})"
        painter.setPen(QPen(self.text_color, 1))
        font = painter.font()
        font.setPointSize(DotOverlay_Configs.TEXT_FONT_SIZE)
        font.setBold(True)
        painter.setFont(font)
        rect = painter.boundingRect(
            x + DotOverlay_Configs.TEXT_OFFSET_X,
            y + DotOverlay_Configs.TEXT_OFFSET_Y,
            100, 20,
            Qt.AlignmentFlag.AlignLeft,
            label_text
        )
        painter.fillRect(rect, self.text_bg_color)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, label_text)