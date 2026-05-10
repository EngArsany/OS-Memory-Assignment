from abc import ABC, abstractmethod

class Segment(ABC):
    def __init__(self, size = 0, name = None, starting_address = 0):
        self.size = size
        self.starting_address = starting_address
        self.ending_address = self.starting_address + self.size
        self.name = name

        if self.name is None:
            self.__class__._counter += 1
            self.name = f"{self.get_prefix()}{self.__class__._counter}"

    def print_info(self):
        if self.name == None:
            self.name = "hole naming error"
        else:
            print(self.name, ": ")
            
        print(" Starting Address: ", self.starting_address)
        print(" Size: ", self.size)

    # Getters and Setters
    @abstractmethod
    def get_prefix(self):
        pass

    def get_starting_address(self):
        return self.starting_address

    def set_starting_address(self, address):
        self.starting_address = address

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size
    
    def get_ending_address(self):
        return self.ending_address