from typing import List
from Allocator import Allocator
from Hole import Hole
from Segment import Segment

class FirstFitAllocator(Allocator):
    
    def choose_hole(self, segment : Segment, hole_list : List) -> Hole:
        """Allocate the first hole that is big enough"""

        for hole in hole_list:
            suitable_size = segment.get_size() == hole.get_size()
            if suitable_size:
                return hole

        # No suitable hole found
        return None