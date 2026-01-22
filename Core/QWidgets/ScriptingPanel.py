from Core.globals.Base_import import *
from Core.configs.ScriptPanel_Configs import ScriptPanelConfig
from Core.custom_widgets.QPlainTextEdit.PyScriptEditor import ScriptEditor
from Core.custom_widgets.QSyntaxHighlighter.PyScriptHighlighter import PyScriptHighlighter
from Core.managers.FileManager import FileManager


class ScriptPanel(QWidget):
    script_started = pyqtSignal()
    script_stopped = pyqtSignal()
    
    def __init__(self, script_engine, file_manager: FileManager = None):
        super().__init__()
        self.script_engine = script_engine
        self.cfg = ScriptPanelConfig()
        self.file_manager = file_manager or FileManager()
        self.current_script_file = None
        self._setup_ui()
        self._connect_signals()
        self._load_example_script()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.cfg.LAYOUT_MARGINS)
        layout.setSpacing(self.cfg.LAYOUT_SPACING)
        self.setObjectName(self.cfg.SCRIPT_PANEL_OBJECT_NAME)
        
        header = QHBoxLayout()
        
        self.help_btn = QPushButton("Open Manual")
        self.help_btn.setFixedSize(150, 30)  
        self.help_btn.setObjectName("help_button")
        self.help_btn.setToolTip("Open Scripting Manual")
        self.help_btn.setCursor(self.cfg.HAND_CURSOR)
        header.addWidget(self.help_btn)
        
        self.run_btn = QPushButton(self.cfg.RUN_BUTTON_TEXT)
        self.stop_btn = QPushButton(self.cfg.STOP_BUTTON_TEXT)
        self.run_btn.setMinimumHeight(self.cfg.BUTTON_MIN_HEIGHT)
        self.stop_btn.setMinimumHeight(self.cfg.BUTTON_MIN_HEIGHT)
        self.stop_btn.setEnabled(False)
        self.run_btn.setObjectName(self.cfg.RUN_BUTTON_OBJECT_NAME)
        self.stop_btn.setObjectName(self.cfg.STOP_BUTTON_OBJECT_NAME)
        self.run_btn.setCursor(self.cfg.HAND_CURSOR)
        self.stop_btn.setCursor(self.cfg.HAND_CURSOR)
        
        header.addStretch()
        header.addWidget(self.run_btn)
        header.addWidget(self.stop_btn)
        layout.addLayout(header)
        
        editor_label = QLabel(self.cfg.EDITOR_LABEL_TEXT)
        editor_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(editor_label)
        
        self.script_editor = ScriptEditor(config=self.cfg)
        self.script_editor.setFont(QFont(
            self.cfg.EDITOR_FONT_FAMILY, 
            self.cfg.EDITOR_FONT_SIZE
        ))
        self.script_editor.setPlaceholderText(self.cfg.EDITOR_PLACEHOLDER_TEXT)
        self.script_editor.setMinimumHeight(self.cfg.EDITOR_MIN_HEIGHT)
        self._setup_syntax_highlighter()
        
        layout.addWidget(self.script_editor, stretch=3)
        
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(self.cfg.BUTTON_SPACING)
        self.clear_btn = QPushButton(self.cfg.CLEAR_BUTTON_TEXT)
        self.example_btn = QPushButton(self.cfg.EXAMPLE_BUTTON_TEXT)
        self.save_btn = QPushButton(self.cfg.SAVE_BUTTON_TEXT)
        self.load_btn = QPushButton(self.cfg.LOAD_BUTTON_TEXT)
        buttons = [
            (self.clear_btn, self.cfg.CLEAR_BUTTON_OBJECT_NAME),
            (self.example_btn, self.cfg.EXAMPLE_BUTTON_OBJECT_NAME),
            (self.save_btn, self.cfg.SAVE_BUTTON_OBJECT_NAME),
            (self.load_btn, self.cfg.LOAD_BUTTON_OBJECT_NAME)
        ]
        
        for btn, obj_name in buttons:
            btn_layout.addWidget(btn)
            btn.setObjectName(obj_name)
        
        layout.addLayout(btn_layout)
        
        output_label = QLabel(self.cfg.OUTPUT_LABEL_TEXT)
        output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        layout.addWidget(output_label)

        self.output_console = QTextEdit()
        self.output_console.setReadOnly(True)
        self.output_console.setFont(QFont(
            self.cfg.CONSOLE_FONT_FAMILY, 
            self.cfg.CONSOLE_FONT_SIZE
        ))
        self.output_console.setMinimumHeight(self.cfg.CONSOLE_MIN_HEIGHT)
        self.output_console.setObjectName(self.cfg.OUTPUT_CONSOLE_OBJECT_NAME)
        layout.addWidget(self.output_console, stretch=2)
    
    def _setup_syntax_highlighter(self):
        self.highlighter = PyScriptHighlighter(self.script_editor.document(), self.cfg)
    
    def _connect_signals(self):
        self.run_btn.clicked.connect(self._on_run_clicked)
        self.stop_btn.clicked.connect(self._on_stop_clicked)
        self.clear_btn.clicked.connect(self.script_editor.clear)
        self.example_btn.clicked.connect(self._load_example_script)
        self.save_btn.clicked.connect(self._save_script)
        self.load_btn.clicked.connect(self._load_script)
        self.help_btn.clicked.connect(self._open_manual)

        if hasattr(self.script_engine, 'log_signal'):
            self.script_engine.log_signal.connect(self._append_output)
        if hasattr(self.script_engine, 'error_signal'):
            self.script_engine.error_signal.connect(self._append_error)
        if hasattr(self.script_engine, 'finished_signal'):
            self.script_engine.finished_signal.connect(self._on_script_finished)
    
    def _on_run_clicked(self):
        script = self.script_editor.toPlainText()
        if not script.strip():
            self._append_error(self.cfg.EMPTY_SCRIPT_ERROR)
            return
        self.output_console.clear()
        if hasattr(self.script_engine, 'set_script'):
            self.script_engine.set_script(script)
        
        if hasattr(self.script_engine, 'start'):
            self.script_engine.start()
        self.run_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.script_started.emit()
    
    def _on_stop_clicked(self):
        if hasattr(self.script_engine, 'stop_script'):
            self.script_engine.stop_script()
        self._append_output(self.cfg.STOPPING_SCRIPT_MESSAGE)
    
    def _on_script_finished(self):
        self.run_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.script_stopped.emit()
    
    def _append_output(self, text: str):
        self.output_console.append(text)
        if self.cfg.AUTO_SCROLL_ENABLED:
            scrollbar = self.output_console.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def _append_error(self, text: str):
        self.output_console.append(
            f'<span style="color: {self.cfg.ERROR_COLOR};">{text}</span>'
        )
        if self.cfg.AUTO_SCROLL_ENABLED:
            scrollbar = self.output_console.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def _load_example_script(self):
        self.script_editor.setPlainText(self.cfg.EXAMPLE_SCRIPT)
        self.current_script_file = None
        self._stop_watching_file()
    
    def _save_script(self):
        result = self.file_manager.save_script(self.script_editor.toPlainText())
        if result:
            self.current_script_file = result
            self._append_output(self.cfg.SAVE_SUCCESS_FORMAT.format(filename=result))
            self._start_watching_file(result)
    
    def _load_script(self):
        result = self.file_manager.load_script()
        if result:
            filename, content = result
            self.script_editor.setPlainText(content)
            self.current_script_file = filename
            self._append_output(self.cfg.LOAD_SUCCESS_FORMAT.format(filename=filename))
            self._start_watching_file(filename)
    
    def _open_manual(self):
        if self.file_manager.open_manual():
            self._append_output("Manual opened successfully")
        else:
            self._append_error("Manual file not found")
    
    def _start_watching_file(self, filepath: str):
        self.file_manager.watch_script_file(filepath, self._on_script_file_changed)
    
    def _stop_watching_file(self):
        if self.current_script_file:
            self.file_manager.unwatch_script_file(self.current_script_file)
    
    def _on_script_file_changed(self, filepath: str):
        if filepath == self.current_script_file:
            result = self.file_manager.load_script(filepath)
            if result:
                _, content = result
                self.script_editor.setPlainText(content)
                self._append_output(f"Reloaded script from {filepath}")
    
    def set_file_manager(self, file_manager: FileManager):
        self.file_manager = file_manager
    
    def cleanup(self):
        self._stop_watching_file()
        if hasattr(self.file_manager, 'cleanup'):
            self.file_manager.cleanup()