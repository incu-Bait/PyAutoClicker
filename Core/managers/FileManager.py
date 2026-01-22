from Core.globals.Base_import import *


class FileManager:
    def __init__(self, keybind_manager: Any = None, event_handler: Any = None) -> None:
        self.keybind_manager = keybind_manager
        self.event_handler = event_handler
        self.file_watcher = QFileSystemWatcher()
        self.watched_script_files = {}
        self.script_file_callbacks = {}
        if keybind_manager:
            self._setup_keybind_watcher()
    
    def _setup_keybind_watcher(self) -> None:
        if not self.keybind_manager:
            return
        config_file = self.keybind_manager.config_file
        config_dir = os.path.dirname(config_file)
        if os.path.exists(config_dir):
            self.file_watcher.addPath(config_dir)
            if os.path.exists(config_file):
                self.file_watcher.addPath(config_file)
            self.file_watcher.directoryChanged.connect(self._on_directory_changed)
            self.file_watcher.fileChanged.connect(self._on_file_changed)
    
    def _on_directory_changed(self, path: str) -> None:
        if not self.keybind_manager:
            return
        config_file = self.keybind_manager.config_file
        if os.path.exists(config_file) and config_file not in self.file_watcher.files():
            self.file_watcher.addPath(config_file)
            print(f"Started watching config file: {config_file}")
    
    def _on_file_changed(self, path: str) -> None:
        if self.keybind_manager and path == self.keybind_manager.config_file:
            print(f"Keybinds file changed: {path}")
            if hasattr(self.keybind_manager, 'reload_config'):
                self.keybind_manager.reload_config()
        
        if path in self.watched_script_files:
            print(f"Watched script file changed: {path}")
            self._debounce_file_change(path)
    
    def _debounce_file_change(self, path: str) -> None:
        if path in self.watched_script_files:
            self.watched_script_files[path].stop()
        timer = QTimer()
        timer.setSingleShot(True)
        timer.timeout.connect(lambda: self._process_file_change(path))
        timer.start(500)
        self.watched_script_files[path] = timer
    
    def _process_file_change(self, path: str) -> None:
        if path in self.script_file_callbacks:
            for callback in self.script_file_callbacks[path]:
                try:
                    callback(path)
                except Exception as e:
                    print(f"Error in file change callback for {path}: {e}")
    
    def get_keybind_info(self) -> List[Tuple[str, str, Optional[str]]]:
        if self.keybind_manager:
            return self.keybind_manager.get_all_keybinds()
        return []
    
    def get_keybind(self, action: str) -> Optional[str]:
        if self.keybind_manager:
            return self.keybind_manager.get_keybind(action)
        return None
    
    def save_script(self, content: str, default_path: str = "") -> Optional[str]:
        if not default_path:
            default_path = os.path.expanduser("~")
        filename, _ = QFileDialog.getSaveFileName(
            None,
            "Save Script",
            default_path,
            "Python Files (*.py);;Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                if not filename.endswith('.py'):
                    filename += '.py'
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Script saved to: {filename}")
                return filename
            except Exception as e:
                print(f"Error saving script: {e}")
        return None
    
    def load_script(self, default_path: str = "") -> Optional[Tuple[str, str]]:
        if not default_path:
            default_path = os.path.expanduser("~")
        filename, _ = QFileDialog.getOpenFileName(
            None,
            "Load Script",
            default_path,
            "Python Files (*.py);;Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"Script loaded from: {filename}")
                return filename, content
            except Exception as e:
                print(f"Error loading script: {e}")
        return None
    
    def watch_script_file(self, filepath: str, callback: callable) -> bool:
        if not os.path.exists(filepath):
            print(f"File does not exist: {filepath}")
            return False
        try:
            if filepath not in self.file_watcher.files():
                self.file_watcher.addPath(filepath)
            if filepath not in self.script_file_callbacks:
                self.script_file_callbacks[filepath] = []
            self.script_file_callbacks[filepath].append(callback)
            print(f"Started watching file: {filepath}")
            return True
        except Exception as e:
            print(f"Error watching file {filepath}: {e}")
            return False
    
    def unwatch_script_file(self, filepath: str, callback: callable = None) -> None:
        if filepath in self.file_watcher.files():
            self.file_watcher.removePath(filepath)
        if filepath in self.script_file_callbacks:
            if callback:
                if callback in self.script_file_callbacks[filepath]:
                    self.script_file_callbacks[filepath].remove(callback)
            else:
                del self.script_file_callbacks[filepath]
        if filepath in self.watched_script_files:
            self.watched_script_files[filepath].deleteLater()
            del self.watched_script_files[filepath]
    
    def find_file(self, filename: str, search_dirs: List[str] = None) -> Optional[str]:
        if not search_dirs:
            search_dirs = [
                os.path.curdir,
                os.path.expanduser("~"),
                os.path.dirname(__file__) if __file__ else "."
            ]
        for search_dir in search_dirs:
            search_path = os.path.join(search_dir, filename)
            if os.path.exists(search_path):
                return os.path.abspath(search_path)
            for root, dirs, files in os.walk(search_dir):
                if filename in files:
                    return os.path.join(root, filename)
        return None
    
    def open_manual(self, manual_filename: str = "PyScripting_Manual.html") -> bool:
        manual_path = self.find_file(manual_filename)
        if manual_path:
            try:
                QDesktopServices.openUrl(QUrl.fromLocalFile(manual_path))
                return True
            except Exception as e:
                print(f"Error opening manual: {e}")
                return False
        else:
            print(f"Manual file not found: {manual_filename}")
            return False
    
    def cleanup(self) -> None:
        for timer in self.watched_script_files.values():
            timer.deleteLater()
        self.watched_script_files.clear()
        self.script_file_callbacks.clear()
        if self.file_watcher:
            self.file_watcher.deleteLater()