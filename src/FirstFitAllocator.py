from typing import List
from Allocator import Allocator
from Hole import Hole
from Segment import Segment
from Memory import Memory

class FirstFitAllocator(Allocator):
    def __init__(self, name, memory : Memory):
        super().__init__(name, memory)

    def choose_hole(self, segment : Segment, hole_list : List) -> Hole:
        """Allocate the first hole that is big enough"""

        for hole in hole_list:
            suitable_size = segment.get_size() == hole.get_size()
            if suitable_size:
                return hole

        # No suitable hole found
        return None