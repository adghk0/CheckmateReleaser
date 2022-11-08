
from .connector import Connector
from abc import abstractmethod

import pymysql

class Database(Connector):
    """ 데이터베이스 연결 인터페이스 클래스 입니다.
    """
    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def query(self, query: str, arguments: list):
        pass

    @abstractmethod
    def select(self, table: str, columns: list=[], conditions: dict={}):
        pass

    @abstractmethod
    def insert(self, table: str, values: dict):
        pass

    @abstractmethod
    def update(self, table: str, conditions: dict, datas: dict):
        pass

    @abstractmethod
    def delete(self, table: str, conditions: dict):
        pass
    
    def check(self, table: str, conditions: dict):
        return not self.select(table, ['1'], conditions)[0] == 0

    def insert_or_select(self, table: str, columns: list, datas: dict):
        if not self.check(table, datas):
            self.insert(table, datas)
        return self.select(table, columns, datas)


class MySQLDatabase(Database):
    def __init__(self, **kwargs):
        self.db = None
        self.connect(**kwargs)

    def connect(self, **kwargs) -> bool:
        self.address = kwargs['address']
        self.port = int(kwargs['port'])
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.encoding = kwargs['encoding'] if 'encoding' in kwargs else 'utf8mb4' 
        self.database = kwargs['database']
        self.db = pymysql.connect( 
            host=self.address,
            port=self.port,
            user=self.user,
            password=self.password,
            charset=self.encoding,
            database=self.database
        )

    def close(self) -> bool:
        self.db.close()

    def commit(self):
        self.db.commit()

    def query(self, query: str, arguments: list=[]):
        result = None
        with self.db.cursor() as cur:
            if arguments:
                # print(query)
                aff = cur.execute(query, arguments)
            else:
                aff = cur.execute(query)
            result = (aff, cur.fetchall())
        return result

    def select(self, table: str, columns: list=[], conditions: dict={}):
        if not columns:
            columns = ['*']
        s_columns = ', '.join(columns)

        s_conditions = ('WHERE ' + ' AND '.join([f'`{c}`=%s' for c in conditions.keys()])) if conditions else ''
        
        sql = f'''
            SELECT {s_columns}
            FROM `{table}`
            {s_conditions};
        '''
        return self.query(sql, list(conditions.values()))

    def insert(self, table: str, datas: dict):
        s_columns = ', '.join(f'`{c}`' for c in datas.keys())
        s_value_pos = ', '.join(['%s' for v in datas.values()])
        sql = f'''
            INSERT INTO `{table}`
            ({s_columns})
            VALUES ({s_value_pos});
        '''
        return self.query(sql, list(datas.values()))

    def update(self, table: str, conditions: dict, datas: dict):
        s_columns = ', '.join([f'`{c}`=%s' for c in datas.keys()])
        s_conditions = ('WHERE ' + ' AND '.join([f'`{c}`=%s' for c in conditions.keys()])) if conditions else ''
        
        sql = f'''
            UPDATE `{table}`
            SET {s_columns}
            {s_conditions};
        '''
        return self.query(sql, [*datas.values(), *conditions.values()])

    def delete(self, table: str, conditions: dict):
        s_conditions = ('WHERE ' + ' AND '.join([f'`{c}`=%s' for c in conditions.keys()])) if conditions else ''
        
        sql = f'''
            DELETE FROM `{table}`
            {s_conditions};
        '''
        return self.query(sql, list(conditions.values()))