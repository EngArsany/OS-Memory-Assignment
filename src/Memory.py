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

    def __add_invalid_block__(self, block):
        self.memory_block[block.get_starting_address] = block

    def __initialize_invalid_blocks__(self):
        for index, (start_address, hole) in self.memory_block:
            new_address = hole.get_size() + start_address
            next_address = self.starting_addresses[index+1] if self.starting_addresses[index+1] else 0

            block_size = next_address - new_address
            invalid_block = InvalidBlock("B{index}", new_address, block_size)
            self.__add_invalid_block__(invalid_block)

    def add_process(self, process : Process):
        pass # add code

    def draw_memory(self):
        pass # add code

    def print_memory(self):
        for segment in self.memory_block:
            segment.print_info()