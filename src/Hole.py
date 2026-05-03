from Segment import Segment

class Hole(Segment):
    def __init__(self, name, starting_address, size):
        super().__init__(name, size, starting_address)