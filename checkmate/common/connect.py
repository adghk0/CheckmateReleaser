"""시스템 기본 연결 도구
"""
from abc import abstractmethod
from pyqconn import Connector
from pyqconn import ConnectionConfig
from pyqconn import MySQLDatabase
from pyqconn import FTPConnector

from checkmate.common.system import *
from checkmate.common.log import Logger

class SystemConnector(Connector):
    """ 설정 파일로 시스템 기본 연결
    """
    def __init__(self, config_file: str):
        self.conn_config = ConnectionConfig(config_file)
        self.db_config = self.conn_config.get('DB')
        self.client_id = None
        self.client_version = None
        self.connect(**self.db_config)

    def connect(self, **kwargs) -> bool:
        self.db = MySQLDatabase(**kwargs)
        self.refresh_table_list()
        self.initial_config_table()
        self.refresh_config()
        self.ftp = FTPConnector(**self.config['System']['ftp'])
        self.log = Logger(self)

    def close(self) -> bool:
        self.close()

    @property
    @abstractmethod
    def program(self):
        pass

    ### Default Config
    def refresh_table_list(self):
        self.table_list = {}
        for (table_id, table_name) in self.db.select(
                self.conn_config.get('System')['table_list']
                )[1]:
            self.table_list[table_id] = table_name
        
    ### Config Tables
    # TODO : 설정 테이블 간 우선순위 생성
    def initial_config_table(self):
        self.client_config_table = {}
        self.set_config_table('Default', 'System', self.table_list['default_configure'])
        self._set_config_connector_table_()

    @abstractmethod
    def _set_config_connector_table_(self):
        pass

    def set_config_table(self, mode: str, category: str, table_name: str):
        self.client_config_table[table_name] = (mode, category)

    def clear_config_table(self, table_name: str):
        del(self.client_config_table[table_name])    

    ### OS
    

    ### Version


    ### Config
    # TODO: 클라이언트 설정하기
    def _get_config_(self, config: dict, category: str, table: str, client_id: int = None):
        config_queue = {}
        if client_id:
            config_data = self.db.select(table, ['priority', 'section', 'parameter_key', 'data', 'config_type'], {'client_id': client_id})[1]
        else:
            config_data = self.db.select(table, ['priority', 'section', 'parameter_key', 'data', 'config_type'])[1]

        for data in config_data:
            config_queue[data[0]] = data[1:]
        
        for priority in sorted(config_queue.keys()):
            section, key, value, config_type = config_queue[priority]
            
            if category not in config:
                config[category] = {}
            if section not in config[category]:
                config[category][section] = {}

            if config_type == 'Set':
                config[category][section][key] = value 
            elif config_type == 'Clear':
                del(config[category][section][key])
            elif config_type == 'Append':
                if key in config[category][section]:
                    if type(config[category][section][key]) == list:
                        config[category][section][key].append(value)
                    else:
                        config[category][section][key] = [
                            config[category][section][key],
                            value]
                else:
                    config[category][section][key] = [value]
            elif config_type == 'Remove':
                config[category][section][key].remove(value)

    def get_config(self, client_id: int = None):
        config = {}
        for (table_name, (mode, category)) in self.client_config_table.items():
            if mode == 'Default':
                self._get_config_(config, category, table_name, None)
            elif mode == 'Client':
                if client_id is not None:
                    self._get_config_(config, category, table_name, client_id)
            else:
                # TODO: 잘못된 값 처리
                pass
        return config

    def refresh_config(self):
        self.config = self.get_config(self.client_id)
