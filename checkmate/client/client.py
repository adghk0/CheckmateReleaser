from threading import Thread

from checkmate.common import SystemConnector, Work
from checkmate.client.schedule import Scheduler

class Client(Thread):
    def __init__(self, config_file: str):
        self.conn = SystemConnector(config_file)
        self.id = self.conn.config.get('Client')['id']
        self.config = self.conn.get_client_config(self.id)
        self.information = self.conn.get_client_information(self.id)
        self.scheduler = Scheduler()

    def start():
        pass

    def terminate():
        pass

    

