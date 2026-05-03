from SegmentOfProcess import SegmentOfProcess

class Process:
    def __init__(self, name, num_of_segments):
        self.name = name
        self.num_of_segments = num_of_segments
        self.start_address = None
        self.total_size = None
        self.segments = []
    
    def add_segment(self, segment : SegmentOfProcess):
        self.segments.append(segment)
        self.total_size += segment.get_size()
    
    def get_name(self):
        return self.get_name()

    def get_num_of_segments(self):
        return self.num_of_segments

    def get_segments(self):
        return self.segments
    
    def get_total_size(self):
        return self.total_size
    