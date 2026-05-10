# Memory Allocation Simulator — Segmentation

A desktop application simulating dynamic memory allocation using segmentation, built for the CSE 335s Operating Systems course at Ain Shams University.

## Features

- First-Fit and Best-Fit allocation algorithms
- Allocate and deallocate processes with multiple named segments
- Live memory layout drawing updated after every operation
- Segment table displayed for each allocated process
- Warning dialog when a process does not fit in memory
- Configurable total memory size and initial holes

## Project Structure

```
├── main.py                  # Entry point
├── gui.py                   # Tkinter GUI
├── Memory.py                # Memory state manager
├── Allocator.py             # Abstract allocator with shared allocate/deallocate logic
├── FirstFitAllocator.py     # First-Fit hole selection
├── BestFitAllocator.py      # Best-Fit hole selection
├── Process.py               # Process and its segments
├── Segment.py               # Abstract base for all memory blocks
├── SegmentOfProcess.py      # Segment belonging to a process
├── Hole.py                  # Free memory region
└── InvalidBlock.py          # Occupied gap not belonging to any process
```

## Requirements

- Python 3.8+
- Tkinter (included in the standard library)

## Running

```bash
python main.py
```

## Building an Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --paths . main.py
```

The executable will be at `dist/main.exe`. No Python installation is required on the target machine.

## Usage

1. Set total memory size and initial holes (start, size per line) under **Memory Setup**
2. Choose **First-Fit** or **Best-Fit** and click **Apply Setup**
3. Enter a process name and its segments (name, size per line) and click **Allocate**
4. Select a process from the dropdown and click **Deallocate**

## Test Case

| Parameter | Value |
|-----------|-------|
| Total Size | 1000 K |
| H1 | Start=0, Size=300 |
| H2 | Start=400, Size=250 |
| H3 | Start=700, Size=200 |

Operations: Allocate P1 (Code=100, Data=120, Stack=90) → Allocate P2 (Code=200, Data=40) → Allocate P3 (Code=120, Data=50) → Deallocate P1 → Allocate P4 (Code=230, Data=40)
