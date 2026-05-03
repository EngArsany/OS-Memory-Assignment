class Segment:
    def __init__(self, name, size, starting_address = None):
        self.name = name
        self.size = size
        self.starting_adress = starting_address

    def print_info(self):
        print(self.name, ": ", self.size)

    def get_starting_address(self):
        return self.starting_address
    
    def get_name(self):
        return self.name

    def get_size(self):
        return self.size