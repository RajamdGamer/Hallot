import tkinter as tk
from tkinter import messagebox
import json

class DepartmentSelectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Department Selection")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Set the window size relative to the screen size
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")

        # Create a canvas and a scrollbar
        self.canvas = tk.Canvas(self.root, bg='lightgreen')
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.main_frame = tk.Frame(self.canvas, bg='lightgreen')
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Bind mouse wheel scroll
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # For Linux systems
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # For Linux systems

        self.ug_programmes = [
            "B.Sc. Maths", "B.Sc. Maths with CA", "B.Sc. CS", "B.Sc. CS (GCD)", "B.Sc. CS (AI & DS)",
            "B.Sc. CS (CS)", "B.Sc. CS (DA)", "B.Sc. Forensic Science", "B.Sc. IT", "BCA", "B.Com.",
            "B.Com. (DM and DM)", "B.Com. (CA)", "B.Com. (PA)", "B.Com. Finance", "B.Com. (IT)", "BBA",
            "BBA (CA)", "B.Sc. CD & F", "B.Sc. CS & HM", "B.A. English Lit.,", "B.Sc. Physics", "B.Sc. Chemistry",
            "B.Sc. Psychology", "B.Sc. CS with Cloud & Information Security", "B.Sc. CS with Block Chain Technology",
            "B.Sc. CS with IOT"
        ]
        self.pg_programmes = [
            "M.Sc. Mathematics", "M.Sc. Computer Science", "M.Com", "M.Com (CA)", "M.A. English Literature", 
            "MBA", "MCA"
        ]

        self.check_vars_ug = [[tk.BooleanVar() for _ in range(3)] for _ in self.ug_programmes]
        self.check_vars_pg = [[tk.BooleanVar() for _ in range(2)] for _ in self.pg_programmes]
        self.select_all_vars_ug = [tk.BooleanVar() for _ in self.ug_programmes]
        self.select_all_vars_pg = [tk.BooleanVar() for _ in self.pg_programmes]

        self.create_interface()

    def _on_mousewheel(self, event):
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")

    def create_interface(self):
        # UG Programmes
        tk.Label(self.main_frame, text="UG Programmes", bg='lightgreen', font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=5, pady=10)
        self.create_programme_interface("UG", self.ug_programmes, self.check_vars_ug, self.select_all_vars_ug, 1, 5)

        # PG Programmes
        tk.Label(self.main_frame, text="PG Programmes", bg='lightgreen', font=('Arial', 14, 'bold')).grid(row=len(self.ug_programmes) + 2, column=0, columnspan=4, pady=10)
        self.create_programme_interface("PG", self.pg_programmes, self.check_vars_pg, self.select_all_vars_pg, len(self.ug_programmes) + 3, 4)

        # Buttons
        tk.Button(self.main_frame, text="Reset", command=self.reset_selections).grid(row=len(self.ug_programmes) + len(self.pg_programmes) + 4, column=0, pady=10, columnspan=2, sticky='ew')
        tk.Button(self.main_frame, text="Submit", command=self.submit_selections).grid(row=len(self.ug_programmes) + len(self.pg_programmes) + 4, column=2, pady=10, columnspan=2, sticky='ew')

        # Preview bar
        self.preview_label = tk.Label(self.main_frame, text="Selected Courses Preview:", bg='lightgreen', font=('Arial', 12, 'bold'))
        self.preview_label.grid(row=len(self.ug_programmes) + len(self.pg_programmes) + 5, column=0, columnspan=4, pady=10)

        self.preview_text = tk.Text(self.main_frame, height=10, width=80)
        self.preview_text.grid(row=len(self.ug_programmes) + len(self.pg_programmes) + 6, column=0, columnspan=4, pady=10)

    def create_programme_interface(self, programme_type, programmes, check_vars, select_all_vars, start_row, col_span):
        years = ["1st Year", "2nd Year"] if programme_type == "PG" else ["1st Year", "2nd Year", "3rd Year"]

        # Header
        tk.Label(self.main_frame, text="", bg='lightgreen').grid(row=start_row, column=1, padx=5)
        for i, year in enumerate(years):
            tk.Label(self.main_frame, text=year, bg='lightgreen', font=('Arial', 12, 'bold')).grid(row=start_row, column=2 + i, padx=5)

        # Programmes and checkboxes
        for i, programme in enumerate(programmes):
            select_all_checkbox = tk.Checkbutton(self.main_frame, variable=select_all_vars[i], command=lambda i=i: self.select_all_in_years(i, programme_type), bg='lightgreen')
            select_all_checkbox.grid(row=start_row + i + 1, column=0, padx=5)
            tk.Label(self.main_frame, text=programme, bg='lightgreen', anchor='w').grid(row=start_row + i + 1, column=1, sticky='w', padx=5)
            for j in range(len(years)):
                tk.Checkbutton(self.main_frame, variable=check_vars[i][j], bg='lightgreen').grid(row=start_row + i + 1, column=2 + j)

    def select_all_in_years(self, index, programme_type):
        if programme_type == "UG":
            select_all_state = self.select_all_vars_ug[index].get()
            for var in self.check_vars_ug[index]:
                var.set(select_all_state)
        elif programme_type == "PG":
            select_all_state = self.select_all_vars_pg[index].get()
            for var in self.check_vars_pg[index]:
                var.set(select_all_state)

    def reset_selections(self):
        for var_list in self.check_vars_ug:
            for var in var_list:
                var.set(False)
        for var_list in self.check_vars_pg:
            for var in var_list:
                var.set(False)
        for var in self.select_all_vars_ug:
            var.set(False)
        for var in self.select_all_vars_pg:
            var.set(False)
        self.preview_text.delete('1.0', tk.END)

    def submit_selections(self):
        selected_courses = {}
        
        # UG Programmes
        for i, programme in enumerate(self.ug_programmes):
            years_selected = []
            for j in range(3):
                if self.check_vars_ug[i][j].get():
                    years_selected.append(f"{j+1}")
            if years_selected:
                selected_courses[programme] = years_selected

        # PG Programmes
        for i, programme in enumerate(self.pg_programmes):
            years_selected = []
            for j in range(2):
                if self.check_vars_pg[i][j].get():
                    years_selected.append(f"{j+1}")
            if years_selected:
                selected_courses[programme] = years_selected

        # Save to JSON
        with open('selected_departments.json', 'w') as f:
            json.dump(selected_courses, f, indent=4)

        # Update preview text
        self.preview_text.delete('1.0', tk.END)
        for programme, years in selected_courses.items():
            self.preview_text.insert(tk.END, f"{programme} - Years: {', '.join(years)}\n")

        messagebox.showinfo("Selected Departments", f"Selected Departments saved successfully.")
        self.root.destroy()  # Close the window after saving

if __name__ == "__main__":
    root = tk.Tk()
    app = DepartmentSelectionApp(root)
    root.mainloop()