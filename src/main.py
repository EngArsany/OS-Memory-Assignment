# main.py
from Memory import Memory
from Hole import Hole
from FirstFitAllocator import FirstFitAllocator
from gui import MemoryGUI

def main():
    # Initialize memory with test case
    total_memory = 1000
    holes = [Hole(300, "H1", 0), Hole(250, "H2", 400), Hole(200, "H3", 700)]
    memory = Memory(total_memory, holes)
    
    # Create default allocator
    allocator = FirstFitAllocator("First-Fit Allocator", memory)
    
    # Launch GUI
    gui = MemoryGUI(memory, allocator)
    gui.run()

if __name__ == "__main__":
    main()