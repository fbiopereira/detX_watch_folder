import app

class DetXFile:


    @staticmethod
    def detx_file_action(file):
        my_name = "detx_file_action"

        app.log.info(class_name="DetXFile", method_name=my_name, file_name=None,
                     message="::Encontrei o arquivo={}::".format(file))

        pass
