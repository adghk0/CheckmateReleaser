""" 연결 인터페이스 정의
"""

from abc import ABC, abstractmethod

class Connector(ABC):
    """ 인터페이스 클래스 입니다.
    """

    @abstractmethod
    def __init__(self, **kwargs):
        self.connect(**kwargs)

    @abstractmethod
    def connect(self, **kwargs) -> bool:
        pass

    @abstractmethod
    def close(self) -> bool:
        pass


