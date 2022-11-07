from abc import ABC, abstractmethod

class Work(ABC):    
    @abstractmethod
    def execute(self):
        pass
