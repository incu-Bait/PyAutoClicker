from Core.globals.Base_import import *

class FileManager:
    def __init__(self, keybind_manager: Any, settings_panel: Any) -> None:
        self.keybind_manager: Any = keybind_manager
        self.settings_panel: Any = settings_panel
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
        if os.path.exists(config_file) and config_file not in self.file_watcher.files():
            self.file_watcher.addPath(config_file)
    
    def _on_file_changed(self, path: str) -> None:
        if path == self.keybind_manager.config_file:
            print(f"Keybinds file changed: {path}")
            QTimer.singleShot(500, self.reload_and_update_keybinds) # \\ Delay to make sure file reloads, prob not needed and could just run a check
    
    def reload_and_update_keybinds(self) -> None:
        try:
            self.keybind_manager.reload_keybinds()
            if hasattr(self.settings_panel, 'keybind_labels'):
                for action, label_widget in self.settings_panel.keybind_labels.items():
                    keybind_text: Optional[str] = self.keybind_manager.get_keybind(action)
                    label_widget.setText(f"<b>{keybind_text}</b>" if keybind_text else "Not set")
            if hasattr(self.settings_panel, '_update_button_shortcuts'):
                self.settings_panel._update_button_shortcuts()
            print(f"Keybinds reloaded: {self.keybind_manager.keybinds}")
        except Exception as e:
            print(f"Error reloading keybinds: {e}")
    
    def get_keybind_info(self) -> List[Tuple[str, str, Optional[str]]]:
        return self.keybind_manager.get_all_keybinds()
    
    def get_keybind(self, action: str) -> Optional[str]:
        return self.keybind_manager.get_keybind(action)
    
    def cleanup(self) -> None:
        if self.file_watcher:
            self.file_watcher.deleteLater()