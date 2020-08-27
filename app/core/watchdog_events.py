"""Watchdog events module"""
from watchdog.events import FileSystemEvent
import app

# pylint: disable=too-few-public-methods
class GarbageCollectorEvent(FileSystemEvent):
    """Watchdog Garbage Collector Event"""
    my_name = "GarbageCollectorEvent"
    event_type = 'gc'

    def __init__(self, datetime_event):
        my_name = "__init__"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Iniciando o GarbageCollectorEvent ::")

        super(GarbageCollectorEvent, self).__init__('')
        self._datetime_event = datetime_event

    @property
    def datetime(self):
        """retun datetime"""
        return self._datetime_event

    def __repr__(self):
        return "<%(class_name)s: datetime=%(datetime)r>" %\
               dict(class_name=self.__class__.__name__,
                    datetime=self._datetime_event)
