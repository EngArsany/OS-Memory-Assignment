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
        self.processes = []
        self._starting_addresses = []
        
        self._initialize_holes(holes)
        self._initialize_invalid_blocks()
        self._sort_segments_by_address()
    
    # Global Methods
    def add_process_to_list(self, process: Process) -> None:
        """Add a process to memory processes list."""
        self.processes.append(process)
    
    def add_segment(self, segment: Segment) -> None:
        """Add any segment (Hole, InvalidBlock, or regular Segment) to memory."""
        self._memory_block[segment.starting_address] = segment
        self._sort_segments_by_address()

    # Helper Methods
    def _initialize_holes(self, holes: List[Hole]) -> None:
        """Initialize holes and their starting addresses."""
        self._holes = sorted(holes, key=attrgetter('starting_address'))
        for hole in self._holes:
            self.add_segment(hole)
            self._starting_addresses.append(hole.starting_address)
        
        self._starting_addresses.sort()
        self._merge_contiguous_holes()

    def _initialize_invalid_blocks(self):
        for i in range(len(self._starting_addresses) - 1):
            current = self._memory_block[self._starting_addresses[i]]
            next_addr = self._starting_addresses[i + 1]
            gap = self._calculate_gap_between_segments(current, next_addr)
            if gap.size > 0:
                self.add_segment(gap)

    def _add_segments(self, segments: List[Segment]) -> None:
        """Add multiple segments to memory."""
        for segment in segments:
            self._memory_block[segment.starting_address] = segment
            self._starting_addresses.append(segment.starting_address)
        
        self._starting_addresses.sort()
        self._merge_contiguous_holes()

    def _merge_contiguous_holes(self):
        if len(self._holes) <= 1:
            return
        
        i = 0
        while i < len(self._holes) - 1:
            current = self._holes[i]
            next_hole = self._holes[i + 1]
            
            if current.get_ending_address() >= next_hole.get_starting_address():
                self._merge_two_holes(current, next_hole)
                # Don't increment i - check new merge
            else:
                i += 1
            
    def _merge_two_holes(self, hole_1 : Hole, hole_2 : Hole):
        new_starting_address = min(hole_1.get_starting_address(), hole_2.get_starting_address())
        hole_1.set_starting_address(new_starting_address)

        new_size = hole_1.get_size() + hole_2.get_size()    
        hole_1.set_size(new_size)

        for key, value in (self._memory_block.items()):
            if value == hole_2:
                del self._memory_block[key]
                break

        if hole_2 in self._holes:
            self._holes.remove(hole_2)

    def _is_last_segment(self, index: int) -> bool:
        """Check if the given index refers to the last memory segment."""
        return index + 1 >= len(self._starting_addresses)
    
    def _calculate_gap_between_segments(self, current_segment: Segment, next_address: int) -> InvalidBlock:
        """Calculate the InvalidBlock between current segment and the next one."""
        end_of_current = current_segment.starting_address + current_segment.size
        gap_size = next_address - end_of_current
        
        if gap_size <= 0:
            return InvalidBlock(0, "empty", 0)
            
        return InvalidBlock(
            name=f"I_{current_segment.starting_address}",
            starting_address=end_of_current,
            size=gap_size
        )
    
    def _sort_segments_by_address(self) -> None:
        """Sort memory segments by their starting addresses."""
        self._memory_block = dict(sorted(self._memory_block.items()))
      
    # Representation
    def set_memory_block(self, memory_block : dict):
        self.memory_block = memory_block

    def set_holes(self, holes : List):
        self._holes = holes

    def draw_memory(self) -> None:
        """Draw memory visualization (implementation pending)."""
        pass
    
    def print_memory(self) -> None:
        """Print all memory segments information."""
        for segment in self._memory_block.values():
            segment.print_info()
            print()
    
    # Setters & Getters
    def get_memory_block(self):
        return self._memory_block
    
    def get_holes(self):
        return self._holes
    
    def get_process_list(self):
        return self.processes
    
