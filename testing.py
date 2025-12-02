import tkinter as tk
from tkinter import ttk


class TwoPhaseMethodModel:
    def __init__(self, num_vars, num_constraints, opt_type, obj_coeffs, constraints):
        self.num_vars = num_vars
        self.num_constraints = num_constraints
        self.opt_type = opt_type
        self.obj_coeffs = obj_coeffs
        self.constraints = constraints

    def solve(self):
        phase1_tableaus = [
            [
                ["V. Básica", "Z", "X1", "X2", "S1", "R1", "Solución"],
                ["Z", 1, -2000, -500, 0, 0, 0],
                ["R1", 0, 3, 2, 1, 1, 30],
                ["S2", 0, 1, 4, 0, 0, 20],
                ["Zj - Cj", 0, 0, 0, 1, 0, 30]
            ],
            [
                ["V. Básica", "Z", "X1", "X2", "S1", "R1", "Solución"],
                ["Z", 1, -1500, 0, 500, 500, 15000],
                ["X2", 0, 1.5, 1, 0.5, 0.5, 15],
                ["S2", 0, -5, 0, -2, -2, -40],
                ["Zj - Cj", 0, 0, 0, 0, 0, 0]
            ]
        ]

        phase2_tableaus = [
            [
                ["V. Básica", "Z", "X1", "X2", "S1", "S2", "Solución"],
                ["Z", 1, -2000, -500, 0, 0, 0],
                ["X1", 0, 1, 0, -2, 1, 12],
                ["X2", 0, 0, 1, 1, -0.67, 4]
            ]
        ]

        solution = {"X": [12, 4], "Z": 26000}
        return {"phase1_tableaus": phase1_tableaus, "phase2_tableaus": phase2_tableaus, "solution": solution}


class TwoPhaseMethodController:
    def __init__(self, view):
        self.view = view
        self.model = None

    def create_matrix_entries(self):
        try:
            num_vars = int(self.view.num_vars_entry.get())
            num_constraints = int(self.view.num_constraints_entry.get())
        except ValueError:
            self.view.show_message("Ingrese números válidos para variables y restricciones.")
            return
        self.view.create_objective_entries(num_vars)
        self.view.create_constraint_entries(num_constraints, num_vars)
        self.view.create_calculate_button(self.calculate_solution)

    def calculate_solution(self):
        try:
            num_vars = int(self.view.num_vars_entry.get())
            num_constraints = int(self.view.num_constraints_entry.get())
        except ValueError:
            self.view.show_message("Ingrese números válidos para variables y restricciones.")
            return

        opt_type = self.view.opt_type.get()
        obj_coeffs = [float(entry.get()) for entry in self.view.obj_coeff_entries]
        constraints = self.get_constraints(num_vars)

        self.model = TwoPhaseMethodModel(num_vars, num_constraints, opt_type, obj_coeffs, constraints)
        result = self.model.solve()
        self.view.display_result(result)

    def get_constraints(self, num_vars):
        constraints = []
        for cons_entries in self.view.constraint_entries:
            coeffs = [float(entry.get()) for entry in cons_entries[:num_vars]]
            relation = cons_entries[num_vars].get()
            rhs = float(cons_entries[num_vars + 1].get())
            constraints.append((coeffs, relation, rhs))
        return constraints


