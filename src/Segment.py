from abc import ABC, abstractmethod

class Segment(ABC):
    def __init__(self, name, size, starting_address = None):
        self.name = name
        self.size = size
        self.starting_address = starting_address

    def print_info(self):
        print(self.name, ": ")
        print(" Starting Address: ", self.starting_address)
        print(" Size: ", self.size)


    def get_starting_address(self):
        return self.starting_address
    
    def get_name(self):
        return self.name

    def get_size(self):
        return self.size