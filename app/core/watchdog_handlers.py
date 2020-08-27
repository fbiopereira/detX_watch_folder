"""Watchdog Handlers Module"""
import logging
from datetime import datetime
from pathtools.patterns import match_any_paths
import app
from app.custom_error import WatchFolderUnexpectedError

# pylint: disable=too-few-public-methods
# pylint: disable=broad-except
class WatcherEventHandler:
    """Watcher Event Handler Class"""

    my_name = "WatcherEventHandler"

    def __init__(self, callback, patterns, timeout=3):

        my_name = "__init__"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Criando o WatcherEventHandler::callback={}::patterns={}::timeout={}"
                     .format(callback, patterns, timeout))

        self.callback = callback
        self.timeout = timeout
        self.files = {}
        self.patterns = patterns
        self.handlers = {
            'gc': self._gc_handler,
            'created': self._create_handler,
            'modified': self._update_handler,
        }

    def dispatch(self, event):
        """Method called by watchdog when one event is dispatched"""

        my_name = "dispatch"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Executando o event dispath::event={}".format(str(event)))

        self.handlers.get(event.event_type, lambda event: None)(event)

    def _gc_handler(self, event):
        my_name = "_gc_handler"

        for file in list(self.files.keys()):
            delta = event.datetime - self.files[file]
            if delta.total_seconds() > self.timeout:
                try:
                    self.callback(file)
                except Exception as ex:

                    custom_err = WatchFolderUnexpectedError(message=str(ex))

                    app.log.error(class_name=self.my_name, code=custom_err.code, method_name=my_name,
                                  message=custom_err.message, file_name=None)

                app.log.info(class_name=self.my_name, method_name=my_name, file_name=self.files[file],
                             message="::GC FILE={}".format(self.files[file]))

                del self.files[file]

    def _create_handler(self, event):
        my_name = "_create_handler"

        if match_any_paths([event.src_path], included_patterns=self.patterns):
            self.files[event.src_path] = datetime.now()

            app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                         message="::File created={}::".format(event))

    def _update_handler(self, event):
        my_name = "_update_handler"

        if event.src_path in self.files and match_any_paths([event.src_path],
                                                            included_patterns=self.patterns):
            self.files[event.src_path] = datetime.now()

            app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                         message="::File modified={}::".format(event))
