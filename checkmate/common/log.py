from datetime import datetime

from pyqconn import MySQLDatabase
from checkmate.common.system import outer_ip

def _c_time_(time_format: str = '%y-%m-%d %H:%M:%S.%f'):
    return datetime.now().strftime(time_format)

class Logger:
    def __init__(self, conn):
        self.conn = conn
        self.log_table = conn.table_list['system_log']
        self.program = conn.program()
        self.db = MySQLDatabase(**conn.db_config)

    def print(self, level: int, message: str):
        if self.conn.client_id and self.conn.client_version:
            log = f'{self.program:^10} [{self.conn.client_id} ({self.conn.client_version})] : ({level}) - {message}'
        else:
            log = f'{self.program:^10} : ({level}) - {message}'
        print(log)

    def logging(self, level: int, message: str):
        self.print(level, message)
        log_data = {
            'ip': outer_ip(),
            'program': self.program,
            'level': level,
            'message': message
        }
        if self.conn.client_id and self.conn.client_version:
            log_data['client_id'] = self.conn.client_id
            log_data['client_version'] = self.conn.client_version
        self.db.insert(self.log_table, log_data)
        self.db.commit()

    def l(self, level: int, message: str):
        self.logging(level, message)
