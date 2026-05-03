from Hole import Hole
from Segment import Segment
from InvalidBlock import InvalidBlock
from Process import Process
from typing import List
from operator import attrgetter

class Memory:    
    def __init__(self, total_size, holes : List):
        self.total_size = total_size
        self.memory_block = {}
        self.holes = holes
        self.starting_addresses = []

        for hole in holes:
            self.add_hole(hole)
            self.starting_addresses.append(hole.get_starting_address())
        
        self.holes = sorted(holes, key=attrgetter('starting_address'))
        self.starting_addresses = sorted(self.starting_addresses)

        self.__initialize_invalid_blocks__()

    
    def add_hole(self, hole : Hole):
        self.memory_block[hole.get_starting_address()] = hole
    
    def __add_segment__(self, segment : Segment):
        pass # Add code

    def __add_invalid_blocks__(self, block_list):
        for block in block_list:
            self.memory_block[block.get_starting_address] = block
            self.starting_addresses.append(block.get_starting_address())

        self.starting_addresses = sorted(self.starting_addresses)


    def __initialize_invalid_blocks__(self):
        invalid_block_list = []
        for index, (start_address, hole) in enumerate(self.memory_block.items()):
            new_address = hole.get_size() + start_address
            
            # Skip if this is the last block
            if index + 1 >= len(self.starting_addresses):
                continue
                
            next_address = self.starting_addresses[index + 1]
            block_size = next_address - new_address
            
            # Only create invalid block if size is positive
            if block_size > 0:
                invalid_block = InvalidBlock(f"B{index}", new_address, block_size)
                invalid_block_list.append(invalid_block)

        self.__add_invalid_blocks__(invalid_block_list)

    def add_process(self, process : Process):
        pass # add code

    def draw_memory(self):
        pass # add code

    def print_memory(self):
        for segment in self.memory_block.values():
            segment.print_info()