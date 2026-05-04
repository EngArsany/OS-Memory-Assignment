from Allocator import Allocator
from Hole import Hole
from Segment import Segment

class FirstFitAllocator(Allocator):
    
    def choose_hole(self, segment : Segment, memory_block : dict) -> Hole:
        """Allocate the first hole that is big enough"""
        for potential_hole in memory_block.values():
            suitable_size = segment.get_size() == potential_hole.get_size()
            if self._is_hole(potential_hole) and suitable_size:
                return potential_hole
        
        # No suitable hole found
        return None