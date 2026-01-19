# ============================================
# Keybind Manager
# ============================================
# Manages keyboard shortcuts configuration
# Handles loading, saving, and merging keybinds
# ============================================
from Core.globals.Base_import import *
from Core.configs.KeyBindManager_Configs import KeybindConfigs


class KeybindManager:
    def __init__(self, config_file: str = KeybindConfigs.CONFIG_FILE) -> None:
        self.config_file = config_file
        self.keybinds = self.load_keybinds()
    
    def load_keybinds(self) -> Dict[str, str]:
        if not os.path.exists(self.config_file):
            return self._create_config_with_defaults()
        try:
            return self._load_and_merge_keybinds()
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading keybinds: {e}")
            return self._create_config_with_defaults()
    
    def reload_keybinds(self) -> Dict[str, str]:
        self.keybinds = self.load_keybinds()
        return self.keybinds
    
    def _create_config_with_defaults(self) -> Dict[str, str]:
        defaults = self.get_default_keybinds()
        self.save_keybinds_to_file(defaults)

        message = KeybindConfigs.CREATED_FILE_MESSAGE
        print(message.format(path=os.path.abspath(self.config_file)))
        
        return defaults
    
    def _load_and_merge_keybinds(self) -> Dict[str, str]:
        with open(self.config_file, 'r') as f:
            loaded = json.load(f)
        merged = self.get_default_keybinds()
        merged.update(loaded)
        if merged != loaded:
            self.save_keybinds_to_file(merged)
        
        return merged

    def save_keybinds_to_file(self, keybinds: Dict[str, str]) -> None:
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(keybinds, f, indent=4, sort_keys=True)
            message = KeybindConfigs.SAVED_MESSAGE
            print(message.format(path=os.path.abspath(self.config_file)))
        except IOError as e:
            message = KeybindConfigs.WARNING_SAVE_MESSAGE
            print(message.format(file=self.config_file, error=e))
    
    def update_keybind(self, action: str, shortcut: str) -> None:
        self.keybinds[action] = shortcut
        self.save_keybinds_to_file(self.keybinds)
    
    def get_default_keybinds(self) -> Dict[str, str]:
        return KeybindConfigs.DEFAULT_KEYBINDS.copy()
    
    def get_keybind(self, action: str) -> str:
        return self.keybinds.get(action, "")
    
    def get_all_keybinds(self) -> List[Tuple[str, str, str]]:
        display_names = KeybindConfigs.DISPLAY_NAMES
        keybind_list = []
        
        for action, shortcut in self.keybinds.items():
            if not shortcut:
                continue
            name = display_names.get(action, action.replace('_', ' ').title())
            keybind_list.append((action, name, shortcut))

        keybind_list.sort(key=lambda x: x[1])
        return keybind_list
    
    def has_keybind(self, action: str) -> bool:
        return bool(self.keybinds.get(action))