from flask_restplus import Resource
from app.helpers import get_service_version, get_server_datetime
import app
from .support_namespace import support_namespace


@support_namespace.route("/info")
@support_namespace.response(200, 'Informações da API')
class InfoApi(Resource):

    def get(self):
        server_datetime = get_server_datetime()
        info_return = {
            "version": get_service_version(),
            "environment": app.flask_app.config['ENVIRONMENT'],
            "server_datetime": server_datetime,
            "environment_variables": [
                    {"LOG_PATH": app.flask_app.config['LOG_PATH']},
                    {"SERVICE_NAME": app.flask_app.config['SERVICE_NAME'],
                     "WATCH_FOLDER_PATH": app.flask_app.config['WATCH_FOLDER_PATH']}
                ]
            }

        return info_return, 200



