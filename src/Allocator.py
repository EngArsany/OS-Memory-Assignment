from abc import ABC, abstractmethod
from Process import Process
from Memory import Memory

class Allocator(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def allocate(self, process : Process, memory : Memory):
        pass

