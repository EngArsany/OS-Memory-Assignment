from src.Hole import Hole
from src.Segment import Segment
from src.Process import Process
from typing import List

class Memory:    
    def __init__(self, total_size, holes : List):
        self.total_size = total_size
        self.memory = {}
        self.holes = holes

        for hole in holes:
            self.add_hole(hole)
        
        self.__initialize_invalid_blocks__()

    
    def add_hole(self, hole : Hole):
        self.memory[hole.get_starting_address()] = hole
    
    def __add_segment__(self, segment : Segment):
        pass # Add code

    def __add_invalid_block__(self, starting_address):
        self.memory[starting_address] = 

    def __initialize_invalid_blocks__(self):
        for start_address, hole in self.memory:
            new_address = hole.get_size() + start_address


    def add_process(self, process : Process):
        pass # add code

    def draw_memory(self):
        pass # add code
