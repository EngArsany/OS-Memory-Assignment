import copy
from abc import ABC, abstractmethod
from typing import List
from Process import Process
from Memory import Memory
from Segment import Segment
from Hole import Hole

class Allocator(ABC):
    def __init__(self, name):
        self.name = name
    
    def allocate(self, process : Process, memory : Memory):
        hole_list = memory.get_holes()
        spare_memory_block = copy.deepcopy(memory_block)
        
        segments = process.get_segments()
        for segment in segments:
            chosen_hole = self.choose_hole(segment, hole_list)
            if chosen_hole is None:
                memory_block = spare_memory_block
                print(f"== Process {process.get_name()} does not fit! ==")
                return
                
            self.allocate_segment_to_hole(segment, chosen_hole)
            memory.add_segment(segment)

    @abstractmethod
    def choose_hole(self, segment : Segment, hole_list : List) -> Hole:
        pass

    def allocate_segment_to_hole(self, segment : Segment, hole : Hole):
        hole_starting_address = hole.get_starting_address()
        segment_size = segment.get_size()

        segment.set_starting_address(hole_starting_address)
        # Add the segment to the memory block  

        hole.set_starting_address(hole_starting_address + segment_size)
        hole.shrink_by(segment_size)

    def _is_hole(self, segment : Segment) -> bool:
        return isinstance(segment, Hole)