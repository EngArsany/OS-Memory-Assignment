from Allocator import Allocator
from Hole import Hole

class FirstFitAllocator(Allocator):

    def choose_hole(self, process, memory):
        """Allocate the first hole that is big enough"""