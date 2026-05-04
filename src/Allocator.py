from abc import ABC, abstractmethod
from Process import Process
from Memory import Memory
from Segment import Segment
from Hole import Hole

class Allocator(ABC):
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def choose_hole(self, process : Process, memory : Memory) -> Hole:
        pass

    def allocate_segment_to_hole(self, segment : Segment, hole : Hole, memory_block : dict):
        hole_starting_address = hole.get_starting_address()
        segment_size = segment.get_size()

        segment.set_starting_address(hole_starting_address)
        # Add the segment to the memory block  

        hole.set_starting_address(hole_starting_address + segment_size)
        hole.shrink_by(segment_size)