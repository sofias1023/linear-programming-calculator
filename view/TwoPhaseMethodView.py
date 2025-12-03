import tkinter as tk
from tkinter import ttk
from controller.two_phase_controller import TwoPhaseMethodController
from utils.center_window import center_window


class TwoPhaseMethodView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora")

        self.root.state('zoomed')
        self.colors = {
            "bg": "#0f172a",
            "panel": "#111827",
            "accent": "#22d3ee",
            "text_primary": "#e5e7eb",
            "text_muted": "#9ca3af",
            "input": "#0b1220",
        }

        self.bg_color = self.colors["bg"]
        self.panel_color = self.colors["panel"]
        self.accent_color = self.colors["accent"]
        self.text_primary = self.colors["text_primary"]
        self.text_muted = self.colors["text_muted"]

        self.root.configure(bg=self.bg_color)

        self.obj_frame = None
        self.constraints_frame = None
        self.calculate_button = None
        self.constraint_entries = []
        self.obj_coeff_entries = []

        self.configure_styles()
        self.init_ui()
        self.controller = TwoPhaseMethodController(self)

        center_window(self.root)
        self.root.mainloop()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.bg_color, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            font=("Helvetica", 11, "bold"),
            padding=(12, 8),
            background=self.panel_color,
            foreground=self.text_primary,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.accent_color)],
            foreground=[("selected", "#0b132b")],
        )
        style.configure(
            "TCombobox",
            fieldbackground=self.colors["input"],
            background=self.panel_color,
            foreground=self.text_primary,
            arrowcolor=self.text_primary,
            bordercolor=self.accent_color,
        )
        style.map("TCombobox", fieldbackground=[("readonly", self.colors["input"])] )
        style.configure("TFrame", background=self.bg_color)
        style.configure("TLabel", background=self.panel_color, foreground=self.text_primary)
        style.configure(
            "TLabelframe",
            background=self.panel_color,
            foreground=self.text_primary,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "TLabelframe.Label",
            background=self.panel_color,
            foreground=self.text_primary,
            font=("Helvetica", 11, "bold"),
        )

    def create_entry(self, parent_frame, width=10):
        entry = tk.Entry(
            parent_frame,
            width=width,
            bg=self.colors["input"],
            fg=self.text_primary,
            insertbackground=self.accent_color,
            highlightthickness=0,
            relief="flat",
        )
        entry.pack(side=tk.LEFT, padx=6, pady=6)
        entry.config(highlightbackground=self.accent_color, highlightcolor=self.accent_color, bd=1)
        return entry

    def create_entries(self, parent_frame, num_vars):
        return [self.create_entry(parent_frame) for _ in range(num_vars)]

    def create_objective_entries(self, num_vars):
        if self.obj_frame:
            self.obj_frame.destroy()
        obj_frame = tk.Frame(self.frame, bg=self.panel_color, bd=1, relief="solid")
        obj_frame.pack(pady=10)
        self.obj_frame = obj_frame

        tk.Label(
            obj_frame,
            text="Función Objetivo:",
            bg=self.panel_color,
            fg=self.text_primary,
            font=("Helvetica", 16, "bold"),
        ).pack(side=tk.LEFT, padx=8)

        self.opt_type = ttk.Combobox(obj_frame, values=["Maximizar", "Minimizar"], width=12, style="TCombobox")
        self.opt_type.current(0)
        self.opt_type.pack(side=tk.LEFT, padx=5)

        entry_labels_frame = tk.Frame(obj_frame, bg=self.panel_color)
        entry_labels_frame.pack(pady=5)

        self.obj_coeff_entries = []
        for i in range(num_vars):
            entry = self.create_entry(entry_labels_frame, width=7)
            self.obj_coeff_entries.append(entry)

            label = tk.Label(
                entry_labels_frame,
                text=f"x{i + 1}",
                bg=self.panel_color,
                fg=self.text_primary,
                font=("Helvetica", 14),
            )
            label.pack(side=tk.LEFT, padx=5)

    def create_constraint_entries(self, num_constraints, num_vars):
        if self.constraints_frame:
            self.constraints_frame.destroy()
        constraints_frame = tk.Frame(self.frame, bg=self.panel_color, bd=1, relief="solid")
        constraints_frame.pack(pady=10, fill="x")
        self.constraints_frame = constraints_frame   

        tk.Label(
            constraints_frame,
            text="Restricciones:",
            bg=self.panel_color,
            fg=self.text_primary,
            font=("Helvetica", 16, "bold"),
        ).pack(anchor="w", padx=8, pady=6)

        self.constraint_entries = []
        for i in range(num_constraints): 
            constraint_frame = tk.Frame(constraints_frame, bg=self.panel_color)
            constraint_frame.pack(pady=5, fill="x")

            tk.Label(
                constraint_frame,
                text=f"Restricción {i + 1}:",
                bg=self.panel_color,
                fg=self.text_primary,
                font=("Helvetica", 12, "bold"),
            ).pack(side=tk.LEFT, padx=5)

            coeff_entries = []
            coeff_labels_frame = tk.Frame(constraint_frame, bg=self.panel_color)
            coeff_labels_frame.pack(side=tk.LEFT)

            coeff_entries = []
            for j in range(num_vars):
                entry = self.create_entry(coeff_labels_frame, width=6)
                coeff_entries.append(entry)
                label = tk.Label(
                    coeff_labels_frame,
                    text=f"x{j + 1}",
                    bg=self.panel_color,
                    fg=self.text_primary,
                    font=("Helvetica", 14),
                )
                label.pack(side=tk.LEFT, padx=2)

            sign = ttk.Combobox(constraint_frame, values=[">=", "=", "<="], width=3, style="TCombobox")
            sign.current(0)
            sign.pack(side=tk.LEFT, padx=5)
            rhs_entry = self.create_entry(constraint_frame, width=6)
            self.constraint_entries.append(
                {
                    "coeff_entries": coeff_entries,
                    "sign": sign,
                    "rhs": rhs_entry,
                }
            )

    def create_calculate_button(self, command):
        if self.calculate_button:
            self.calculate_button.destroy()
        calculate_button = tk.Button(
            self.frame,
            text="Calcular Solución",
            command=command,
            bg=self.accent_color,
            fg="#0b132b",
            font=("Helvetica", 14, "bold"),
            relief="flat",
            bd=0,
            padx=14,
            pady=8,
            activebackground="#38bdf8",
        )
        calculate_button.config(borderwidth=0, highlightthickness=0)
        calculate_button.pack(pady=10)
        self.calculate_button = calculate_button

    def create_back_button(self):
        back_button = tk.Button(
            self.frame,
            text="Volver",
            command=self.on_back,
            bg=self.panel_color,
            fg=self.text_primary,
            font=("Helvetica", 14, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=5,
            activebackground="#1f2937",
        )
        back_button.config(borderwidth=0, highlightthickness=0)
        back_button.pack(pady=6)

    def init_ui(self):
        self.frame = tk.Frame(self.root, bg=self.bg_color)
        self.frame.pack(expand=True, fill="both")
        tk.Label(
            self.frame,
            text="Calculadora",
            font=("Helvetica", 28, "bold"),
            bg=self.bg_color,
            fg=self.text_primary,
        ).pack(pady=(30, 6))
        self.subtitle_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 16),
            bg=self.bg_color,
            fg=self.text_muted,
        )
        self.subtitle_label.pack(pady=(0, 20))
        self.init_input_section()
        self.create_back_button()
        self.result_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.result_frame.pack(pady=20)

        self.footer_label = tk.Label(
            self.root,
            text="© Felipe Vernal · Sofía Sánchez · Johan Barreto",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.text_muted,
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=20)

    def init_input_section(self):
        self.input_frame = tk.Frame(self.frame, bg=self.bg_color)
        self.input_frame.pack(pady=20)
        self.num_vars_entry = self.create_labeled_entry("Número de Variables:", font_size=18)
        self.num_constraints_entry = self.create_labeled_entry("Número de Restricciones:")
        self.generate_button = tk.Button(
            self.input_frame,
            text="Crear Matriz",
            command=self.on_generate_matrix,
            bg=self.panel_color,
            fg=self.text_primary,
            font=("Helvetica", 12, "bold"),
            relief="flat",
            bd=0,
            padx=12,
            pady=6,
            activebackground="#1f2937",
        )
        self.generate_button.config(borderwidth=0, highlightthickness=0)
        self.generate_button.pack(pady=10)

    def create_labeled_entry(self, label_text, font_size=14):
        frame = tk.Frame(self.input_frame, bg=self.bg_color)
        frame.pack(pady=2)
        label = tk.Label(
            frame,
            text=label_text,
            bg=self.bg_color,
            fg=self.text_primary,
            font=("Helvetica", font_size, "bold"),
        )
        label.pack(side=tk.LEFT, padx=5)
        return self.create_entry(frame)

    def on_generate_matrix(self):
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        try:
            num_vars = int(self.num_vars_entry.get())
            num_constraints = int(self.num_constraints_entry.get())
        except ValueError:
            self.subtitle_label.config(text="")
            self.display_result("Número de variables o restricciones inválido.")
            return

        if num_vars < 2:
            self.subtitle_label.config(text="")
            self.display_result("Debe ingresar al menos 2 variables.")
            return

        if num_vars == 2:
            self.subtitle_label.config(text="Método Gráfico")
            self.root.destroy()
            from view.GraphicMethodView import GraphicMethodView

            GraphicMethodView(initial_restrictions=num_constraints)
            return

        self.subtitle_label.config(text="Método de las Dos Fases")

        self.constraint_entries = []
        self.obj_coeff_entries = []
        self.controller.create_matrix_entries(num_vars, num_constraints)

    def on_back(self):
        self.root.destroy()
        from view.TwoPhaseMethodView import TwoPhaseMethodView

        TwoPhaseMethodView()

    def display_result(self, result):
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        if isinstance(result, str):
            tk.Label(
                self.result_frame,
                text=result,
                justify=tk.LEFT,
                bg=self.bg_color,
                fg=self.text_primary,
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
            ttk.Label(phase_frame, text="Sin iteraciones", background=self.bg_color, foreground=self.text_primary).pack(pady=10)
            return

        for idx, tableau in enumerate(phase_tableaus):
            group = ttk.LabelFrame(phase_frame, text=f"Iteración {idx + 1}")
            group.pack(fill="both", expand=True, padx=10, pady=5)
            self.display_tableau(group, tableau)

    def display_solution(self, notebook, solution):
        solution_frame = ttk.Frame(notebook)
        notebook.add(solution_frame, text="Solución")

        ttk.Label(
            solution_frame,
            text=f"Valor óptimo de Z: {solution.get('Z', 0)}",
            font=("Helvetica", 14),
            background=self.bg_color,
            foreground=self.text_primary,
        ).pack(pady=10)
        for i, val in enumerate(solution.get("X", [])):
            ttk.Label(
                solution_frame,
                text=f"X{i + 1} = {val}",
                background=self.bg_color,
                foreground=self.text_primary,
            ).pack()

    def display_tableau(self, parent, tableau):
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        headers = tableau[0]
        for col, header in enumerate(headers):
            cell = ttk.Label(
                frame,
                text=header,
                borderwidth=1,
                relief="solid",
                padding=5,
                background=self.panel_color,
                foreground=self.text_primary,
            )
            cell.grid(row=0, column=col, sticky="nsew")

        for row_idx, row in enumerate(tableau[1:], start=1):
            for col_idx, value in enumerate(row):
                bg_color = "#0b1220" if row_idx != len(tableau) - 1 else "#1d4ed8"
                cell = ttk.Label(
                    frame,
                    text=str(value),
                    borderwidth=1,
                    relief="solid",
                    padding=5,
                    background=bg_color,
                    foreground=self.text_primary,
                )
                cell.grid(row=row_idx, column=col_idx, sticky="nsew")

        for col in range(len(headers)):
            frame.grid_columnconfigure(col, weight=1)

