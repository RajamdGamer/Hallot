import tkinter as tk
from tkinter import messagebox
import json

class HallAllotmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hall Allotment Software")

        # Maximize the window
        self.root.state('zoomed')

        # Create main frame with a canvas for scrolling
        self.canvas = tk.Canvas(root, bg='lightgreen')
        self.h_scrollbar = tk.Scrollbar(root, orient="horizontal", command=self.canvas.xview)
        self.v_scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg='lightgreen')

        # Add scroll frame to canvas
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor='nw')
        self.scroll_frame.bind("<Configure>", self.on_frame_configure)
        
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        # Bind mouse wheel to scroll canvas
        self.root.bind_all("<MouseWheel>", self.on_mouse_wheel)

        self.blocks = ["A Block", "B Block", "C Block", "D Block", "E Block", "F Block", "CS Block"]
        self.rooms = {
            "A Block": ["A204", "A209", "A210", "A301", "A303", "A304", "A305", "A306", "A308", "A309", "A310", "A311", "A312"],
            "B Block": ["B101", "B104", "B107", "B109", "B203", "B205", "B207", "B208", "B209", "B210", "B211", "B212", "B302"],
            "C Block": ["C101", "C105", "C107", "C108", "C109", "C110", "C201", "C205", "C206", "C207", "C208"],
            "D Block": ["D002", "D005", "D104", "D105", "D201", "D202", "D204", "D205", "D206", "D207"],
            "E Block": ["E003", "E004", "E005", "E006", "E101", "E102", "E105", "E201", "E202", "E203", "E205", "E206", "E301", "E302", "E303", "E305", "E306", "E307"],
            "F Block": ["F201", "F202", "F203", "F301", "F302", "F303"],
            "CS Block": ["CS-201", "CS-202", "CS-203", "CS-204", "CS-301", "CS-302"]
        }

        self.check_vars = {block: [tk.BooleanVar() for _ in self.rooms[block]] for block in self.blocks}
        self.block_vars = {block: tk.BooleanVar() for block in self.blocks}

        self.create_interface()

    def create_interface(self):
        for col, block in enumerate(self.blocks):
            block_frame = tk.LabelFrame(self.scroll_frame, text=block, bg='lightgreen', padx=10, pady=10)
            block_frame.grid(row=0, column=col, padx=10, pady=10, sticky='nsew')

            block_check = tk.Checkbutton(block_frame, text=block, variable=self.block_vars[block], bg='lightgreen', command=lambda b=block: self.select_all_in_block(b))
            block_check.grid(row=0, column=0, sticky='w', columnspan=2)

            # Create a grid layout for the rooms in the block frame
            for i, room in enumerate(self.rooms[block]):
                tk.Checkbutton(block_frame, text=room, variable=self.check_vars[block][i], bg='lightgreen').grid(row=(i//4) + 1, column=i%4, sticky='w')

        # Add control buttons
        button_frame = tk.Frame(self.scroll_frame, bg='lightgreen')
        button_frame.grid(row=1, column=0, columnspan=len(self.blocks), pady=10, sticky='ew')

        tk.Button(button_frame, text="Select All Halls", command=self.select_all).pack(side='left', padx=10)
        tk.Button(button_frame, text="Deselect All Halls", command=self.deselect_all).pack(side='left', padx=10)
        tk.Button(button_frame, text="Next", command=self.next_step).pack(side='left', padx=10)

        # Preview label
        self.preview_label = tk.Label(self.scroll_frame, text="Selected Rooms: ", bg='lightgreen')
        self.preview_label.grid(row=2, column=0, columnspan=len(self.blocks), pady=10, sticky='w')

        # Update canvas scroll region
        self.scroll_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def select_all_in_block(self, block):
        state = self.block_vars[block].get()
        for var in self.check_vars[block]:
            var.set(state)
        self.update_preview()

    def select_all(self):
        for block in self.blocks:
            for var in self.check_vars[block]:
                var.set(True)
        self.update_preview()

    def deselect_all(self):
        for block in self.blocks:
            for var in self.check_vars[block]:
                var.set(False)
        self.update_preview()

    def update_preview(self):
        selected_rooms = []
        for block in self.blocks:
            for i, var in enumerate(self.check_vars[block]):
                if var.get():
                    selected_rooms.append(self.rooms[block][i])
        self.preview_label.config(text="Selected Rooms: " + ', '.join(selected_rooms))

    def next_step(self):
        self.selected_rooms = []  # Clear selected_rooms before appending new selections
        for block in self.blocks:
            for i, var in enumerate(self.check_vars[block]):
                if var.get():
                    self.selected_rooms.append(self.rooms[block][i])
        
        messagebox.showinfo("Selected Rooms", f"Selected Rooms: {', '.join(self.selected_rooms)}")
        
        # Save the selected rooms to a file
        with open('selected_rooms.json', 'w') as f:
            json.dump(self.selected_rooms, f)
        
        self.root.destroy()  # Close the window after saving

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        if event.state & 0x0001:  # Shift key pressed
            self.canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        else:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

if __name__ == "__main__":
    root = tk.Tk()
    app = HallAllotmentApp(root)
    root.mainloop()
