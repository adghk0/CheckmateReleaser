
from .connector import Connector
from .explorer import Explorer
from abc import abstractmethod

class FileConnector(Connector):
    """ 파일 연결 인터페이스 클래스 입니다.
    """
    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str) -> bool:
        pass

    @abstractmethod
    def download_file(self, remote_path: str, local_path: str) -> bool:
        pass

    @abstractmethod
    def upload_dir(self, local_path: str, remote_path: str) -> int:
        pass

    @abstractmethod
    def download_dir(self, remote_path: str, local_path: str) -> int:
        pass


class FileExplorer(Explorer):
    """ 파일 구조 탐색 클래스 입니다.
    """
    @abstractmethod
    def listdir(self, remote_path: str) -> list:
        pass
    
    @abstractmethod
    def exists(self, remote_path: str) -> bool:
        pass
    
    @abstractmethod
    def mkdir(self, remote_path: str) -> bool:
        pass
    
    @abstractmethod
    def isdir(self, remote_path: str) -> bool:
        pass

    @abstractmethod
    def isfile(self, remote_path: str) -> bool:
        pass

    """
    TODO : 구현 대상 메소드
    os.path.getatime
    os.path.getctime
    os.path.getmtime
    os.path.getsize
    os.path.isabs
    os.path.islink
    os.path.ismount
    os.path.lexists
    """
