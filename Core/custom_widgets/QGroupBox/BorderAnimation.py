from Core.globals.Base_import import *
from Core.configs.PyGoupBox_Configs import Configs


class Animation:
    def _init_animated_border(self):
        self._dash_offset = Configs.INITIAL_DASH_OFFSET
        self.dash_speed = Configs.INITIAL_DASH_SPEED
        self.border_color = Configs.INITIAL_BORDER_COLOR
        self.border_width = Configs.INITIAL_BORDER_WIDTH
        self.dash_pattern = Configs.INITIAL_DASH_PATTERN.copy()
        self.corner_radius = Configs.INITIAL_CORNER_RADIUS
        self._border_timer = QTimer(self)
        self._border_timer.setTimerType(Configs.TIMER_PRECISION)
        self._border_timer.setSingleShot(Configs.TIMER_SINGLE_SHOT)
        self._border_timer.setObjectName(Configs.BORDER_TIMER_OBJECT_NAME)
        self._border_timer.timeout.connect(self._update_dash_offset)
        self._border_timer.setInterval(Configs.ANIMATION_TIMER_INTERVAL)
        self._animation_enabled = True

    def _update_dash_offset(self):
        if not self._animation_enabled:
            return
        self._dash_offset += self.dash_speed
        if self._dash_offset >= sum(self.dash_pattern):
            self._dash_offset = Configs.INITIAL_DASH_OFFSET
        self.update()

    # ---------------- drawing ----------------

    def _draw_animated_border(self, painter: QPainter):

        if not self._animation_enabled:  # \\ Only draw if animation is enabled
            return
        pen = QPen(self.border_color, self.border_width)
        pen.setStyle(Configs.PEN_STYLE_CUSTOM)
        pen.setDashPattern(self.dash_pattern)
        pen.setDashOffset(-self._dash_offset)
        pen.setCapStyle(Configs.PEN_CAP_STYLE)
        pen.setJoinStyle(Configs.PEN_JOIN_STYLE)
        painter.setPen(pen)
        painter.setBrush(Configs.BRUSH_STYLE)
        fm = QFontMetrics(self.font())
        title_height = fm.height()
        top_offset = title_height + Configs.EXTRA_SPACING
        rect = QRect(
            self.border_width * Configs.RECTANGLE_INSET,
            top_offset,
            self.width() - self.border_width * Configs.RECTANGLE_INSET * 2,
            self.height() - top_offset - self.border_width * Configs.RECTANGLE_INSET
        )
        painter.drawRoundedRect(rect, self.corner_radius, self.corner_radius)
    
    # ===================================
    # Methods i can use for the frame 
    # to change color, cycle through set colors 
    # and if i want i can add more effects here
    # shouldnt really need to leave this file
    # if i end up making more depending on 
    # what they are. KEEP IT SIMPLE.
    # ----------------------------------- 
    # Example --> .setProperty("dashed", True)
    # Example --> .set_preset_pattern("dotted") 
    # Example --> .set_dash_pattern([1, 3])  
    # Example --> .set_preset_color("yellow") 
    # Example --> .set_animation_speed(2.0)  
    # Example --> .set_color_cycle (#Color1 , #Color2, #Color3)interval) # \\ Hex Format 
    # ===================================
    def set_color_cycle(self, colors: list, interval: int = 1000, enabled: bool = True):
        self._color_cycle = colors
        self._color_cycle_enabled = enabled
        self._current_color_index = 0
        
        if enabled and colors:
            self._color_timer = QTimer(self)
            self._color_timer.timeout.connect(self._next_color)
            self._color_timer.start(interval)

    def _next_color(self):
        if not self._color_cycle_enabled or not self._color_cycle:
            return
        
        self._current_color_index = (self._current_color_index + 1) % len(self._color_cycle)
        self.set_border_color(self._color_cycle[self._current_color_index])
        
    def set_border_color(self, color):
        if isinstance(color, str):
            try:
                self.border_color = QColor(color)
            except:
                print(f"{Configs.ERROR_INVALID_COLOR}: {color}")
                self.border_color = Configs.INITIAL_BORDER_COLOR
        elif isinstance(color, QColor):
            self.border_color = color
        else:
            print(f"{Configs.ERROR_INVALID_COLOR}: {color}")
            self.border_color = Configs.INITIAL_BORDER_COLOR
            
        self.update()

    def set_animation_speed(self, speed: float):
        if Configs.MIN_DASH_SPEED <= speed <= Configs.MAX_DASH_SPEED:
            self.dash_speed = speed
        else:
            error_msg = Configs.ERROR_INVALID_SPEED.format(
                min=Configs.MIN_DASH_SPEED,
                max=Configs.MAX_DASH_SPEED
            )
            print(error_msg)

    def set_dash_pattern(self, pattern: list):
        if isinstance(pattern, list) and all(isinstance(x, (int, float)) and x > 0 for x in pattern):
            self.dash_pattern = pattern.copy()
            self.update()
        else:
            print(Configs.ERROR_INVALID_PATTERN)

    def set_border_width(self, width: int):
        if Configs.BORDER_WIDTH_MIN <= width <= Configs.BORDER_WIDTH_MAX:
            self.border_width = width
            self.update()

    def set_corner_radius(self, radius: int):
        if Configs.CORNER_RADIUS_MIN <= radius <= Configs.CORNER_RADIUS_MAX:
            self.corner_radius = radius
            self.update()

    def set_preset_color(self, preset_name: str):
        if preset_name in Configs.COLOR_PRESETS:
            self.set_border_color(Configs.COLOR_PRESETS[preset_name])

    def set_preset_pattern(self, pattern_name: str):
        if pattern_name in Configs.ANIMATION_PATTERNS:
            self.set_dash_pattern(Configs.ANIMATION_PATTERNS[pattern_name])

    def start_border_animation(self):
        if not self._border_timer.isActive():
            self._border_timer.start()
            self._animation_enabled = True

    def stop_border_animation(self):
        if self._border_timer.isActive():
            self._border_timer.stop()
        self.update()  

    def pause_border_animation(self):
        self._border_timer.stop()

    def resume_border_animation(self):
        if self._animation_enabled and not self._border_timer.isActive():
            self._border_timer.start()

    def set_animation_enabled(self, enabled: bool):
        self._animation_enabled = enabled
        if enabled:
            self.start_border_animation()
        else:
            self.stop_border_animation()

    def get_animation_state(self):
        if self._border_timer.isActive():
            return Configs.ANIMATION_STATE_RUNNING
        return Configs.ANIMATION_STATE_STOPPED

    def is_animation_enabled(self):
        return self._animation_enabled 