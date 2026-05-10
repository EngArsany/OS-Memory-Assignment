import copy
from abc import ABC, abstractmethod
from typing import List
from Process import Process
from Memory import Memory
from Segment import Segment
from Hole import Hole
from InvalidBlock import InvalidBlock
from SegmentOfProcess import SegmentOfProcess

class Allocator(ABC):
    def __init__(self, name, memory : Memory):
        self.name = name
        self.memory = memory

    # Helper Methods
    @abstractmethod
    def choose_hole(self, segment : Segment, hole_list : List) -> Hole:
        pass

    def allocate_segment_to_hole(self, segment : Segment, hole : Hole):
        hole_starting_address = hole.get_starting_address()
        segment_size = segment.get_size()

        segment.set_starting_address(hole_starting_address)

        # Remove the hole from memory block at its old address
        if hole_starting_address in self.memory.get_memory_block():
            del self.memory.get_memory_block()[hole_starting_address]

        # Update Hole position and size
        hole.set_starting_address(hole_starting_address + segment_size)
        hole.shrink_by(segment_size)

        # Add the updated hole back to memory block if it still has size
        if hole.get_size() > 0:
            self.memory.get_memory_block()[hole.get_starting_address()] = hole
        else:
            self.memory.get_holes().remove(hole)

    def _is_hole(self, segment : Segment) -> bool:
        return isinstance(segment, Hole)

    # Core Logic
    def allocate(self, process: Process):
        backup_memory = copy.deepcopy(self.memory.get_memory_block())
        backup_holes = copy.deepcopy(self.memory.get_holes())
        backup_addresses = copy.deepcopy(self.memory._starting_addresses)

        segments = process.get_segments()
        for segment in segments:
            chosen_hole = self.choose_hole(segment, self.memory.get_holes())
            if chosen_hole is None:
                self.memory.set_memory_block(backup_memory)
                self.memory.set_holes(backup_holes)
                self.memory._starting_addresses = backup_addresses
                print(f"== Process {process.get_name()} does not fit! ==")
                return
                
            self.allocate_segment_to_hole(segment, chosen_hole)
            self.memory.add_segment(segment)
        
        self.memory.add_process_to_list(process)

    def deallocate(self, process: Process):
        if process not in self.memory.get_process_list():
            print(f"Process {process.get_name()} is not in memory")
            return

        # Remove all segments belonging to this process
        addrs_to_remove = [
            addr for addr, seg in self.memory.get_memory_block().items()
            if isinstance(seg, SegmentOfProcess) and seg.get_process() == process
        ]
        for addr in addrs_to_remove:
            del self.memory.get_memory_block()[addr]

        self.memory.processes.remove(process)

        # Surviving segments: remaining process segments + invalid blocks
        # Holes are discarded and rebuilt from scratch below
        surviving_segments = [
            seg for seg in self.memory.get_memory_block().values()
            if not isinstance(seg, Hole)
        ]

        # Rebuild memory state from scratch
        self.memory._memory_block.clear()
        self.memory._holes.clear()
        self.memory._starting_addresses.clear()

        for seg in surviving_segments:
            self.memory._memory_block[seg.get_starting_address()] = seg
            self.memory._starting_addresses.append(seg.get_starting_address())

        self.memory._starting_addresses.sort()

        # Scan address space for free regions; invalid blocks count as occupied
        occupied = sorted(
            [(seg.get_starting_address(), seg.get_size()) for seg in surviving_segments],
            key=lambda x: x[0]
        )

        free_regions = []
        cursor = 0
        for start, size in occupied:
            if cursor < start:
                free_regions.append((cursor, start - cursor))
            cursor = start + size
        if cursor < self.memory.total_size:
            free_regions.append((cursor, self.memory.total_size - cursor))

        # Create holes for free regions; contiguous ones merge automatically in _initialize_holes
        holes = [
            Hole(size=size, name=f"H_{start}", starting_address=start)
            for start, size in free_regions
        ]
        self.memory._initialize_holes(holes)
        self.memory._initialize_invalid_blocks()
        self.memory._sort_segments_by_address()

        print("== De-Allocation Successful ==")