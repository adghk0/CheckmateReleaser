""" 작업 기본 가상 클래스
"""

from abc import ABC, abstractmethod

class Work(ABC):    
    @abstractmethod
    def execute(self):
        pass
