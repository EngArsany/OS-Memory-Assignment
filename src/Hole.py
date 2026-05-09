from Segment import Segment

class Hole(Segment):
    _counter = 0

    def __init__(self, size = 0, name = None, starting_address = 0):
        super().__init__(size, name, starting_address)
    
    def get_prefix(self):
        return "H"

    def set_size(self, new_size):
        self.size = new_size
    
    def shrink_by(self, size):
        self.size -= size
    
    def grow_by(self, size):
        self.size += size