""" 시스템 관리 도구
"""

import os

from checkmate.common import SystemConnector

class Server(SystemConnector):
    def __init__(self, config_file: str):
        super().__init__(config_file)
        self.log.l(10, 'New server application has started.')

    def program(self):
        return 'Server'

    def _set_config_connector_table_(self):
        config_table = [
            ('Default', 'System', self.table_list['server_configure']),
        ]
        for config_info in config_table:
            self.set_config_table(*config_info)

    ### Release
    def release(self, path: str, version: str, description: str):
        self.log.l(10, f'try to release new client program at {path} as client [{version}]')
        version_table = self.table_list['client_version']
        if not self.db.check(version_table, {'version': version}):
            remote_path = self.config['System']['program']['remote_path']
            self.ftp.upload_dir(path, os.path.join(remote_path, version), rapper=False)
            self.db.insert(version_table, {'version': version, 'description': description})
            self.db.commit()
            self.log.l(3, f'client [{version}] has successfully released')
        else:
            self.log.l(1, f'client [{version}] is alredy existed')
       