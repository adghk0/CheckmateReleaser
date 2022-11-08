
import configparser


class ConnectionConfig:
    """ 연결 설정 클래스입니다.
    """
    def __init__(self, file: str):
        self.file = file
        self.config = configparser.ConfigParser()
        self.config.read(self.file)

    def get(self, connection_name: str):
        return self.config[connection_name]