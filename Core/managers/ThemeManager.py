from Core.globals.Base_import import *
from Core.configs.Theme_Configs import *


class PyStyleSheet:
    @staticmethod
    def generate(theme: Dict[str, str]) -> str:
        with open(QSS_PATH, 'r') as qss_file:
            qss_style_template = qss_file.read()
        replacements = {
            '{{font_family}}': FONT_CONFIG['family'],
            '{{font_size}}': FONT_CONFIG['size'],
            '{{bg_primary}}': theme['bg_primary'],
            '{{bg_secondary}}': theme['bg_secondary'],
            '{{bg_tertiary}}': theme['bg_tertiary'],
            '{{text_primary}}': theme['text_primary'],
            '{{text_secondary}}': theme['text_secondary'],
            '{{accent}}': theme['accent'],
            '{{highlight}}': theme['highlight'],
            '{{border}}': theme['border'],
            '{{success}}': theme['success'],
            '{{warning}}': theme['warning'],
            '{{error}}': theme['error'],
            '{{warning_insane}}': theme.get('warning_insane', '#8B0000'),
            '{{warning_text_insane}}': theme.get('warning_text_insane', '#FFFFFF'),
            '{{warning_extreme}}': theme.get('warning_extreme', '#DC3545'),
            '{{warning_text_extreme}}': theme.get('warning_text_extreme', '#FFFFFF'),
            '{{warning_ultra}}': theme.get('warning_ultra', '#FF6B35'),
            '{{warning_text_ultra}}': theme.get('warning_text_ultra', '#FFFFFF'),
            '{{warning_fast}}': theme.get('warning_fast', '#FFC107'),
            '{{warning_text_fast}}': theme.get('warning_text_fast', '#856404'),
        }
        for placeholder, value in replacements.items():
            qss_style_template = qss_style_template.replace(placeholder, value)
        
        return qss_style_template

class ThemeManager:
    def __init__(self):
        self.current_theme = DEFAULT_THEME
        self.themes = THEME_PRESETS
    
    def get_available_themes(self):
        return list(self.themes.keys())
    
    def get_theme(self, theme_name: Optional[str] = None) -> Dict[str, str]:
        if theme_name and theme_name in self.themes:
            return self.themes[theme_name]
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name: str) -> bool:
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def PyStyleSheet(self, theme_name: Optional[str] = None) -> str:
        theme = self.get_theme(theme_name)
        return PyStyleSheet.generate(theme)