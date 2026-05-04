from typing import List
from operator import attrgetter
from Hole import Hole
from Segment import Segment
from InvalidBlock import InvalidBlock
from Process import Process


class Memory:
    """Manages memory allocation and tracks memory blocks (holes, segments, invalid blocks)."""
    
    def __init__(self, total_size: int, holes: List[Hole]):
        self.total_size = total_size
        self._memory_block = {}
        self._holes = []
        self._starting_addresses = []
        
        self._initialize_holes(holes)
        self._initialize_invalid_blocks()
        self._sort_segments_by_address()
    
    def _initialize_holes(self, holes: List[Hole]) -> None:
        """Initialize holes and their starting addresses."""
        self._holes = sorted(holes, key=attrgetter('starting_address'))
        
        for hole in self._holes:
            self.add_segment(hole)
            self._starting_addresses.append(hole.starting_address)
        
        self._starting_addresses.sort()
    
    def add_segment(self, segment: Segment) -> None:
        """Add any segment (Hole, InvalidBlock, or regular Segment) to memory."""
        self._memory_block[segment.starting_address] = segment
    
    def _add_segments(self, segments: List[Segment]) -> None:
        """Add multiple segments to memory."""
        for segment in segments:
            self._memory_block[segment.starting_address] = segment
            self._starting_addresses.append(segment.starting_address)
        
        self._starting_addresses.sort()
    
    def _initialize_invalid_blocks(self) -> None:
        """Create invalid blocks for gaps between valid memory segments."""
        invalid_blocks = []
        
        for index, (start_address, segment) in enumerate(self._memory_block.items()):
            if self._is_last_segment(index):
                continue
                
            next_address = self._starting_addresses[index + 1]
            gap = self._calculate_gap_between_segments(segment, next_address)
            
            if gap.size > 0:
                invalid_blocks.append(gap)
        
        self._add_segments(invalid_blocks)
    
    def _is_last_segment(self, index: int) -> bool:
        """Check if the given index refers to the last memory segment."""
        return index + 1 >= len(self._starting_addresses)
    
    def _calculate_gap_between_segments(self, current_segment: Segment, next_address: int) -> InvalidBlock:
        """Calculate the InvalidBlock between current segment and the next one."""
        end_of_current = current_segment.starting_address + current_segment.size
        gap_size = next_address - end_of_current
        
        if gap_size <= 0:
            return InvalidBlock("empty", 0, 0)
            
        return InvalidBlock(
            name=f"I_{current_segment.starting_address}",
            starting_address=end_of_current,
            size=gap_size
        )
    
    def _sort_segments_by_address(self) -> None:
        """Sort memory segments by their starting addresses."""
        self._memory_block = dict(sorted(self._memory_block.items()))
    
    def add_process(self, process: Process) -> None:
        """Add a process to memory (implementation pending)."""
        pass
    
    def draw_memory(self) -> None:
        """Draw memory visualization (implementation pending)."""
        pass
    
    def print_memory(self) -> None:
        """Print all memory segments information."""
        for segment in self._memory_block.values():
            segment.print_info()
            print()
    
    def get_memory_block(self):
        return self._memory_block
    
    def get_holes(self):
        return self._holes