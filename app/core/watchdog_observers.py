"""Watchdog Observer Module"""
from datetime import datetime
from watchdog.observers.polling import PollingEmitter
from watchdog.observers.api import BaseObserver
from .watchdog_events import GarbageCollectorEvent
import app

class WatcherPollingEmitter(PollingEmitter):
    """Watcher Polling Emitter"""

    my_name = "WatcherPollingEmitter"

    def queue_events(self, timeout):

        my_name = "queue_events"

        my_name = "queue_events"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Criando o WatcherPollingEmitter::timeout={}".format(timeout))

        super().queue_events(timeout)
        with self._lock:
            self.queue_event(GarbageCollectorEvent(datetime.now()))

class WatcherPollingObserver(BaseObserver):
    my_name = "WatcherPollingObserver"

    def __init__(self, timeout=5):
        my_name = "__init__"

        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Criando o WatcherPollingObserver::timeout={}".format(timeout))

        BaseObserver.__init__(self, emitter_class=WatcherPollingEmitter, timeout=timeout)
