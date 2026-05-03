from abc import ABC, abstractmethod
from Process import Process

class Allocator(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def allocate(self, process : Process):
        pass

