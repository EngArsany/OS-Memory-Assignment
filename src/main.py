from Hole import Hole
from Layout import Layout
from Process import Process
from Segment import Segment
from Memory import Memory
from FirstFitAllocator import FirstFitAllocator
from BestFitAllocator import BestFitAllocator
from SegmentOfProcess import SegmentOfProcess

def user_input():
    print("User Input")
    # Memory


    # Holes

    # Method

    # Process

def main():
    # Given Test case
    total_memory = 1000
    holes = [Hole(300, "H1", 0), Hole(250, "H2", 400), Hole(200, "H3", 700)]
    memory = Memory(total_memory, holes)
    print("Hello world")
    memory.print_memory()

    algorithm = "first-fit"
    allocator = FirstFitAllocator("First-Fit Allocator", memory) if algorithm == "first-fit" else BestFitAllocator("Best-Fit Allocator")

    # Input 1
    operation = "allocation"
    process_1 = Process("P1", 3)
    process_1.add_segment("Code", 100)
    process_1.add_segment("Data", 120)
    process_1.add_segment("Stack", 90)
    allocator.allocate(process_1)
    memory.print_memory()

    # allocate(process_1)
    # Layout.print_layout()
    


    # Input 2
    # operation = "allocation"
    # process_2 = Process("P2", 2)
    # process_2.add_segment(Segment("Code", 200))
    # process_2.add_segment(Segment("Data", 40))


    # # Input 3
    # operation = "allocation"
    # process_3 = Process("P3", 3)
    # process_3.add_segment(Segment("Code", 120))
    # process_3.add_segment(Segment("Data", 50))

    # # Input 4
    # operation = "de-allocation" # Process 1
    

    # # Input 5
    # operation = "allocation"
    # process_4 = Process("P4", 3)
    # process_4.add_segment(Segment("Code", 230))
    # process_4.add_segment(Segment("Data", 40))




main()