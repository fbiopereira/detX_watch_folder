import app
from .watchers import PatternWatcher
from .detx_file import DetXFile




class WatcherWorker:
    my_name = "WatcherWorker"
    watcher = None
    det_x = None

    def __init__(self):
        my_name = "__init__"

        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Iniciando a construcao do watcher ::")

        det_x = DetXFile()
        self.watcher = PatternWatcher(
            callback=det_x.detx_file_action,
            workdir=app.flask_app.config['WATCH_FOLDER_PATH'],
            ext=app.flask_app.config['EXTENSIONS'].split(','),
            timeout=float(app.flask_app.config['TIMEOUT_DETECTION']),
            blocking=False,
            recursive=False)

    def start(self):
        my_name = "start"
        app.log.info(class_name=self.my_name, method_name=my_name, file_name=None,
                     message="::Iniciando o watcher ::")
        self.watcher.start()


