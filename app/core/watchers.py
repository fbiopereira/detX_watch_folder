"""Pattern Watcher Module"""
from .watchdog_handlers import WatcherEventHandler
from .watchdog_observers import WatcherPollingObserver
import app

class PatternWatcher():
    """Pattern Watcher Class"""
    my_name = "PatternWatcher"

    def __init__(self, callback, workdir, ext,
                 timeout=5, recursive=False, blocking=False):

        my_name = "__init__"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Construindo o PatternWatcher::")

        self._observer = WatcherPollingObserver()
        handler2 = WatcherEventHandler(callback, ext, timeout)
        self._observer.schedule(handler2, workdir, recursive=recursive)
        self._blocking = blocking

    def start(self):
        """Start Watcher"""

        my_name = "start"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Iniciando o PatternWatcher::")

        self._observer.start()
        if self._blocking:
            self._observer.join()

    def stop(self):
        """Stop Watcher"""

        my_name = "stop"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Parando o PatternWatcher::")

        self._observer.stop()
