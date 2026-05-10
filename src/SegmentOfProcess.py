from Segment import Segment

class SegmentOfProcess(Segment):
    _counter = 0

    def __init__(self, size, process, data_type, name= None, starting_address = 0):
        super().__init__(size, name, starting_address)
        self.process = process
        self.data_type = data_type
    
    # Override
    def print_info(self):
        print(self.process.get_name())
        print(self.data_type, ": ", self.size)
        super().print_info()

    def get_prefix(self):
        return "S"
    
    def get_process(self):
        return self.process

    def get_data_type(self):
        return self.data_type