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
        import copy

        # Work on a copy of memory state
        trial_memory_block = dict(self.memory.get_memory_block())
        trial_holes = [copy.copy(h) for h in self.memory.get_holes()]

        for segment in process.get_segments():
            chosen_hole = self.choose_hole(segment, trial_holes)
            if chosen_hole is None:
                print(f"== Process {process.get_name()} does not fit! ==")
                return  # Live memory untouched

            # Apply allocation to trial state
            seg_addr = chosen_hole.get_starting_address()
            segment.set_starting_address(seg_addr)

            del trial_memory_block[seg_addr]
            chosen_hole.set_starting_address(seg_addr + segment.get_size())
            chosen_hole.shrink_by(segment.get_size())

            if chosen_hole.get_size() > 0:
                trial_memory_block[chosen_hole.get_starting_address()] = chosen_hole
            else:
                trial_holes.remove(chosen_hole)

            trial_memory_block[segment.get_starting_address()] = segment

        # All segments fit — commit trial state to live memory
        self.memory.set_memory_block(dict(sorted(trial_memory_block.items())))
        self.memory.set_holes(trial_holes)
        self.memory._starting_addresses = sorted(trial_memory_block.keys())
        self.memory.add_process_to_list(process)

    def deallocate(self, process: Process):
        if process not in self.memory.get_process_list():
            print(f"Process {process.get_name()} is not in memory")
            return

        # Collect freed address ranges
        freed_regions = [
            (seg.get_starting_address(), seg.get_size())
            for seg in self.memory.get_memory_block().values()
            if isinstance(seg, SegmentOfProcess) and seg.get_process() == process
        ]

        # Remove process segments and all invalid blocks from memory block
        addrs_to_remove = [
            addr for addr, seg in self.memory.get_memory_block().items()
            if (isinstance(seg, SegmentOfProcess) and seg.get_process() == process)
            or isinstance(seg, InvalidBlock)
        ]
        for addr in addrs_to_remove:
            del self.memory.get_memory_block()[addr]

        self.memory.processes.remove(process)

        # Convert freed regions into holes, merging with any adjacent existing hole
        for start, size in freed_regions:
            new_hole = Hole(size=size, starting_address=start)
            self.memory.get_memory_block()[start] = new_hole
            self.memory.get_holes().append(new_hole)

        # Merge all contiguous holes in one pass
        self.memory._merge_contiguous_holes()

        # Remove any hole entries from _memory_block that were consumed by merging
        live_hole_addrs = {h.get_starting_address() for h in self.memory.get_holes()}
        for addr in list(self.memory.get_memory_block().keys()):
            seg = self.memory.get_memory_block()[addr]
            if isinstance(seg, Hole) and addr not in live_hole_addrs:
                del self.memory.get_memory_block()[addr]

        # Rebuild _starting_addresses from current memory block
        self.memory._starting_addresses = sorted(self.memory.get_memory_block().keys())

        # Regenerate invalid blocks for gaps between remaining segments
        self.memory._initialize_invalid_blocks()
        self.memory._sort_segments_by_address()

        print("== De-Allocation Successful ==")