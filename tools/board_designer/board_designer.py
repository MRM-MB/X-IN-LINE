import tkinter as tk
from tkinter import messagebox, filedialog
import importlib.util
import os

class BoardDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("X-in-a-Line Board Designer by Manish Raj Moriche")

        self.width = 15
        self.height = 15
        self.cell_size = 30
        self.obstacles = set()
        self.is_drawing = True  # Track if we are adding or removing in the current drag

        # Controls frame
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Row 1: Dimensions and Actions
        row1 = tk.Frame(self.controls_frame)
        row1.pack(side=tk.TOP, fill=tk.X, pady=2)

        tk.Label(row1, text="W:").pack(side=tk.LEFT)
        self.width_entry = tk.Entry(row1, width=5)
        self.width_entry.insert(0, "15")
        self.width_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(row1, text="H:").pack(side=tk.LEFT)
        self.height_entry = tk.Entry(row1, width=5)
        self.height_entry.insert(0, "15")
        self.height_entry.pack(side=tk.LEFT, padx=2)

        tk.Button(row1, text="Set Size", command=self.reset_grid).pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Load Board", command=self.load_board).pack(side=tk.LEFT, padx=5)
        tk.Button(row1, text="Generate Code", command=self.generate_code).pack(side=tk.LEFT, padx=5)

        # Row 2: Zoom and Help
        row2 = tk.Frame(self.controls_frame)
        row2.pack(side=tk.TOP, fill=tk.X, pady=2)

        tk.Label(row2, text="Zoom:").pack(side=tk.LEFT)
        self.zoom_scale = tk.Scale(row2, from_=5, to=50, orient=tk.HORIZONTAL, command=self.update_zoom)
        self.zoom_scale.set(30)
        self.zoom_scale.pack(side=tk.LEFT, padx=5)
        
        tk.Label(row2, text="(Left click/drag to paint)").pack(side=tk.RIGHT, padx=5)

        # Canvas frame with scrollbars
        self.canvas_frame = tk.Frame(root)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.v_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.VERTICAL)
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL)

        self.canvas = tk.Canvas(self.canvas_frame, bg="white", 
                                yscrollcommand=self.v_scrollbar.set, 
                                xscrollcommand=self.h_scrollbar.set)
        
        self.v_scrollbar.config(command=self.canvas.yview)
        self.h_scrollbar.config(command=self.canvas.xview)

        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.draw_grid()

    def update_zoom(self, val):
        self.cell_size = int(val)
        self.draw_grid()

    def load_board(self):
        file_path = filedialog.askopenfilename(
            initialdir="boards",
            title="Select Board File",
            filetypes=(("Python files", "*.py"), ("All files", "*.*"))
        )
        if not file_path:
            return
            
        try:
            spec = importlib.util.spec_from_file_location("loaded_board", file_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            
            self.width = mod.BOARD_WIDTH
            self.height = mod.BOARD_HEIGHT
            self.obstacles = set(mod.OBSTACLES)
            
            self.width_entry.delete(0, tk.END)
            self.width_entry.insert(0, str(self.width))
            self.height_entry.delete(0, tk.END)
            self.height_entry.insert(0, str(self.height))
            
            self.draw_grid()
            messagebox.showinfo("Success", f"Loaded {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load board: {e}")

    def reset_grid(self):
        try:
            self.width = int(self.width_entry.get())
            self.height = int(self.height_entry.get())
            self.obstacles = set()
            self.draw_grid()
        except ValueError:
            messagebox.showerror("Error", "Invalid width or height")

    def draw_grid(self):
        self.canvas.delete("all")
        
        # Calculate total grid size
        grid_width = self.width * self.cell_size
        grid_height = self.height * self.cell_size
        
        # Update scroll region
        self.canvas.config(scrollregion=(0, 0, grid_width, grid_height))

        # Draw grid lines
        for i in range(self.width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, grid_height, fill="#ddd")
        
        for i in range(self.height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, grid_width, y, fill="#ddd")

        # Draw obstacles
        for x, y in self.obstacles:
            self.draw_cell(x, y, "black")

    def draw_cell(self, x, y, color):
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", tags=f"cell_{x}_{y}")

    def start_draw(self, event):
        # Account for scrolling
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        x = int(canvas_x // self.cell_size)
        y = int(canvas_y // self.cell_size)
        
        if 0 <= x < self.width and 0 <= y < self.height:
            if (x, y) in self.obstacles:
                self.is_drawing = False # We clicked an existing one, so we are erasing
                self.obstacles.remove((x, y))
                self.canvas.delete(f"cell_{x}_{y}")
            else:
                self.is_drawing = True # We clicked empty, so we are drawing
                self.obstacles.add((x, y))
                self.draw_cell(x, y, "black")

    def draw(self, event):
        # Account for scrolling
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        x = int(canvas_x // self.cell_size)
        y = int(canvas_y // self.cell_size)

        if 0 <= x < self.width and 0 <= y < self.height:
            if self.is_drawing:
                if (x, y) not in self.obstacles:
                    self.obstacles.add((x, y))
                    self.draw_cell(x, y, "black")
            else:
                if (x, y) in self.obstacles:
                    self.obstacles.remove((x, y))
                    self.canvas.delete(f"cell_{x}_{y}")

    def generate_code(self):
        code = f'BOARD_NAME = "CustomBoard"\n\n'
        code += f'BOARD_WIDTH = {self.width}\n'
        code += f'BOARD_HEIGHT = {self.height}\n'
        code += f'WIN_LENGTH = 4\n'
        code += f'NUM_PLAYERS = 2\n\n'
        
        code += "OBSTACLES = [\n"
        sorted_obstacles = sorted(list(self.obstacles), key=lambda p: (p[1], p[0]))
        
        # Format nicely
        line_buffer = "    "
        for i, (x, y) in enumerate(sorted_obstacles):
            item = f"({x}, {y}), "
            if len(line_buffer) + len(item) > 80:
                code += line_buffer + "\n"
                line_buffer = "    " + item
            else:
                line_buffer += item
        
        if line_buffer.strip():
            code += line_buffer
            
        code += "\n]\n\n"
        code += "GAME_TIME_MS = 1000\n"

        print("\n" + "="*40)
        print("Copy the code below into a new file in boards/")
        print("="*40 + "\n")
        print(code)
        print("="*40)
        
        # Also copy to clipboard if possible
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(code)
            messagebox.showinfo("Success", "Code generated and copied to clipboard! Check the terminal as well.")
        except:
            messagebox.showinfo("Success", "Code generated! Check the terminal output.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BoardDesigner(root)
    root.mainloop()
