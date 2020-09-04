import ntpath
import app
import requests
from app.custom_error import WatchFolderDetXUnexpectedError

class DetXFile:
    my_name = "DetXFile"
    detx_api_url = None
    file_name = None
    json_body = None

    def detx_file_action(self, file):
        my_name = "detx_file_action"

        try:
            self.detx_api_url = app.flask_app.config['DETX_API']
            self.file_name = self.get_file_name(file)
            self.create_body_json()


            app.log.info(class_name=self.my_name, method_name=my_name, file_name=str(self.file_name),
                         message="::Iniciando o processo de chamada do DetX::")

            response = requests.post(self.detx_api_url, json=self.json_body, timeout=None)

            if response.status_code in [200, 201, 204]:
                return True
            else:
                custom_err = WatchFolderDetXUnexpectedError('O servico DetX retornou erro. STATUS_CODEL: {} URL: {} '
                                                            'BODY: {}'.format(response.status_code, self.detx_api_url,
                                                                              self.json_body))
                self.error_log(custom_err, my_name)

        except Exception as ex:
            custom_err = WatchFolderDetXUnexpectedError('Erro no post enviado para o DetX. URL: {} BODY: {} '
                                                        'Exception: {}'.format(str(self.detx_api_url), str(self.json_body), str(ex)))
            self.error_log(custom_err, my_name)

        pass

    def get_file_name(self, file):
        return ntpath.basename(file)

    def error_log(self, custom_err, my_name):
        app.log.error(class_name=self.my_name, code=custom_err.code, method_name=my_name,
                      message=custom_err.message, file_name=str(self.file_name))

    def create_body_json(self):
        self.json_body = {
            "file_name": str(self.file_name)
        }