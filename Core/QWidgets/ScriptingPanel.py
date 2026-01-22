from Core.globals.Base_import import *
from Core.configs.ScriptPanel_Configs import ScriptPanelConfig
from Core.custom_widgets.QPlainTextEdit.PyScriptEditor import ScriptEditor
from Core.custom_widgets.QSyntaxHighlighter.PyScriptHighlighter import PyScriptHighlighter


class ScriptPanel(QWidget):
    script_started = pyqtSignal()
    script_stopped = pyqtSignal()
    
    def __init__(self, script_engine):
        super().__init__()
        self.script_engine = script_engine
        self.cfg = ScriptPanelConfig()
        self._setup_ui()
        self._connect_signals()
        self._load_example_script()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(*self.cfg.LAYOUT_MARGINS)
        layout.setSpacing(self.cfg.LAYOUT_SPACING)
        self.setObjectName(self.cfg.SCRIPT_PANEL_OBJECT_NAME)
        
        # --- Header Buttons ---
        header = QHBoxLayout()
        
        # --- Help button on the left ---
        self.help_btn = QPushButton("Documents")
        self.help_btn.setFixedSize(100, 30)  
        self.help_btn.setObjectName("help_button")
        self.help_btn.setToolTip("Open Scripting Manual")
        header.addWidget(self.help_btn)
        
        self.run_btn = QPushButton(self.cfg.RUN_BUTTON_TEXT)
        self.stop_btn = QPushButton(self.cfg.STOP_BUTTON_TEXT)
        self.run_btn.setMinimumHeight(self.cfg.BUTTON_MIN_HEIGHT)
        self.stop_btn.setMinimumHeight(self.cfg.BUTTON_MIN_HEIGHT)
        self.stop_btn.setEnabled(False)
        self.run_btn.setObjectName(self.cfg.RUN_BUTTON_OBJECT_NAME)
        self.stop_btn.setObjectName(self.cfg.STOP_BUTTON_OBJECT_NAME)
        
        header.addStretch()
        header.addWidget(self.run_btn)
        header.addWidget(self.stop_btn)
        layout.addLayout(header)
        
        # --- Script editor with line numbers ---
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
        
        # --- Quick action buttons ---
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
        
        # --- Output console ---
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
    
    def _save_script(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 
            self.cfg.SAVE_DIALOG_TITLE, 
            "", 
            self.cfg.FILE_FILTER
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.script_editor.toPlainText())
                self._append_output(self.cfg.SAVE_SUCCESS_FORMAT.format(filename=filename))
            except Exception as e:
                self._append_error(self.cfg.SAVE_ERROR_FORMAT.format(error=e))
    
    def _load_script(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            self.cfg.LOAD_DIALOG_TITLE,
            "",
            self.cfg.FILE_FILTER
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.script_editor.setPlainText(f.read())
                self._append_output(self.cfg.LOAD_SUCCESS_FORMAT.format(filename=filename))
            except Exception as e:
                self._append_error(self.cfg.LOAD_ERROR_FORMAT.format(error=e))
    
    def _open_manual(self):
        try:
            manual_path = self._find_manual_file()
            
            if manual_path:
                QDesktopServices.openUrl(QUrl.fromLocalFile(manual_path))
            else:
                self._append_error(f"Manual file not found")
                
        except Exception as e:
            self._append_error(f"Error opening manual: {e}")
    
    def _find_manual_file(self):
        possible_paths = [
            r"Manual\PyScripting_Manual.html",
            os.path.join("Manual", "PyScripting_Manual.html"),
        ]
        
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                return abs_path

        return None
