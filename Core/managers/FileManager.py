from Core.globals.Base_import import *


class FileManager:
    def __init__(self, keybind_manager: Any, event_handler: Any) -> None:
        self.keybind_manager: Any = keybind_manager
        self.event_handler: Any = event_handler
        self.file_watcher: QFileSystemWatcher = QFileSystemWatcher()
        self._setup_file_watcher()
    
    def _setup_file_watcher(self) -> None:
        config_file: str = self.keybind_manager.config_file
        config_dir: str = os.path.dirname(config_file)
        if os.path.exists(config_dir):
            self.file_watcher.addPath(config_dir)
            if os.path.exists(config_file):
                self.file_watcher.addPath(config_file)
            self.file_watcher.directoryChanged.connect(self._on_directory_changed)
            self.file_watcher.fileChanged.connect(self._on_file_changed)
    
    def _on_directory_changed(self, path: str) -> None:
        config_file: str = self.keybind_manager.config_file
        
        # --- If config file was just created, start watching it (-,-) --- 
        if os.path.exists(config_file) and config_file not in self.file_watcher.files():
            self.file_watcher.addPath(config_file)
            print(f"Started watching config file: {config_file}")
    
    def _on_file_changed(self, path: str) -> None:
        if path == self.keybind_manager.config_file:
            print(f"Keybinds file changed: {path}")
            
    def get_keybind_info(self) -> List[Tuple[str, str, Optional[str]]]:
        return self.keybind_manager.get_all_keybinds()
    
    def get_keybind(self, action: str) -> Optional[str]:
        return self.keybind_manager.get_keybind(action)
    
    def cleanup(self) -> None:
        if self.file_watcher:
            self.file_watcher.deleteLater()