import copy
from abc import ABC, abstractmethod
from typing import List
from Process import Process
from Memory import Memory
from Segment import Segment
from Hole import Hole

class Allocator(ABC):
    def __init__(self, name, memory : Memory):
        self.name = name
        self.memory = memory
    
    def allocate(self, process : Process):
        hole_list = self.memory.get_holes()
        spare_memory_block = copy.deepcopy(self.memory.get_memory_block())

        segments = process.get_segments()
        for segment in segments:
            chosen_hole = self.choose_hole(segment, hole_list)
            # print(segment.print_info())
            if chosen_hole is None:
                self.memory.set_memory_block(spare_memory_block)
                print(f"== Process {process.get_name()} does not fit! ==")
                return
                
            self.allocate_segment_to_hole(segment, chosen_hole)
            self.memory.add_segment(segment)
        
        self.memory.add_process_to_list(process)

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

    def deallocate(self, process : Process):
        if process not in self.memory.get_process_list():
            print(f"Process {process.get_name()} is not in memory")
        
        segments = process.get_segments()
        for segment in segments:
            substituting_hole = Hole(None, segment.get_starting_address(), segment.get_size())
            self.memory.add_segment(substituting_hole) # Overwrites the SegmentOfProcess in the address

        print("== De-Allocation Successful ==")

