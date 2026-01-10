from Core.globals.Base_import import *
from Core.configs.ControlPanel_Configs import ControlPanel_Config


class ControlPanel(QWidget):    
    def __init__(self, main_window, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.main_window = main_window
        self._is_running: bool = False
        self._count: int = 0
        self.status_icon: Optional[QLabel] = None
        self.status_label: Optional[QLabel] = None
        self.count_label: Optional[QLabel] = None
        self.toggle_button: Optional[QPushButton] = None
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(ControlPanel_Config.CONTROL_PANEL_SPACING)
        main_layout.setContentsMargins(ControlPanel_Config.get_margins())
        main_layout.addLayout(self._create_status_section())
        main_layout.addSpacing(ControlPanel_Config.SEPARATOR_SPACING)
        main_layout.addWidget(self._create_separator())
        main_layout.addSpacing(ControlPanel_Config.SEPARATOR_SPACING)
        main_layout.addWidget(self._create_toggle_section())

        if ControlPanel_Config.CONTROL_PANEL_HAS_STRETCH:
            main_layout.addStretch()
        
        self.update_ui(False)
        
    def _create_status_section(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(ControlPanel_Config.STATUS_LAYOUT_SPACING)

        self.status_icon = self._create_status_icon()
        self.status_label = QLabel(ControlPanel_Config.COUNT_DEFAULT_TEXT)
        self.status_label.setObjectName(ControlPanel_Config.STATUS_LABEL_OBJECT_NAME)
        self.count_label = QLabel(ControlPanel_Config.COUNT_DEFAULT_TEXT)
        self.count_label.setObjectName(ControlPanel_Config.COUNT_LABEL_OBJECT_NAME)
        
        layout.addWidget(self.status_icon)
        layout.addWidget(self.status_label)
        layout.addSpacing(ControlPanel_Config.STATUS_LAYOUT_SPACING)
        layout.addWidget(self.count_label)
        
        if ControlPanel_Config.STATUS_SECTION_HAS_STRETCH:
            layout.addStretch()
        
        return layout
    
    def _create_status_icon(self) -> QLabel:
        icon = QLabel()
        icon.setObjectName(ControlPanel_Config.STATUS_ICON_OBJECT_NAME)
        icon.setFixedSize(
            ControlPanel_Config.STATUS_ICON_SIZE,
            ControlPanel_Config.STATUS_ICON_SIZE
        )
        icon.setAlignment(ControlPanel_Config.ICON_ALIGNMENT)
        return icon
        
    def _create_separator(self) -> QFrame:
        separator = QFrame()
        separator.setFrameShape(getattr(QFrame.Shape, ControlPanel_Config.SEPARATOR_FRAME_SHAPE))
        separator.setFrameShadow(getattr(QFrame.Shadow, ControlPanel_Config.SEPARATOR_FRAME_SHADOW))
        separator.setObjectName(ControlPanel_Config.SEPARATOR_OBJECT_NAME)
        return separator
    
    def _create_toggle_section(self) -> QPushButton:
        self.toggle_button = QPushButton()
        self.toggle_button.setObjectName(ControlPanel_Config.TOGGLE_BUTTON_OBJECT_NAME)
        self.toggle_button.setMinimumHeight(ControlPanel_Config.TOGGLE_BUTTON_MIN_HEIGHT)
        self.toggle_button.setCursor(ControlPanel_Config.TOGGLE_BUTTON_CURSOR)
        self._update_toggle_button_text(False)
        return self.toggle_button
    
    def _update_toggle_button_text(self, running: bool) -> None:
        hotkey = self.main_window.hotkey.upper()
        if running:
            text = ControlPanel_Config.TOGGLE_STOP_TEXT_FORMAT.format(hotkey=hotkey)
        else:
            text = ControlPanel_Config.TOGGLE_START_TEXT_FORMAT.format(hotkey=hotkey)
        self.toggle_button.setText(text)
    
    def _update_status_icon_and_label(self, running: bool) -> None:
        if running:
            icon_type = ControlPanel_Config.get_icon_constant(ControlPanel_Config.PLAY_ICON)
            status_text = ControlPanel_Config.STATUS_RUNNING_TEXT
        else:
            icon_type = ControlPanel_Config.get_icon_constant(ControlPanel_Config.STOP_ICON)
            status_text = ControlPanel_Config.STATUS_STOPPED_TEXT
        
        icon = self.main_window.style().standardIcon(icon_type)
        pixmap = icon.pixmap(
            ControlPanel_Config.STATUS_ICON_SIZE_RENDER,
            ControlPanel_Config.STATUS_ICON_SIZE_RENDER
        )
        self.status_icon.setPixmap(pixmap)
        self.status_label.setText(status_text)
    
    def update_ui(self, running: bool) -> None:
        self._is_running = running
        self._update_toggle_button_text(running)
        self._update_status_icon_and_label(running)
        
    def update_status_ui(self, running: bool) -> None:
        self._is_running = running
        self._update_status_icon_and_label(running)
        
    def update_count_ui(self, count: int) -> None:
        self._count = count
        self.count_label.setText(ControlPanel_Config.COUNT_LABEL_FORMAT.format(count=count))
        
    def update_hotkey_ui(self, hotkey: str) -> None:
        self.main_window.hotkey = hotkey
        self._update_toggle_button_text(self._is_running)
    
    @property
    def is_running(self) -> bool:
        return self._is_running
    
    @property
    def current_count(self) -> int:
        return self._count