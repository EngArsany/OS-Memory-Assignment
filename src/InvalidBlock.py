from Segment import Segment

class InvalidBlock(Segment):
    _counter = 0

    def __init__(self, name, starting_address, size):
        super().__init__(name, size, starting_address)

    def get_prefix(self):
        return "I"