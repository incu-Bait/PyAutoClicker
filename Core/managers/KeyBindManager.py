from Core.globals.Base_import import *
from Core.configs.KeyBindManager_Configs import KeybindConstants

class KeybindManager:
    def __init__(self, config_file: str = KeybindConstants.CONFIG_FILE) -> None:
        self.config_file: str = config_file
        self.keybinds: Dict[str, str] = self.load_keybinds()
        
    def load_keybinds(self) -> Dict[str, str]:
        default_keybinds: Dict[str, str] = self.get_default_keybinds()
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        if not os.path.exists(self.config_file):
            self.save_keybinds_to_file(default_keybinds)
            print(KeybindConstants.CREATED_FILE_MESSAGE.format(path=os.path.abspath(self.config_file)))
            return default_keybinds
        try:
            with open(self.config_file, 'r') as f:
                loaded_keybinds: Dict[str, str] = json.load(f)
                merged_keybinds: Dict[str, str] = default_keybinds.copy()
                merged_keybinds.update(loaded_keybinds)  
                if merged_keybinds != loaded_keybinds:
                    self.save_keybinds_to_file(merged_keybinds)
                return merged_keybinds
        except (json.JSONDecodeError, IOError) as e:
            self.save_keybinds_to_file(default_keybinds)
            return default_keybinds
    
    def save_keybinds_to_file(self, keybinds: Dict[str, str]) -> None:
        try:
            with open(self.config_file, 'w') as f:
                json.dump(keybinds, f, indent=4, sort_keys=True)
            print(KeybindConstants.SAVED_MESSAGE.format(path=os.path.abspath(self.config_file)))
        except IOError as e:
            print(KeybindConstants.WARNING_SAVE_MESSAGE.format(file=self.config_file, error=e))
    
    def get_default_keybinds(self) -> Dict[str, str]:
        return KeybindConstants.DEFAULT_KEYBINDS.copy()
    
    def get_keybind(self, action: str) -> str:
        return self.keybinds.get(action, "")
    
    def get_all_keybinds(self) -> List[Tuple[str, str, str]]:
        display_names: Dict[str, str] = KeybindConstants.DISPLAY_NAMES
        keybind_list: List[Tuple[str, str, str]] = []
        for action, shortcut in self.keybinds.items():
            if action in display_names:
                readable_name: str = display_names[action]
            else:
                readable_name: str = action.replace('_', ' ').title()
            
            # Only add to list if there's a shortcut assigned
            if shortcut:
                keybind_list.append((action, readable_name, shortcut))
        
        keybind_list.sort(key=lambda x: x[1])
        return keybind_list
    
    def reload_keybinds(self) -> Dict[str, str]:
        self.keybinds = self.load_keybinds()
        return self.keybinds