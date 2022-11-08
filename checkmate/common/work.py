""" 작업 기본 가상 클래스
"""
import time

from abc import ABC, abstractmethod


class Work(ABC):    
    @abstractmethod
    def execute(self):
        pass


class Delay(Work):
    def __init__(self, seconds: int):
        self.seconds = seconds
    
    def execute(self):
        time.sleep(self.seconds)

