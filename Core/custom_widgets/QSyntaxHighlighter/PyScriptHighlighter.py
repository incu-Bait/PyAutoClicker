from Core.globals.Base_import import *
from Core.configs.ScriptPanel_Configs import ScriptPanelConfig


class PyScriptHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.cfg = config or ScriptPanelConfig()
        self.highlighting_rules = []
        
        self._setup_highlighting_rules()
    
    def _setup_highlighting_rules(self):
        # --- Python keywords format ---
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(self.cfg.SYNTAX_KEYWORD_COLOR))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        for word in self.cfg.AUTO_INDENT_KEYWORDS + [
            'and', 'as', 'assert', 'break', 'continue', 'del', 'finally', 
            'from', 'global', 'import', 'in', 'is', 'lambda', 'nonlocal',
            'not', 'or', 'pass', 'raise', 'return', 'with', 'yield', 
            'True', 'False', 'None'
        ]:
            pattern = QRegularExpression(f"\\b{word}\\b")
            rule = (pattern, keyword_format)
            self.highlighting_rules.append(rule)
        
        # --- PyScript API methods --- 
        pyscript_api_format = QTextCharFormat()
        pyscript_api_format.setForeground(QColor(self.cfg.SYNTAX_PYSCRIPT_API_COLOR))
        pyscript_api_format.setFontWeight(QFont.Weight.Bold)
        
        pyscript_api_methods = [
            'click', 'move', 'wait', 'get_position', 'log', 'stop', 'is_running',
            'on', 'emit', 'get_mouse_state', 'is_button_pressed', 'get_button_state',
            'get_mouse_position', 'get_last_click_info', 'drag_to', 'mouse_down',
            'mouse_up', 'is_dragging', 'get_drag_info', 'mouse_scroll',
            'wait_for_button_press', 'wait_for_button_release'
        ]
        
        for method in pyscript_api_methods:
            pattern = QRegularExpression(f"\\bpyscript\\.{method}\\b")
            rule = (pattern, pyscript_api_format)
            self.highlighting_rules.append(rule)
        
        # --- PyScript object --- 
        pyscript_obj_format = QTextCharFormat()
        pyscript_obj_format.setForeground(QColor(self.cfg.SYNTAX_PYSCRIPT_OBJECT_COLOR))
        pyscript_obj_format.setFontWeight(QFont.Weight.Bold)
        pyscript_obj_pattern = QRegularExpression(f"\\bpyscript\\b")
        rule = (pyscript_obj_pattern, pyscript_obj_format)
        self.highlighting_rules.append(rule)
        
        # --- Builtin functions format ---
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(self.cfg.SYNTAX_BUILTIN_COLOR))
        builtin_functions = [
            'print', 'range', 'len', 'str', 'int', 'float', 'bool', 'list',
            'dict', 'tuple', 'set', 'min', 'max', 'sum', 'abs', 'round'
        ]
        
        for func in builtin_functions:
            pattern = QRegularExpression(f"\\b{func}\\b")
            rule = (pattern, builtin_format)
            self.highlighting_rules.append(rule)
        
        # --- Module imports format ---
        module_format = QTextCharFormat()
        module_format.setForeground(QColor(self.cfg.SYNTAX_MODULE_COLOR))
        modules = ['random', 'time']
        for module in modules:
            pattern = QRegularExpression(f"\\b{module}\\b")
            rule = (pattern, module_format)
            self.highlighting_rules.append(rule)

        # --- String format ---
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(self.cfg.SYNTAX_STRING_COLOR))
        
        string_patterns = [
            QRegularExpression("\".*\""),
            QRegularExpression("'.*'"),
            QRegularExpression("\"\"\".*\"\"\"", QRegularExpression.PatternOption.DotMatchesEverythingOption),
            QRegularExpression("'''.*'''", QRegularExpression.PatternOption.DotMatchesEverythingOption)
        ]
        
        for pattern in string_patterns:
            rule = (pattern, string_format)
            self.highlighting_rules.append(rule)
        
        # --- Comment format ---
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(self.cfg.SYNTAX_COMMENT_COLOR))
        comment_pattern = QRegularExpression("#[^\n]*")
        rule = (comment_pattern, comment_format)
        self.highlighting_rules.append(rule)
        
        # --- Number format ---
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(self.cfg.SYNTAX_NUMBER_COLOR))
        number_pattern = QRegularExpression("\\b[0-9]+\\b")
        rule = (number_pattern, number_format)
        self.highlighting_rules.append(rule)
        
        # --- Function calls format ---
        function_call_format = QTextCharFormat()
        function_call_format.setForeground(QColor(self.cfg.SYNTAX_FUNCTION_CALL_COLOR))
        function_call_pattern = QRegularExpression("\\b[a-zA-Z_][a-zA-Z0-9_]*\\s*(?=\\()")
        rule = (function_call_pattern, function_call_format)
        self.highlighting_rules.append(rule)
    
    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)