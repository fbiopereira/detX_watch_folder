from datetime import datetime
import platform
import socket
import os
import glob
import logging
import logging.handlers
import logging.config
from logging.handlers import RotatingFileHandler
from logging import StreamHandler
from .json_log_formatter import JSONFormatter

SERVICE_NAME = "media_service_team_log"
LOG_PATH = "{}/custom_log/".format(os.getcwd())
GIT_TAG = "0.0.0"
ENVIRONMENT = 'NAO INFORMADO'

ERROR = {
    'code': "HS001",
    'message': 'valor do status HTTP é inválido'
}


class CustomLog(object):

    def __init__(self, service_version, scope_name=__name__):

        self._max_file_size = 500000
        self._log_folder = os.environ.get('LOG_PATH')
        self.service_name = os.environ.get('SERVICE_NAME').replace(" ", "_")
        self.service_version = service_version
        self.service_host_name = socket.gethostname()
        self.service_ip = socket.gethostbyname(self.service_host_name)
        self.environment = os.getenv('ENVIRONMENT', ENVIRONMENT)
        self.os_name = os.name
        self.os_platform = platform.system()
        self.os_version = platform.release()
        self.python_version = platform.python_version()
        self.create_folder()

        file_name = datetime.now().strftime('%d-%m-%Y.{}_log').format(self.service_name)
        file_path = "{0}{1}".format(self._log_folder, file_name)
        formatter = JSONFormatter()

        file_handler = RotatingFileHandler(
            file_path, maxBytes=self._max_file_size, backupCount=20)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)

        self._logger = logging.getLogger(scope_name)
        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)
        self._logger.setLevel(logging.DEBUG)

    def create_folder(self):
        if not os.path.exists(self._log_folder):
            os.makedirs(self._log_folder)

    def path(self):
        """Return the path of the logs folder.
        For default, path is your folder.
        """
        return self._log_folder

    def service_name_log(self):
        """service name that used in info, warning and error."""
        return self.service_name

    def service_version_log(self):
        """service version thats used in info, warning and error."""
        return self.service_version

    def count_log_files(self):
        """Return number of custom_log files."""
        return len(glob.glob("{0}/*.custom_log*".format(self._log_folder)))

    def get_log_files(self):
        """Return all logs files."""
        return glob.glob("{0}/*.custom_log*".format(self._log_folder))

    def delete_log_files(self):
        for file in glob.glob("{0}/*.custom_log*".format(self._log_folder)):
            try:
                os.remove(file)
            except IOError as io:
                self.error("erro ao excluir")

    def debug(self, message):
        self._logger.debug(message)

    def info(self, class_name=None, method_name=None, file_name=None, message=None):

        log_data = self.mount_service_data()
        log_data.update([('class_name', class_name), ('method', method_name), ('file_name', file_name)])
        self._logger.info(
            message,
            extra={'level': 'INFO', 'data': log_data})
        pass

    def error(self, code, class_name=None, method_name=None, file_name=None, message=None):

        log_data = self.mount_service_data()
        log_data.update([('class_name', class_name), ('method', method_name), ('file_name', file_name), ('error_code', code)])
        self._logger.error(
            message, extra={'level': 'ERROR', 'data': log_data}, exc_info=True)


    def mount_service_data(self):
        service_data = {'service_name': self.service_name,
                        'service_version': self.service_version,
                        'service_host_name': self.service_host_name,
                        'service_ip': self.service_ip,
                        'os_name': self.os_name, 'os_platform': self.os_platform,
                        'os_version': self.os_version,
                        'python_version': self.python_version,
                        'environment': self.environment}

        return service_data
