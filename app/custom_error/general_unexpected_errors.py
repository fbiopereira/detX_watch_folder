from .base_error import BaseError
import app

class GeneralUnexpectedError(BaseError):
    def __init__(self, message):
        super().__init__(
            code="WFUE000",
            message="Erro inesperado no {0}: {1}".format(app.flask_app.config['SERVICE_NAME'], message),
            friendly_message="Erro inesperado no {}.".format(app.flask_app.config['SERVICE_NAME']),
            http_status=500)

class WatchFolderUnexpectedError(BaseError):
    def __init__(self, message):
        super().__init__(
            code="WFUE001",
            message="Erro inesperado no {0}: {1}".format(app.flask_app.config['SERVICE_NAME'], message),
            friendly_message="Erro inesperado no processo de watch folder do {}.".format(app.flask_app.config['SERVICE_NAME']),
            http_status=500)

