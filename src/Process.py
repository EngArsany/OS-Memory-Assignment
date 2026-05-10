from SegmentOfProcess import SegmentOfProcess

class Process:
    def __init__(self, name, num_of_segments):
        self.name = name
        self.num_of_segments = num_of_segments
        self.start_address = None
        self.total_size = 0
        self.segments = []
    
    def add_segment(self, data_type : str, size : int):
        segment = SegmentOfProcess(size, self, data_type)
        self.segments.append(segment)
        self.total_size += segment.get_size()
    
    def get_name(self):
        return self.name

    def get_num_of_segments(self):
        return self.num_of_segments

    def get_segments(self):
        return self.segments
    
    def get_total_size(self):
        return self.total_size
    