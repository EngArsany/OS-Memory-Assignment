from Segment import Segment
# import Process

class SegmentOfProcess(Segment):
    def __init__(self, type, starting_address, size, process):
        super().__init__(type, size, starting_address)
        self.process = process
    
    # Override
    def print_info(self):
        print(self.process.get_name())
        print(self.name, ": ", self.size)