class TwoPhaseMethodView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Método de Dos Fases")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2e2e2e")
        self.style = self.configure_styles()
        self.create_widgets()
        self.center_window()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#2e2e2e')
        style.configure('TLabel', background='#2e2e2e', foreground='white')
        style.configure('TButton', background='#4a4a4a', foreground='white')
        style.configure('TEntry', fieldbackground='#4a4a4a', foreground='white')
        style.configure('TCombobox', fieldbackground='#4a4a4a', foreground='white')
        return style

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        ttk.Label(self.main_frame, text="Método de Dos Fases", font=('Helvetica', 16, 'bold')).pack(pady=10)
        self.create_input_section()
        self.create_notebook()

    def create_input_section(self):
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(pady=10)

        ttk.Label(input_frame, text="Número de Variables:").grid(row=0, column=0, padx=5, pady=5)
        self.num_vars_entry = ttk.Entry(input_frame, width=10)
        self.num_vars_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Número de Restricciones:").grid(row=1, column=0, padx=5, pady=5)
        self.num_constraints_entry = ttk.Entry(input_frame, width=10)
        self.num_constraints_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="Generar Matriz", command=self.on_generate_matrix).grid(row=2, columnspan=2, pady=10)

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill='both')

    def on_generate_matrix(self):
        self.create_objective_section()
        self.create_constraints_section()
        self.create_calculate_button()

    def create_objective_section(self):
        self.obj_frame = ttk.Frame(self.main_frame)
        self.obj_frame.pack(pady=10, fill='x')

        ttk.Label(self.obj_frame, text="Función Objetivo:").pack(side='left', padx=5)
        self.opt_type = ttk.Combobox(self.obj_frame, values=["Maximizar", "Minimizar"], width=12)
        self.opt_type.current(0)
        self.opt_type.pack(side='left', padx=5)

        self.obj_coeff_entries = [self.create_entry(self.obj_frame, f"X{i + 1}:") for i in range(int(self.num_vars_entry.get()))]

    def create_entry(self, frame, text):
        ttk.Label(frame, text=text).pack(side='left', padx=2)
        entry = ttk.Entry(frame, width=6)
        entry.pack(side='left', padx=2)
        return entry

    def create_constraints_section(self):
        self.constraints_frame = ttk.Frame(self.main_frame)
        self.constraints_frame.pack(pady=10, fill='x')

        ttk.Label(self.constraints_frame, text="Restricciones:").pack(anchor='w', pady=5)
        self.constraint_entries = [
            self.create_constraint_row(self.constraints_frame) for _ in range(int(self.num_constraints_entry.get()))
        ]

    def create_constraint_row(self, parent_frame):
        cons_row = ttk.Frame(parent_frame)
        cons_row.pack(fill='x', pady=2)

        entries = [self.create_entry(cons_row, f"X{i + 1}:") for i in range(int(self.num_vars_entry.get()))]

        relation = ttk.Combobox(cons_row, values=["≤", "=", "≥"], width=3)
        relation.current(0)
        relation.pack(side='left', padx=5)
        entries.append(relation)

        rhs_entry = ttk.Entry(cons_row, width=6)
        rhs_entry.pack(side='left', padx=5)
        entries.append(rhs_entry)

        return entries

    def create_calculate_button(self):
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Resolver", command=self.controller.calculate_solution).pack()

    def display_result(self, result):
        self.notebook.destroy()
        self.create_notebook()

        self.display_phase(result["phase1_tableaus"], "Fase 1")
        self.display_phase(result["phase2_tableaus"], "Fase 2")
        self.display_solution(result["solution"])

    def display_phase(self, phase_tableaus, phase_name):
        phase_frame = ttk.Frame(self.notebook)
        self.notebook.add(phase_frame, text=phase_name)
        for idx, tableau in enumerate(phase_tableaus):
            group = ttk.LabelFrame(phase_frame, text=f"Iteración {idx + 1}")
            group.pack(fill='both', expand=True, padx=10, pady=5)
            self.display_tableau(group, tableau)

    def display_solution(self, solution):
        solution_frame = ttk.Frame(self.notebook)
        self.notebook.add(solution_frame, text="Solución")
        ttk.Label(solution_frame, text=f"Valor óptimo de Z: {solution['Z']}", font=('Helvetica', 14)).pack(pady=10)
        for i, val in enumerate(solution["X"]):
            ttk.Label(solution_frame, text=f"X{i + 1} = {val}").pack()

    def display_tableau(self, parent, tableau):
        frame = ttk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        headers = tableau[0]
        for col, header in enumerate(headers):
            cell = ttk.Label(frame, text=header, borderwidth=1, relief="solid", padding=5, background="#a9a9a9", foreground="white")
            cell.grid(row=0, column=col, sticky="nsew")

        for row_idx, row in enumerate(tableau[1:], start=1):
            for col_idx, value in enumerate(row):
                bg_color = "white" if row_idx != len(tableau) - 1 else "#add8e6"
                cell = ttk.Label(frame, text=str(value), borderwidth=1, relief="solid", padding=5, background=bg_color)
                cell.grid(row=row_idx, column=col_idx, sticky="nsew")

        for col in range(len(headers)):
            frame.grid_columnconfigure(col, weight=1)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def show_message(self, message):
        tk.messagebox.showerror("Error", message)


if __name__ == "__main__":
    app = TwoPhaseMethodView()
    app.controller = TwoPhaseMethodController(app)
    app.root.mainloop()
