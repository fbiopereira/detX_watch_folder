from flask import Flask
from flask_restplus import Api
from config import config
from app.custom_log import CustomLog
from app.helpers import get_service_version, process_async
from prometheus_flask_exporter import PrometheusMetrics
from .services import HealthApi, InfoApi, support_namespace
from app.core import WatcherWorker

import os

config_name = os.environ.get('ENVIRONMENT')

log = CustomLog(service_version=get_service_version())

flask_app = Flask(__name__)
metrics = PrometheusMetrics(flask_app)

flask_app.config.from_object(config[config_name])

flask_app.config.SWAGGER_SUPPORTED_SUBMIT_METHODS = ['get']

api = Api(app=flask_app,  doc="/docs", version=get_service_version(),
          title="DetX Watch Folder", description="Watch Folder que inicializa o processo de verificacao de arquivos. <style>.models {display: none !important}</style>",
          validate=True, catch_all_404s=False)

api.add_namespace(support_namespace.support_namespace, path="/monit")

watcher_worker = WatcherWorker()
process_async(watcher_worker.start)

pass
