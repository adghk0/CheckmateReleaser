""" 클라이언트 생성 관련 도구
"""
import os, sys

from datetime import datetime

from threading import Thread
import subprocess

from pyqconn import MySQLDatabase
from checkmate.common import SystemConnector, Work, Delay
from checkmate.common.log import _c_time_

class Client(SystemConnector):
    def __init__(self, config_file: str, program_path: str, program_file: str):
        if sys.argv[1] == 'Manager':
            self.program_name = 'Client_Manager'
        elif sys.argv[1] == 'Worker':
            self.program_name = 'Client_Worker'
        else:
            raise Exception('잘못된 인수') # TODO: 잘못된 인수 처리
        
        super().__init__(config_file)
        client_conf = self.conn_config.get('Client')
        self.client_id = client_conf['id']
        self.client_version = client_conf['version']
        self.program_path = program_path
        self.program_file = program_file
        
        if self.program_name == 'Client_Manager':
            self._set_manager_works_()
            self.status = 'Prepared'
            self.interval = self.config['System']['connection']['interval']
            self.log.l(10, f'New client application at "{program_path}" has prepared.')
        else:
            self.client_works = []
            self.log.l(10, f'client worker application at "{program_path}" has started.')

    def program(self):
        return self.program_name

    def _set_config_connector_table_(self):
        config_table = [
            ('Default', 'System', self.table_list['client_default_configure']),
            ('Client', 'System', self.table_list['client_configure'])
        ]
        for config_info in config_table:
            self.set_config_table(*config_info)

    def _set_manager_works_(self):
        self.manager_works = [
            Report(self),
            MakeWorker(self),
            Delay(5)
        ]

    def start(self):
        self.tr = Thread(target=self.run)
        self.tr_run = True
        self.tr.start()

    def stop(self):
        self.tr_run = False

    def run(self):
        if self.program_name == 'Client_Manager':
            works = self.manager_works
        else:
            works = self.client_works

        while self.tr_run:
            for work in works:
                work.execute()

    def append_work(self, work: Work):
        if self.program_name == 'Client_Worker':
            self.client_works.append(work)

    def remove_work(self, work: Work):
        if self.program_name == 'Client_Worker':
            self.client_works.remove(work)

### Manager Works
class Report(Work):
    def __init__(self, client: Client):
        self.client = client

    def execute(self):
        info_table = self.client.table_list['client_information']
        db: MySQLDatabase = self.client.db
        db.update(
            info_table, 
            {'client_id':self.client.client_id},
            {'last_signal_time': _c_time_(),
            'last_signal_status': self.client.status}
            )
        db.commit()

class MakeWorker(Work):
    def __init__(self, client: Client):
        self.client = client
        self.ps = None

    def start_worker(self):
        if self.ps is None:
            program_path = os.path.join(self.client.program_path, self.client.program_file)
            self.ps = subprocess.Popen([sys.executable, program_path, 'Worker'])
    
    def stop_worker(self):
        if self.ps:
            subprocess.call(['taskkill', '/F', '/T', '/PID',  str(self.ps.pid)])
        self.ps = None

    def check_worker(self):
        if self.ps is None:
            pass
        else:
            self.ps.poll()
            if self.ps.returncode is not None:
                self.ps = None
            else:
                pass

    def execute(self):
        self.check_worker()
        if self.ps is None:
            self.start_worker()
        else:
            pass