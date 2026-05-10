import tkinter as tk
from tkinter import ttk, messagebox
from Hole import Hole
from Memory import Memory
from FirstFitAllocator import FirstFitAllocator
from BestFitAllocator import BestFitAllocator
from Process import Process
from SegmentOfProcess import SegmentOfProcess
from InvalidBlock import InvalidBlock


COLORS = {
    "hole":    "#4a90d9",
    "invalid": "#888888",
    "process": ["#e74c3c", "#2ecc71", "#f39c12", "#9b59b6",
                "#1abc9c", "#e67e22", "#3498db", "#e91e63"],
}


class MemoryGUI:
    def __init__(self, memory: Memory, allocator):
        self.memory = memory
        self.allocator = allocator
        self._process_color_map = {}
        self._color_index = 0

        self.root = tk.Tk()
        self.root.title("Memory Allocator")
        self.root.resizable(True, True)

        self._build_ui()

    # ------------------------------------------------------------------ build

    def _build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=8)
        main.grid(sticky="nsew")
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=1)
        main.rowconfigure(0, weight=1)

        self._build_controls(main)
        self._build_display(main)

    def _build_controls(self, parent):
        ctrl = ttk.Frame(parent, padding=4)
        ctrl.grid(row=0, column=0, sticky="ns")

        # ── Setup section ──────────────────────────────────────────────────
        setup_frame = ttk.LabelFrame(ctrl, text="Memory Setup", padding=6)
        setup_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(setup_frame, text="Total Size:").grid(row=0, column=0, sticky="w")
        self.total_size_var = tk.StringVar(value=str(self.memory.total_size))
        ttk.Entry(setup_frame, textvariable=self.total_size_var, width=8).grid(row=0, column=1, padx=4)

        ttk.Label(setup_frame, text="Holes (start,size per line):").grid(row=1, column=0, columnspan=2, sticky="w")
        self.holes_text = tk.Text(setup_frame, width=22, height=4, font=("Courier", 9))
        self.holes_text.grid(row=2, column=0, columnspan=2)
        self.holes_text.insert("1.0", "0,300\n400,250\n700,200")

        ttk.Label(setup_frame, text="Algorithm:").grid(row=3, column=0, sticky="w", pady=(4, 0))
        self.algo_var = tk.StringVar(value="First-Fit")
        ttk.Combobox(
            setup_frame, textvariable=self.algo_var,
            values=["First-Fit", "Best-Fit"], state="readonly", width=10
        ).grid(row=3, column=1, padx=4, pady=(4, 0))

        ttk.Button(setup_frame, text="Apply Setup", command=self._apply_setup).grid(
            row=4, column=0, columnspan=2, pady=(6, 0), sticky="ew")

        # ── Allocate section ───────────────────────────────────────────────
        alloc_frame = ttk.LabelFrame(ctrl, text="Allocate Process", padding=6)
        alloc_frame.pack(fill="x", pady=(0, 8))

        ttk.Label(alloc_frame, text="Process Name:").grid(row=0, column=0, sticky="w")
        self.proc_name_var = tk.StringVar()
        ttk.Entry(alloc_frame, textvariable=self.proc_name_var, width=10).grid(row=0, column=1, padx=4)

        ttk.Label(alloc_frame, text="Segments (name,size per line):").grid(row=1, column=0, columnspan=2, sticky="w")
        self.segments_text = tk.Text(alloc_frame, width=22, height=5, font=("Courier", 9))
        self.segments_text.grid(row=2, column=0, columnspan=2)
        self.segments_text.insert("1.0", "Code,100\nData,120\nStack,90")

        ttk.Button(alloc_frame, text="Allocate", command=self._allocate).grid(
            row=3, column=0, columnspan=2, pady=(6, 0), sticky="ew")

        # ── Deallocate section ─────────────────────────────────────────────
        dealloc_frame = ttk.LabelFrame(ctrl, text="Deallocate Process", padding=6)
        dealloc_frame.pack(fill="x")

        ttk.Label(dealloc_frame, text="Process:").grid(row=0, column=0, sticky="w")
        self.dealloc_var = tk.StringVar()
        self.dealloc_combo = ttk.Combobox(
            dealloc_frame, textvariable=self.dealloc_var,
            state="readonly", width=12)
        self.dealloc_combo.grid(row=0, column=1, padx=4)

        ttk.Button(dealloc_frame, text="Deallocate", command=self._deallocate).grid(
            row=1, column=0, columnspan=2, pady=(6, 0), sticky="ew")

    def _build_display(self, parent):
        display = ttk.Frame(parent, padding=4)
        display.grid(row=0, column=1, sticky="nsew")
        display.columnconfigure(0, weight=1)
        display.columnconfigure(1, weight=1)
        display.rowconfigure(0, weight=1)

        # Memory map canvas
        map_frame = ttk.LabelFrame(display, text="Memory Layout", padding=4)
        map_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        map_frame.rowconfigure(0, weight=1)
        map_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(map_frame, width=180, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        map_scroll = ttk.Scrollbar(map_frame, orient="vertical", command=self.canvas.yview)
        map_scroll.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=map_scroll.set)

        # Segment tables
        table_frame = ttk.LabelFrame(display, text="Segment Tables", padding=4)
        table_frame.grid(row=0, column=1, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.table_text = tk.Text(
            table_frame, width=36, font=("Courier", 9),
            state="disabled", wrap="none")
        self.table_text.grid(row=0, column=0, sticky="nsew")

        tbl_scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.table_text.yview)
        tbl_scroll_y.grid(row=0, column=1, sticky="ns")
        self.table_text.configure(yscrollcommand=tbl_scroll_y.set)

        self._refresh_display()

    # ---------------------------------------------------------------- actions

    def _apply_setup(self):
        try:
            total = int(self.total_size_var.get())
        except ValueError:
            messagebox.showerror("Error", "Total size must be an integer.")
            return

        holes = []
        for line in self.holes_text.get("1.0", "end").strip().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 2:
                messagebox.showerror("Error", f"Invalid hole line: '{line}'. Use start,size")
                return
            try:
                start, size = int(parts[0]), int(parts[1])
            except ValueError:
                messagebox.showerror("Error", f"Non-integer in hole line: '{line}'")
                return
            holes.append(Hole(size=size, starting_address=start))

        self.memory.__init__(total, holes)

        algo = self.algo_var.get()
        if algo == "First-Fit":
            self.allocator.__class__ = FirstFitAllocator
            self.allocator.__init__("First-Fit Allocator", self.memory)
        else:
            self.allocator.__class__ = BestFitAllocator
            self.allocator.__init__("Best-Fit Allocator", self.memory)

        self._process_color_map.clear()
        self._color_index = 0
        self._refresh_display()

    def _allocate(self):
        name = self.proc_name_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter a process name.")
            return

        segments_raw = self.segments_text.get("1.0", "end").strip().splitlines()
        if not segments_raw:
            messagebox.showerror("Error", "Enter at least one segment.")
            return

        parsed_segments = []
        for line in segments_raw:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 2:
                messagebox.showerror("Error", f"Invalid segment line: '{line}'. Use name,size")
                return
            try:
                seg_size = int(parts[1])
            except ValueError:
                messagebox.showerror("Error", f"Non-integer size in: '{line}'")
                return
            parsed_segments.append((parts[0].strip(), seg_size))

        process = Process(name, len(parsed_segments))
        for seg_name, seg_size in parsed_segments:
            process.add_segment(seg_name, seg_size)

        self.allocator.allocate(process)

        if process in self.memory.get_process_list():
            self._assign_color(name)
        else:
            messagebox.showwarning("Does Not Fit", f"Process {name} does not fit in memory.")

        self._refresh_display()

    def _deallocate(self):
        name = self.dealloc_var.get().strip()
        if not name:
            messagebox.showerror("Error", "Select a process to deallocate.")
            return

        target = next(
            (p for p in self.memory.get_process_list() if p.get_name() == name),
            None
        )
        if target is None:
            messagebox.showerror("Error", f"Process '{name}' not found in memory.")
            return

        self.allocator.deallocate(target)
        self._refresh_display()

    # --------------------------------------------------------------- display

    def _refresh_display(self):
        self._draw_memory()
        self._draw_segment_tables()
        self._update_process_list()

    def _draw_memory(self):
        self.canvas.delete("all")

        total = self.memory.total_size
        canvas_width = 180
        canvas_height = max(600, total)
        scale = canvas_height / total

        BAR_X0, BAR_X1 = 40, canvas_width - 10

        self.canvas.configure(scrollregion=(0, 0, canvas_width, canvas_height + 20))

        for seg in self.memory.get_memory_block().values():
            y0 = int(seg.get_starting_address() * scale)
            y1 = int(seg.get_ending_address() * scale)
            color = self._segment_color(seg)

            self.canvas.create_rectangle(BAR_X0, y0, BAR_X1, y1,
                                         fill=color, outline="white", width=1)

            label = self._segment_label(seg)
            mid_y = (y0 + y1) / 2
            block_height = y1 - y0
            if block_height >= 12:
                self.canvas.create_text(
                    (BAR_X0 + BAR_X1) / 2, mid_y,
                    text=label, fill="white", font=("Arial", 7, "bold"),
                    width=BAR_X1 - BAR_X0 - 4)

            # address labels
            self.canvas.create_text(BAR_X0 - 2, y0, text=str(seg.get_starting_address()),
                                     anchor="e", font=("Arial", 7), fill="#333")

        # ending address
        self.canvas.create_text(BAR_X0 - 2, canvas_height,
                                 text=str(total), anchor="e", font=("Arial", 7), fill="#333")

    def _draw_segment_tables(self):
        self.table_text.configure(state="normal")
        self.table_text.delete("1.0", "end")

        processes = self.memory.get_process_list()
        if not processes:
            self.table_text.insert("end", "(no processes allocated)")
        else:
            for proc in processes:
                self.table_text.insert("end", f"Process: {proc.get_name()}\n")
                self.table_text.insert("end", f"{'Segment':<12}{'Start':>8}{'Size':>8}\n")
                self.table_text.insert("end", "-" * 28 + "\n")
                for seg in proc.get_segments():
                    self.table_text.insert(
                        "end",
                        f"{seg.get_data_type():<12}{seg.get_starting_address():>8}{seg.get_size():>8}\n"
                    )
                self.table_text.insert("end", "\n")

        self.table_text.configure(state="disabled")

    def _update_process_list(self):
        names = [p.get_name() for p in self.memory.get_process_list()]
        self.dealloc_combo["values"] = names
        if names:
            self.dealloc_var.set(names[0])
        else:
            self.dealloc_var.set("")

    # ---------------------------------------------------------------- helpers

    def _assign_color(self, process_name: str):
        if process_name not in self._process_color_map:
            self._process_color_map[process_name] = (
                COLORS["process"][self._color_index % len(COLORS["process"])]
            )
            self._color_index += 1

    def _segment_color(self, seg) -> str:
        if isinstance(seg, Hole):
            return COLORS["hole"]
        if isinstance(seg, InvalidBlock):
            return COLORS["invalid"]
        if isinstance(seg, SegmentOfProcess):
            name = seg.get_process().get_name()
            if name not in self._process_color_map:
                self._assign_color(name)
            return self._process_color_map[name]
        return "#cccccc"

    def _segment_label(self, seg) -> str:
        if isinstance(seg, Hole):
            return f"{seg.get_name()}\n{seg.get_size()}"
        if isinstance(seg, InvalidBlock):
            return f"invalid\n{seg.get_size()}"
        if isinstance(seg, SegmentOfProcess):
            return f"{seg.get_process().get_name()}.{seg.get_data_type()}\n{seg.get_size()}"
        return seg.get_name()

    # ------------------------------------------------------------------- run

    def run(self):
        self.root.mainloop()