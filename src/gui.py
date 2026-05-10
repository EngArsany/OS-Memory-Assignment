# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from Memory import Memory
from Process import Process
from FirstFitAllocator import FirstFitAllocator
from BestFitAllocator import BestFitAllocator

class MemoryGUI:
    # Color mapping for different segment types
    COLORS = {
        'SegmentOfProcess': 'lightblue',  # Allocated segments
        'Hole': 'lightgreen',              # Free holes
        'InvalidBlock': 'lightgray'        # Invalid blocks
    }
    
    def __init__(self, memory: Memory, allocator):
        self.memory = memory
        self.allocator = allocator
        
        # Main window
        self.root = tk.Tk()
        self.root.title("Memory Allocation Simulator")
        self.root.geometry("900x700")
        
        # Setup UI sections
        self.setup_memory_display()
        self.setup_control_panel()
        self.setup_legend()
        
        # Initial display
        self.refresh_display()
    
    def setup_memory_display(self):
        """Canvas for color-coded memory visualization"""
        # Main frame for memory display
        display_frame = tk.Frame(self.root)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Title
        tk.Label(display_frame, text="Memory Layout", font=('Arial', 14, 'bold')).pack()
        
        # Canvas with scrollbar
        canvas_frame = tk.Frame(display_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', height=500)
        scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def setup_control_panel(self):
        """Simple control panel with basic operations"""
        panel = tk.Frame(self.root, relief=tk.RAISED, bd=2)
        panel.pack(fill=tk.X, padx=20, pady=10)
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(panel, text="Allocation Algorithm", padx=10, pady=5)
        algo_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.algo_var = tk.StringVar(value="first-fit")
        tk.Radiobutton(algo_frame, text="First-Fit", variable=self.algo_var, 
                      value="first-fit").pack(anchor=tk.W)
        tk.Radiobutton(algo_frame, text="Best-Fit", variable=self.algo_var,
                      value="best-fit").pack(anchor=tk.W)
        
        # Process input
        process_frame = tk.LabelFrame(panel, text="Create Process", padx=10, pady=5)
        process_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        tk.Label(process_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(process_frame, width=10)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        tk.Label(process_frame, text="Segments (type,size):").grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.segments_text = tk.Text(process_frame, height=3, width=25)
        self.segments_text.grid(row=2, column=0, columnspan=2, pady=5)
        tk.Label(process_frame, text="Example: Code,100;Data,120;Stack,90", 
                font=('Arial', 8)).grid(row=3, column=0, columnspan=2)
        
        # Buttons
        button_frame = tk.Frame(panel)
        button_frame.pack(side=tk.LEFT, padx=20, pady=5)
        
        tk.Button(button_frame, text="Allocate", command=self.allocate_process,
                 bg='lightgreen', width=12).pack(pady=5)
        tk.Button(button_frame, text="Deallocate", command=self.deallocate_process,
                 bg='lightcoral', width=12).pack(pady=5)
        tk.Button(button_frame, text="Refresh", command=self.refresh_display,
                 bg='lightblue', width=12).pack(pady=5)
        
        # Process list for deallocation
        list_frame = tk.LabelFrame(panel, text="Running Processes", padx=10, pady=5)
        list_frame.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.process_listbox = tk.Listbox(list_frame, height=5, width=15)
        self.process_listbox.pack()
    
    def setup_legend(self):
        """Color legend for memory blocks"""
        legend_frame = tk.Frame(self.root, relief=tk.GROOVE, bd=1)
        legend_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(legend_frame, text="Legend:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        
        # Legend items
        for segment_type, color in self.COLORS.items():
            type_name = segment_type.replace('Of', ' ') if 'Of' in segment_type else segment_type
            color_box = tk.Label(legend_frame, bg=color, width=3, height=1, relief=tk.SUNKEN)
            color_box.pack(side=tk.LEFT, padx=(10, 2))
            tk.Label(legend_frame, text=type_name).pack(side=tk.LEFT, padx=(0, 15))
    
    def draw_memory_layout(self):
        """Draw color-coded memory blocks"""
        self.canvas.delete("all")
        
        if not self.memory.get_memory_block():
            self.canvas.create_text(200, 250, text="No memory blocks to display", 
                                   font=('Arial', 12), fill='gray')
            return
        
        # Calculate dimensions
        bar_width = 350
        start_x = 50
        start_y = 50
        pixels_per_kb = 400 / self.memory.total_size
        
        y_position = start_y
        for address, segment in self.memory.get_memory_block().items():
            # Get segment type for color
            segment_type = segment.__class__.__name__
            color = self.COLORS.get(segment_type, 'white')
            height = max(segment.get_size() * pixels_per_kb, 15)  # Minimum 15px height
            
            # Draw rectangle
            rect = self.canvas.create_rectangle(
                start_x, y_position,
                start_x + bar_width, y_position + height,
                fill=color, outline='black', width=1
            )
            
            # Add segment info text
            info_text = f"{segment.get_name()}\n{segment.get_size()}KB"
            if segment_type == 'SegmentOfProcess':
                info_text = f"{segment.process.get_name()}:{segment.data_type}\n{segment.get_size()}KB"
            
            self.canvas.create_text(
                start_x + bar_width + 10, y_position + height/2,
                text=info_text, anchor=tk.W, font=('Arial', 9)
            )
            
            # Add address label
            addr_text = f"@{segment.get_starting_address()}"
            self.canvas.create_text(
                start_x - 10, y_position + height/2,
                text=addr_text, anchor=tk.E, font=('Arial', 8), fill='gray'
            )
            
            y_position += height
            
            # Add thin separator line
            if y_position < start_y + 400:
                self.canvas.create_line(
                    start_x - 20, y_position,
                    start_x + bar_width, y_position,
                    fill='lightgray', dash=(2, 2)
                )
        
        # Add total memory indicator
        self.canvas.create_rectangle(
            start_x, start_y - 25,
            start_x + bar_width, start_y - 15,
            fill='black'
        )
        self.canvas.create_text(
            start_x + bar_width/2, start_y - 20,
            text=f"Total Memory: {self.memory.total_size} KB",
            font=('Arial', 10, 'bold')
        )
        
        # Set scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def update_process_list(self):
        """Update the list of running processes"""
        self.process_listbox.delete(0, tk.END)
        for process in self.memory.get_process_list():
            self.process_listbox.insert(tk.END, process.get_name())
    
    def allocate_process(self):
        """Create and allocate a new process"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a process name")
            return
        
        # Parse segments
        segments_text = self.segments_text.get("1.0", tk.END).strip()
        if not segments_text:
            messagebox.showerror("Error", "Please enter at least one segment")
            return
        
        segments = []
        for seg_str in segments_text.split(';'):
            if ',' in seg_str:
                try:
                    seg_type, size = seg_str.split(',')
                    segments.append((seg_type.strip(), int(size.strip())))
                except ValueError:
                    messagebox.showerror("Error", f"Invalid segment format: {seg_str}\nUse: Type,Size")
                    return
            else:
                messagebox.showerror("Error", f"Invalid segment format: {seg_str}\nUse: Type,Size")
                return
        
        # Update allocator based on selected algorithm
        if self.algo_var.get() == "first-fit":
            from FirstFitAllocator import FirstFitAllocator
            self.allocator = FirstFitAllocator("First-Fit", self.memory)
        else:
            from BestFitAllocator import BestFitAllocator
            self.allocator = BestFitAllocator("Best-Fit", self.memory)
        
        # Create and allocate process
        process = Process(name, len(segments))
        for seg_type, size in segments:
            process.add_segment(seg_type, size)
        
        self.allocator.allocate(process)
        
        # Refresh display
        self.refresh_display()
        
        # Show result
        if process in self.memory.get_process_list():
            messagebox.showinfo("Success", f"Process '{name}' allocated successfully!\nAlgorithm: {self.algo_var.get()}")
        else:
            messagebox.showwarning("Failed", f"Process '{name}' could not be allocated - Not enough contiguous memory")
        
        # Clear input
        self.name_entry.delete(0, tk.END)
        self.segments_text.delete("1.0", tk.END)
    
    def deallocate_process(self):
        """Deallocate selected process"""
        selection = self.process_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a process to deallocate")
            return
        
        process_name = self.process_listbox.get(selection[0])
        
        # Find and deallocate process
        for process in self.memory.get_process_list():
            if process.get_name() == process_name:
                self.allocator.deallocate(process)
                self.refresh_display()
                messagebox.showinfo("Success", f"Process '{process_name}' deallocated")
                return
    
    def refresh_display(self):
        """Update all visual elements"""
        self.draw_memory_layout()
        self.update_process_list()
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()