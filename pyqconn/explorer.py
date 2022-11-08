""" 탐색 인터페이스 정의
"""

from typing import Any

from .connector import Connector
from abc import abstractmethod


class Explorer(Connector):
    """ 기본 구조 탐색 클래스 입니다.
    """

    @abstractmethod
    def current(self) -> Any:
        """ 현재 탐색중인 항목을 반환합니다.
        """
        pass

    @abstractmethod
    def explore(self, target: Any):
        """ 입력받은 항목을 탐색합니다.
        """
        pass

