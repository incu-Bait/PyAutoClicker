from Core.globals.Base_import import pyqtSignal, QThread, random, time, traceback, List
from Core.script_engine.PyScriptAPI import PyScript
from Core.script_engine.configs.PyScript_Configs import PyScriptConfig
from typing import Dict, Any, Optional


class PyScriptEngine(QThread):
    log_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()
    
    def __init__(self, clicker_thread: Any) -> None:
        super().__init__()
        self.cfg: PyScriptConfig = PyScriptConfig
        self.clicker: Any = clicker_thread
        self.script_code: str = ""
        self.is_running: bool = False
        self.pyscript: PyScript = PyScript(clicker_thread, self)
        self.start_time: Optional[float] = None
        
    def set_script(self, code: str) -> None:
        self.script_code = code
    
    def run(self) -> None:
        if not self.script_code.strip():
            self.error_signal.emit(self.cfg.EMPTY_SCRIPT_MESSAGE)
            return
            
        self.is_running = True
        self.start_time = time.time()
        self.pyscript._should_stop = False
        safe_globals: Dict[str, Any] = {
            '__builtins__': self._create_safe_builtins(),
            'pyscript': self.pyscript,
        }
        for module_name in self.cfg.ALLOWED_MODULES:
            if module_name == 'random':
                safe_globals['random'] = random
            elif module_name == 'time':
                safe_globals['time'] = time
        
        try:
            self.pyscript.emit('script_start', {'time': self.start_time})

            self.log_signal.emit(self.cfg.SCRIPT_START_MESSAGE)

            if self.cfg.MAX_SCRIPT_EXECUTION_TIME > 0:
                self._execute_with_timeout(self.script_code, safe_globals)
            else:
                exec(self.script_code, safe_globals)
            
            self.log_signal.emit(self.cfg.SCRIPT_COMPLETE_MESSAGE)
            
        except StopIteration as e:
            self.log_signal.emit(f"{self.cfg.SCRIPT_STOPPED_MESSAGE}: {str(e)}")
        except TimeoutError as e:
            error_msg: str = f"Script timeout after {self.cfg.MAX_SCRIPT_EXECUTION_TIME}s"
            self.error_signal.emit(error_msg)
            self.pyscript.emit('script_error', {'error': error_msg, 'type': 'timeout'})
        except Exception as e:
            error_msg: str = self.cfg.ERROR_FORMAT.format(
                error=str(e),
                traceback=traceback.format_exc()
            )
            self.error_signal.emit(error_msg)
            self.pyscript.emit('script_error', {'error': str(e), 'traceback': traceback.format_exc()})

            if self.cfg.AUTO_STOP_ON_ERROR:
                self.pyscript._should_stop = True
        finally:
            self.is_running = False
            self.finished_signal.emit()

            elapsed: float = time.time() - self.start_time if self.start_time else 0
            self.pyscript.emit('script_stop', {'elapsed_time': elapsed})
    
    def _create_safe_builtins(self) -> Dict[str, Any]:
        safe_builtins: Dict[str, Any] = {}
        import builtins
        
        for func_name in self.cfg.ALLOWED_BUILTINS:
            if hasattr(builtins, func_name):
                safe_builtins[func_name] = getattr(builtins, func_name)
        
        safe_builtins['print'] = lambda *args, **kwargs: self._safe_print(*args, **kwargs)
        
        return safe_builtins
    
    def _safe_print(self, *args: Any, **kwargs: Any) -> None:
        sep: str = kwargs.get('sep', ' ')
        end: str = kwargs.get('end', '\n')

        message: str = sep.join(str(arg) for arg in args) + end

        if message.endswith('\n'):
            message = message[:-1]
            
        self.log_signal.emit(message)
    
    def _execute_with_timeout(self, code: str, globals_dict: Dict[str, Any]) -> None:
        import threading
        import sys
        
        result: List[Any] = []
        exception: List[Exception] = []
        
        def target() -> None:
            try:
                exec_result: Any = exec(code, globals_dict)
                result.append(exec_result)
            except Exception as e:
                exception.append(e)
        
        thread: threading.Thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        
        thread.join(self.cfg.MAX_SCRIPT_EXECUTION_TIME)
        if thread.is_alive():
            raise TimeoutError(f"Script exceeded maximum execution time of {self.cfg.MAX_SCRIPT_EXECUTION_TIME} seconds")
        
        if exception:
            raise exception[0]
    
    def stop_script(self) -> None:
        self.pyscript._should_stop = True
        if self.isRunning():
            wait_success: bool = self.wait(self.cfg.THREAD_WAIT_TIMEOUT)
            if not wait_success and self.cfg.FORCE_TERMINATE_THREAD:
                self.terminate()
                self.log_signal.emit("Script force terminated")
    
    def get_execution_time(self) -> float:
        if self.start_time:
            return time.time() - self.start_time
        return 0
    
    def is_script_running(self) -> bool:
        return self.is_running
    
    def get_script_code(self) -> str:
        return self.script_code
    
    def clear_script(self) -> None:
        self.script_code = ""