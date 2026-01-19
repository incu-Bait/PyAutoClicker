from Core.globals.Base_import import *
from Core.custom_widgets.QGroupBox.BorderAnimation import Animation
from Core.configs.PyGoupBox_Configs import Configs
from Core.managers.ThemeManager import ThemeManager


class PyGroupBox(QGroupBox, Animation):
    def __init__(self, title: str = "", parent=None):
        super().__init__(title, parent)
        self._init_animated_border()
        self._is_hovered: bool = False
        self._theme_manager: ThemeManager | None = None
        self.setProperty("pygroupbox", True)

    def update_theme(self, theme_manager: ThemeManager | None = None):
        if not theme_manager:
            return
        self._theme_manager = theme_manager
        theme = theme_manager.get_theme()
        self.set_border_color(
            theme.get("border", Configs.BORDER_COLOR)
        )
        self.update()

    def enterEvent(self, event):
        super().enterEvent(event)
        self._is_hovered = True
        self.start_border_animation()

    def leaveEvent(self, event):
        super().leaveEvent(event)
        self._is_hovered = False
        self.stop_border_animation()
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(Configs.RENDER_ANTIALIASING)

        if self._is_hovered and self._border_timer.isActive():
            self._draw_animated_border(painter)
        else:
            self._draw_static_border(painter)

    # ---------------- drawing ---------------- 
    
    def _draw_static_border(self, painter: QPainter):
        pen = self._create_pen()
        painter.setPen(pen)
        painter.setBrush(Configs.BRUSH_STYLE)
        rect = self._border_rect()
        path = self._border_path(rect)
        painter.drawPath(path)

    def _create_pen(self) -> QPen:
        border_color = self.border_color
        if self._theme_manager:
            theme = self._theme_manager.get_theme()
            border_color = QColor(
                theme.get("border", border_color.name())
            )
        pen = QPen(border_color, self.border_width)
        pen.setStyle(Configs.PEN_STYLE_SOLID)
        pen.setCapStyle(Configs.PEN_CAP_STYLE)
        pen.setJoinStyle(Configs.PEN_JOIN_STYLE)
        return pen

    def _border_rect(self) -> QRect:
        inset = self.border_width * Configs.RECTANGLE_INSET
        return QRect(
            inset,
            inset,
            self.width() - inset * 2,
            self.height() - inset * 2
        )
    # NOTE: dont think to much about this 
    def _border_path(self, rect: QRect) -> QPainterPath:
        path = QPainterPath()
        radius = self.corner_radius
        title = self.title()
        title_width = 0
        if title:
            fm = QFontMetrics(self.font())
            title_width = fm.horizontalAdvance(title) + 20
        # --- title gap centered ---
        if title_width > 0:
            gap_start = (rect.width() - title_width) // 2
            gap_end = gap_start + title_width
        else:
            gap_start = gap_end = 0
        # --- top edge wit gap ---
        path.moveTo(rect.left() + radius, rect.top())

        if title_width > 0 and gap_start > radius:
            path.lineTo(rect.left() + gap_start, rect.top())
            path.moveTo(rect.left() + gap_end, rect.top())

        path.lineTo(rect.right() - radius, rect.top())

        # --- corners + sides ---
        path.arcTo(rect.right() - radius * 2, rect.top(),
                   radius * 2, radius * 2, 90, -90)

        path.lineTo(rect.right(), rect.bottom() - radius)

        path.arcTo(rect.right() - radius * 2, rect.bottom() - radius * 2,
                   radius * 2, radius * 2, 0, -90)

        path.lineTo(rect.left() + radius, rect.bottom())

        path.arcTo(rect.left(), rect.bottom() - radius * 2,
                   radius * 2, radius * 2, -90, -90)

        path.lineTo(rect.left(), rect.top() + radius)

        path.arcTo(rect.left(), rect.top(),
                   radius * 2, radius * 2, 180, -90)

        if title_width > 0 and gap_start > radius:
            path.lineTo(rect.left() + gap_start, rect.top())

        return path
