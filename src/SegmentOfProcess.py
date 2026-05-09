from Segment import Segment

class SegmentOfProcess(Segment):
    _counter = 0

    def __init__(self, size, name, starting_address, process, data_type):
        super().__init__(size, name, starting_address)
        self.process = process
        self.data_type = data_type
    
    # Override
    def print_info(self):
        print(self.process.get_name())
        print(self.name, ": ", self.size)

    def get_prefix(self):
        return "S"
    
    def get_process(self):
        return self.process

    def get_data_type(self):
        return self.data_type