from Segment import Segment

class Hole(Segment):
    _counter = 0

    def __init__(self, name, starting_address, size):
        super().__init__(name, size, starting_address)
    
    def get_prefix(self):
        return "H"

    def set_size(self, newSize):
        self.size = newSize
    
    def shrink_by(self, size):
        self.size -= size
    
    def grow_by(self, size):
        self.size += size