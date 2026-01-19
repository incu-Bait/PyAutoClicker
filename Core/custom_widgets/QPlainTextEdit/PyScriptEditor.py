from Core.globals.Base_import import *
from Core.configs.ScriptPanel_Configs import ScriptPanelConfig
from Core.QWidgets.LineNumberArea import LineNumberArea


class ScriptEditor(QPlainTextEdit):
    def __init__(self, parent=None, config=None):
        super().__init__(parent)
        self.cfg = config or ScriptPanelConfig()
        self.line_number_area = LineNumberArea(self)
        
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        
        self.update_line_number_area_width(0)
        self.highlight_current_line()
    
    def line_number_area_width(self):
        digits = 1
        max_num = max(1, self.blockCount())
        while max_num >= 10:
            max_num //= 10
            digits += 1
        
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space
    
    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(
            cr.left(), cr.top(),
            self.line_number_area_width(), cr.height()
        ))
    
    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        line_number_bg = QColor(self.cfg.LINE_NUMBER_BACKGROUND)
        painter.fillRect(event.rect(), line_number_bg)
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())
        line_number_color = QColor(self.cfg.LINE_NUMBER_COLOR)
        painter.setPen(line_number_color)
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(
                    0, top,
                    self.line_number_area.width() - 3,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number
                )            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            block_number += 1
    
    def highlight_current_line(self):
        extra_selections = []
        
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(self.cfg.CURRENT_LINE_COLOR)
            selection.format.setBackground(line_color)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        
        self.setExtraSelections(extra_selections)
    
    def keyPressEvent(self, event):
        # --- Handle auto indentation for specific keys ---
        if event.key() == Qt.Key.Key_Return:
            cursor = self.textCursor()
            current_block = cursor.block()
            current_text = current_block.text()
            leading_spaces = 0
            leading_tabs = 0
            for char in current_text:
                if char == ' ':
                    leading_spaces += 1
                elif char == '\t':
                    leading_tabs += 1
                else:
                    break
            extra_indent = False
            line_text = current_text.strip()
            indent_keywords = ['if', 'for', 'while', 'def', 'class', 'with', 'try', 'except', 'else', 'elif']
            
            for keyword in indent_keywords:
                if line_text.startswith(f'{keyword} '):
                    if keyword == line_text.split()[0]:
                        extra_indent = True
                        break
            if line_text.endswith(':'):
                extra_indent = True
            super().keyPressEvent(event) # \\ DONT MOVE THIS
            # --- Apply indentation based on config ---
            if self.cfg.USE_TABS_FOR_INDENT:
                indent_char = '\t'
            else:
                indent_char = ' '
            if leading_tabs > 0 and self.cfg.USE_TABS_FOR_INDENT:
                cursor.insertText(indent_char * leading_tabs)
            elif leading_spaces > 0 and not self.cfg.USE_TABS_FOR_INDENT:
                existing_indents = leading_spaces // self.cfg.INDENT_SIZE
                cursor.insertText(indent_char * (existing_indents * self.cfg.INDENT_SIZE))
            if extra_indent and self.cfg.AUTO_INDENT_ENABLED:
                cursor.insertText(indent_char * self.cfg.INDENT_SIZE)
        else:
            super().keyPressEvent(event)