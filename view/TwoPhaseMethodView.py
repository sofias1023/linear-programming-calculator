import tkinter as tk
from tkinter import ttk
from controller.two_phase_controller import TwoPhaseMethodController
from utils.center_window import center_window


class TwoPhaseMethodView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Método de Dos Fases")

        self.root.state('zoomed')
        self.root.configure(bg="#2e2e2e")

        self.init_ui()
        self.controller = TwoPhaseMethodController(self)

        center_window(self.root)
        self.root.mainloop()

    def create_entries(self, parent_frame, num_vars):
        entries = []
        for i in range(num_vars):
            entry = tk.Entry(parent_frame, width=10, bg="#ffffff", fg="#000000", insertbackground="black", highlightthickness=0)
            entry.pack(side=tk.LEFT, padx=5, pady=5)
            # Añadir borde inferior visible
            entry.config(highlightbackground="#000000", highlightcolor="#000000", bd=0)
            entries.append(entry)
        return entries

    def create_objective_entries(self, num_vars):
        obj_frame = tk.Frame(self.frame, bg="#2e2e2e")
        obj_frame.pack(pady=10)

        tk.Label(obj_frame, text="Función Objetivo:", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 16)).pack(
            side=tk.LEFT, padx=5)

        self.opt_type = ttk.Combobox(obj_frame, values=["Maximizar", "Minimizar"], width=12, style="TCombobox")
        self.opt_type.current(0)
        self.opt_type.pack(side=tk.LEFT, padx=5)

        # Crear la visualización con [] X1 [] X2 ... [] Xi
        entry_labels_frame = tk.Frame(obj_frame, bg="#2e2e2e")
        entry_labels_frame.pack(pady=5)

        for i in range(num_vars):
            # Crear la entrada para el coeficiente
            entry = tk.Entry(entry_labels_frame, width=5, bg="#ffffff", fg="#000000", insertbackground="black",
                             highlightthickness=0)
            entry.pack(side=tk.LEFT, padx=5, pady=5)
            entry.config(highlightbackground="#000000", highlightcolor="#000000", bd=0)

            # Crear la etiqueta para X1, X2, ..., Xi
            label = tk.Label(entry_labels_frame, text=f"x{i + 1}", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 14))
            label.pack(side=tk.LEFT, padx=5)

        # Almacenar las entradas en una lista si es necesario para luego obtener los valores
        self.obj_coeff_entries = [entry for entry in entry_labels_frame.winfo_children() if isinstance(entry, tk.Entry)]

    def create_constraint_entries(self, num_constraints, num_vars):
        constraints_frame = tk.Frame(self.frame, bg="#2e2e2e")
        constraints_frame.pack(pady=10, fill="x")

        tk.Label(constraints_frame, text="Restricciones:", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 16)).pack(
            anchor="w", padx=5)

        self.constraint_entries = []
        for i in range(num_constraints):
            constraint_frame = tk.Frame(constraints_frame, bg="#2e2e2e")
            constraint_frame.pack(pady=5, fill="x")

            tk.Label(constraint_frame, text=f"Restricción {i + 1}:", bg="#2e2e2e", fg="#ffffff").pack(side=tk.LEFT,
                                                                                                      padx=5)

            coeff_entries = []

            # Crear una sub-frame para mantener los inputs y labels alineados
            coeff_labels_frame = tk.Frame(constraint_frame, bg="#2e2e2e")
            coeff_labels_frame.pack(side=tk.LEFT)

            for j in range(num_vars):
                entry = tk.Entry(coeff_labels_frame, width=5, bg="#ffffff", fg="#000000", insertbackground="black",
                                 highlightthickness=0)
                entry.pack(side=tk.LEFT, padx=2, pady=2)
                entry.config(highlightbackground="#000000", highlightcolor="#000000", bd=0)
                coeff_entries.append(entry)

                label = tk.Label(coeff_labels_frame, text=f"x{j + 1}", bg="#2e2e2e", fg="#ffffff",
                                 font=("Helvetica", 14))
                label.pack(side=tk.LEFT, padx=2)

            sign = ttk.Combobox(constraint_frame, values=[">=", "=", "<="], width=3, style="TCombobox")
            sign.current(0)
            sign.pack(side=tk.LEFT, padx=5)

            rhs_entry = tk.Entry(constraint_frame, width=5, bg="#ffffff", fg="#000000", insertbackground="black",
                                 highlightthickness=0)
            rhs_entry.pack(side=tk.LEFT, padx=5)
            rhs_entry.config(highlightbackground="#000000", highlightcolor="#000000", bd=0)

            self.constraint_entries.append({
                "coeff_entries": coeff_entries,
                "sign": sign,
                "rhs": rhs_entry
            })

    def create_calculate_button(self, command):
        calculate_button = tk.Button(self.frame, text="Calcular Solución", command=command, bg="#ffffff", fg="#000000", font=("Helvetica", 14), relief="flat", bd=0, padx=10, pady=5)
        calculate_button.config(borderwidth=0, highlightthickness=0)
        calculate_button.pack(pady=10)

    def create_back_button(self):
        back_button = tk.Button(self.frame, text="Volver", command=self.on_back, bg="#ffffff", fg="#000000", font=("Helvetica", 14), relief="flat", bd=0, padx=10, pady=5)
        back_button.config(borderwidth=0, highlightthickness=0)
        back_button.pack(pady=10)

    def init_ui(self):
        self.frame = tk.Frame(self.root, bg="#2e2e2e")
        self.frame.pack()
        tk.Label(self.frame, text="Método de Dos Fases", font=("Helvetica", 24, "bold"), bg="#2e2e2e", fg="#ffffff").pack(pady=30)
        self.init_input_section()
        self.create_back_button()
        self.result_frame = tk.Frame(self.frame, bg="#2e2e2e")
        self.result_frame.pack(pady=20)

        # Pie de página
        self.footer_label = tk.Label(
            self.root,
            text="© Jhonattan Aponte - Karen Garzon",
            font=("Helvetica", 10),
            bg="#2e2e2e",
            fg="#888888"
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=20)

    def init_input_section(self):
        self.input_frame = tk.Frame(self.frame, bg="#2e2e2e")
        self.input_frame.pack(pady=20)
        self.num_vars_entry = self.create_labeled_entry("Número de Variables:", font_size=18)  # Cambié el tamaño de fuente
        self.num_constraints_entry = self.create_labeled_entry("Número de Restricciones:")
        self.generate_button = tk.Button(self.input_frame, text="Crear Matriz", command=self.on_generate_matrix, bg="#ffffff", fg="#000000", font=("Helvetica", 12), relief="flat", bd=0, padx=10, pady=5)
        self.generate_button.config(borderwidth=0, highlightthickness=0)
        self.generate_button.pack(pady=10)

    def create_labeled_entry(self, label_text, font_size=14):
        frame = tk.Frame(self.input_frame, bg="#2e2e2e")
        frame.pack(pady=2)
        label = tk.Label(frame, text=label_text, bg="#2e2e2e", fg="#ffffff", font=("Helvetica", font_size))
        label.pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, bd=0, highlightthickness=0, bg="#ffffff", fg="#000000", insertbackground="black")
        entry.pack(side=tk.LEFT)
        entry.config(highlightbackground="#000000", highlightcolor="#000000", bd=0)
        return entry

    def on_generate_matrix(self):
        self.controller.create_matrix_entries()

    def on_back(self):
        self.root.destroy()
        from view.MainView import MainView
        MainView()

    def display_result(self, result):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if isinstance(result, str):
            tk.Label(
                self.result_frame,
                text=result,
                justify=tk.LEFT,
                bg="#2e2e2e",
                fg="#ffffff",
                font=("Helvetica", 16),
            ).pack(pady=20)
            return

        notebook = ttk.Notebook(self.result_frame)
        notebook.pack(expand=True, fill="both")

        self.display_phase(notebook, result.get("phase1_tableaus", []), "Fase 1")
        self.display_phase(notebook, result.get("phase2_tableaus", []), "Fase 2")
        self.display_solution(notebook, result.get("solution", {}))

    def display_phase(self, notebook, phase_tableaus, phase_name):
        phase_frame = ttk.Frame(notebook)
        notebook.add(phase_frame, text=phase_name)

        if not phase_tableaus:
            ttk.Label(phase_frame, text="Sin iteraciones", background="#2e2e2e", foreground="white").pack(pady=10)
            return

        for idx, tableau in enumerate(phase_tableaus):
            group = ttk.LabelFrame(phase_frame, text=f"Iteración {idx + 1}")
            group.pack(fill="both", expand=True, padx=10, pady=5)
            self.display_tableau(group, tableau)

    def display_solution(self, notebook, solution):
        solution_frame = ttk.Frame(notebook)
        notebook.add(solution_frame, text="Solución")

        ttk.Label(solution_frame, text=f"Valor óptimo de Z: {solution.get('Z', 0)}", font=("Helvetica", 14)).pack(pady=10)
        for i, val in enumerate(solution.get("X", [])):
            ttk.Label(solution_frame, text=f"X{i + 1} = {val}").pack()

    def display_tableau(self, parent, tableau):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

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
