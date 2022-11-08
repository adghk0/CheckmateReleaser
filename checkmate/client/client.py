""" 클라이언트 생성 관련 도구
"""
from checkmate.common import SystemConnector, Work
from checkmate.common import Scheduler

class Client():
    def __init__(self, config_file: str):
        self.conn = SystemConnector(config_file)
        
        self.id = self.conn.conn_config.get('Client')['id']
        self.config = self.conn.get_config(self.id)
        self.information = self.conn.get_client_information(self.id)


