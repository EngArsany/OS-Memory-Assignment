from Hole import Hole
from Layout import Layout
from Process import Process
from Segment import Segment


def user_input():
    print("User Input")
    # Memory


    # Holes

    # Method

    # Process






def main():
    # Given Test case
    total_memory = 1000
    hole_1 = Hole("H1", 0, 300)
    hole_2 = Hole("H2", 400, 250)
    hole_3 = Hole("H3", 700, 200)

    algorithm = "first-fit"

    # Input 1
    operation = "allocation"
    process_1 = Process("P1", 3)
    process_1.add_segment(Segment("Code", 100))
    process_1.add_segment(Segment("Data", 120))
    process_1.add_segment(Segment("Stack", 90))

    # allocate(process_1)
    # Layout.print_layout()
    


    # Input 2
    operation = "allocation"
    process_2 = Process("P2", 2)
    process_2.add_segment(Segment("Code", 200))
    process_2.add_segment(Segment("Data", 40))


    # Input 3
    operation = "allocation"
    process_3 = Process("P3", 3)
    process_3.add_segment(Segment("Code", 120))
    process_3.add_segment(Segment("Data", 50))

    # Input 4
    operation = "de-allocation" # Process 1
    

    # Input 5
    operation = "allocation"
    process_4 = Process("P4", 3)
    process_4.add_segment(Segment("Code", 230))
    process_4.add_segment(Segment("Data", 40))




