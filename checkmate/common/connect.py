from pyqconn import Connector, ConnectionConfig, MySQLDatabase

class SystemConnector(Connector):

    def __init__(self, config_file: str):
        self.config = ConnectionConfig(config_file)
        self.connect(**self.config.get('DB'))

    def connect(self, **kwargs) -> bool:
        self.db = MySQLDatabase(**kwargs)
        self.refresh_table_list()

    def close(self) -> bool:
        self.close()


    # Default Config

    def refresh_table_list(self):
        self.table_list = {}
        for (table_id, table_name) in self.db.select(
                self.config.get("Checkmate")['table_list']
                )[1]:
            self.table_list[table_id] = table_name
        
        self.initial_client_config_table()
        

    # Client Config Tables
    # TODO : 설정 테이블 간 우선순위 생성
    def initial_client_config_table(self):
        self.client_config_table = {
            self.table_list['client_default_configure']: ("Default", "Checkmate"),
            self.table_list['client_configure']: ("Client", "Checkmate")
        }
        
    def set_client_config_table(self, mode: str, table_name: str):
        self.client_config_table[table_name] = mode

    def clear_client_config_table(self, table_name: str):
        del(self.client_config_table[table_name])    

    ### Client

    # Client Informatation
    def get_client_information(self, client_id):
        row, data = self.db.select(
            self.table_list['client_information'],
            None,
            {'client_id': client_id}
        )
        if row == 0:
            result = None
        else:
            result = {
                'client_id': data[0][0],
                'client_name': data[0][1],
                'program_version': data[0][2],
                'operating_system': data[0][3],
                'program_path': data[0][4],
                'last_signal_time': data[0][5],
                'last_signal_status': data[0][6]
            }
        return result

    # Client Config
    # TODO: 클라이언트 설정하기
    def _get_client_config_(self, config: dict, category: str, table: str, client_id: int = None):
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

    def get_client_config(self, client_id: int):
        config = {}
        for (table_name, (mode, category)) in self.client_config_table.items():
            if mode == 'Default':
                self._get_client_config_(config, category, table_name, None)
            elif mode == 'Client':
                self._get_client_config_(config, category, table_name, client_id)
            else:
                # TODO: 잘못된 값 처리
                pass
        return config
