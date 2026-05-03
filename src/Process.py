from Memory.Segment import Segment

class Process:
    def __init__(self, name, num_of_segments):
        self.name = name
        self.num_of_segments = num_of_segments
        self.start_address = None
        self.total_size = None
        self.segments = []
    
    def add_segment(self, segment):
        self.segments.append(segment)