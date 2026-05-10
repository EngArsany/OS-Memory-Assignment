from Allocator import Allocator
from typing import List
from Segment import Segment
from Hole import Hole
from Memory import Memory

class BestFitAllocator(Allocator):
    def __init__(self, name, memory : Memory):
        super().__init__(name, memory)

    def choose_hole(self, segment: Segment, hole_list: List) -> Hole:
        segment_size = segment.get_size()
        best_hole = None
        best_fragment = float('inf')
        
        for hole in hole_list:
            if hole.get_size() >= segment_size:
                fragment = hole.get_size() - segment_size
                if fragment < best_fragment:
                    best_fragment = fragment
                    best_hole = hole
        
        return best_hole