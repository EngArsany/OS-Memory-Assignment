from Allocator import Allocator
from typing import List
from Segment import Segment
from Hole import Hole
from Memory import Memory

class BestFitAllocator(Allocator):
    max_num = 50000

    def __init__(self, name, memory : Memory):
        super().__init__(name, memory)

    def choose_hole(self, segment : Segment, hole_list : List) -> Hole:
        """Allocate the smallest hole that is big enough"""
        segment_size = segment.get_size()
        
        blank_hole = Hole("Blank Hole", -1, self.max_num)
        min_hole = blank_hole
        for hole in hole_list:
            suitable_size = segment_size == hole.get_size()
            if suitable_size:
                min_hole = min(min_hole.get_size(), hole.get_size())

        hole_found = (min_hole.get_size() != self.max_num)
        return min_hole if hole_found else None