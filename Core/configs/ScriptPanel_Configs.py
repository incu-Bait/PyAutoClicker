from Core.globals.Base_import import *

class ScriptPanelConfig:
    # ==============================================================================
    # UI DIMENSIONS & GEOMETRY
    # ==============================================================================
    PANEL_MIN_WIDTH = 400
    PANEL_MIN_HEIGHT = 500
    EDITOR_MIN_HEIGHT = 200
    CONSOLE_MIN_HEIGHT = 150
    BUTTON_MIN_HEIGHT = 28
    
    # ==============================================================================
    # LAYOUT & SPACING
    # ==============================================================================
    LAYOUT_MARGINS = (8, 8, 8, 8)
    LAYOUT_SPACING = 6
    BUTTON_SPACING = 6
    
    # ==============================================================================
    # FONT CONFIGURATION
    # ==============================================================================
    EDITOR_FONT_FAMILY = "Courier New"
    EDITOR_FONT_SIZE = 9
    CONSOLE_FONT_FAMILY = "Courier New"
    CONSOLE_FONT_SIZE = 8
    LABEL_FONT_WEIGHT = "bold"
    
    # ==============================================================================
    # UI TEXT & LABELS
    # ==============================================================================
    RUN_BUTTON_TEXT = "Run"
    STOP_BUTTON_TEXT = "Stop"
    CLEAR_BUTTON_TEXT = "Clear"
    EXAMPLE_BUTTON_TEXT = "Example"
    SAVE_BUTTON_TEXT = "Save"
    LOAD_BUTTON_TEXT = "Load"
    
    EDITOR_PLACEHOLDER_TEXT = "# Write Your PyScript here..."
    OUTPUT_LABEL_TEXT = "Output Terminal"
    STOPPING_SCRIPT_MESSAGE = "Stopping script..."
    EDITOR_LABEL_TEXT = "PyScript Editor"
    
    # ==============================================================================
    # EXAMPLE SCRIPT
    # ==============================================================================
    EXAMPLE_SCRIPT = """# ----
# Script Example 
# That Clicks 10 times then stops
# ----

for i in range(10):
    pyscript.click()
    pyscript.log(f"Click {i + 1}/10")
    pyscript.wait(0.5)

pyscript.log("Done!")"""
    
    # ==============================================================================
    # FILE DIALOG CONFIG
    # ==============================================================================
    SAVE_DIALOG_TITLE = "Save Script"
    LOAD_DIALOG_TITLE = "Load Script"
    FILE_FILTER = "Python (*.py);;All (*)"
    
    # ==============================================================================
    # SCRIPT ENGINE CONSTANTS
    # ==============================================================================
    EMPTY_SCRIPT_ERROR = "Error: No script to run"
    SAVE_SUCCESS_FORMAT = "Saved: {filename}"
    SAVE_ERROR_FORMAT = "Save error: {error}"
    LOAD_SUCCESS_FORMAT = "Loaded: {filename}"
    LOAD_ERROR_FORMAT = "Load error: {error}"
    
    # ==============================================================================
    # ERROR & CONSOLE COLORS
    # ==============================================================================
    ERROR_COLOR = "#ff6b6b"
    CONSOLE_BACKGROUND = "transparent"
    
    # ==============================================================================
    # LINE NUMBER AREA
    # ==============================================================================
    LINE_NUMBER_BACKGROUND = "#a5a5a5"
    LINE_NUMBER_COLOR = "#FFFFFF"
    
    # ==============================================================================
    # CURRENT LINE HIGHLIGHT
    # ==============================================================================
    CURRENT_LINE_COLOR = "#3d3d3d"  
    
    # ==============================================================================
    # SYNTAX HIGHLIGHTING COLORS
    # ==============================================================================
    
    SYNTAX_KEYWORD_COLOR = "#906feb"    # \\ Python Keywords       
    SYNTAX_PYSCRIPT_API_COLOR = "#FFD700"  # \\ PyScript API 
    SYNTAX_PYSCRIPT_OBJECT_COLOR = "#FFD700" # \\ PyScript API 
    SYNTAX_STRING_COLOR = "#8bffae"    # \\ Strings        
    SYNTAX_COMMENT_COLOR = "#8A8A8A"    # \\ Comments       
    SYNTAX_NUMBER_COLOR = "#97B0FF"    # \\ Numbers       
    SYNTAX_BUILTIN_COLOR = "#4169E1"    # \\ Builtin Functions      
    SYNTAX_MODULE_COLOR = "#00CED1"    # \\ Modules (random, time)       
    SYNTAX_FUNCTION_CALL_COLOR = "#FF8C00"   # \\ Function Calls
    
    # ==============================================================================
    # AUTO-INDENTATION SETTINGS
    # ==============================================================================
    AUTO_INDENT_ENABLED = True
    INDENT_SIZE = 4          
    USE_TABS_FOR_INDENT = False
    
    # --- Keywords that trigger auto-indentation ---
    AUTO_INDENT_KEYWORDS = [
        'if', 'for', 'while', 'def', 'class', 
        'with', 'try', 'except', 'else', 'elif'
    ]
    
    # ==============================================================================
    # SCROLL BEHAVIOR
    # ==============================================================================
    AUTO_SCROLL_ENABLED = True
    
    # ==============================================================================
    # SIGNAL NAMES
    # ==============================================================================
    SIGNAL_SCRIPT_STARTED = "script_started"
    SIGNAL_SCRIPT_STOPPED = "script_stopped"
    SIGNAL_LOG = "log_signal"
    SIGNAL_ERROR = "error_signal"
    SIGNAL_FINISHED = "finished_signal"
    
    # ==============================================================================
    # OBJECT NAMES (for styling/testing)
    # ==============================================================================
    RUN_BUTTON_OBJECT_NAME = "runButton"
    STOP_BUTTON_OBJECT_NAME = "stopButton"
    CLEAR_BUTTON_OBJECT_NAME = "clearButton"
    EXAMPLE_BUTTON_OBJECT_NAME = "exampleButton"
    SAVE_BUTTON_OBJECT_NAME = "saveButton"
    LOAD_BUTTON_OBJECT_NAME = "loadButton"
    SCRIPT_EDITOR_OBJECT_NAME = "scriptEditor"
    OUTPUT_CONSOLE_OBJECT_NAME = "outputConsole"
    SCRIPT_PANEL_OBJECT_NAME = "scriptPanel"
    
    # ==============================================================================
    # PERFORMANCE SETTINGS
    # ==============================================================================
    SYNTAX_HIGHLIGHTING_ENABLED = True
    LINE_NUMBERS_ENABLED = True
    CURRENT_LINE_HIGHLIGHT_ENABLED = True
    
    # ==============================================================================
    # VALIDATION SETTINGS
    # ==============================================================================
    MAX_SCRIPT_LENGTH = 100000  
    WARN_ON_LONG_SCRIPT = True
    LONG_SCRIPT_THRESHOLD = 10000 


    # ==============================================================================
    # Qt Cursors
    # ==============================================================================
    HAND_CURSOR = Qt.CursorShape.PointingHandCursor