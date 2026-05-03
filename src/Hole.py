from src.Segment import Segment

class Hole(Segment):
    def __init__(self, name, starting_address, size):
        self.name = name
        self.starting_address = starting_address
        self.size = size

    def get_starting_address(self):
        return self.starting_address
    
    def get_name(self):
        return self.name

    def get_size(self):
        return self.size