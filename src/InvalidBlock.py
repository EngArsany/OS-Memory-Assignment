from Segment import Segment

class InvalidBlock(Segment):
    _counter = 0

    def __init__(self, size, name, starting_address):
        super().__init__(name, size, starting_address)

    def get_prefix(self):
        return "I"