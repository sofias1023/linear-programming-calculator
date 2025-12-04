import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from scipy.optimize import linprog
from utils.center_window import center_window
from scipy.spatial import ConvexHull


class GraphicMethodView:
    def __init__(self, initial_restrictions=0):
        self.colors = {
            "bg": "#0f172a",
            "panel": "#111827",
            "accent": "#22d3ee",
            "accent_active": "#38bdf8",
            "text": "#e5e7eb",
            "muted": "#9ca3af",
            "input": "#0b1220",
        }

        self.root = self.create_root_window()
        self.main_frame = self.create_main_frame()
        self.controls_frame = self.create_controls_frame()
        self.graph_frame = self.create_graph_frame()
        self.restrictions = []
        self.initial_restrictions = max(0, initial_restrictions)

        self.create_widgets()
        center_window(self.root)
        self.root.mainloop()

    def create_root_window(self):
        root = tk.Tk()
        root.title("Calculadora - Método Gráfico")
        root.state('zoomed')
        root.configure(bg=self.colors["bg"])
        return root

    def create_main_frame(self):
        main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        main_frame.pack(expand=True, fill=tk.BOTH)
        return main_frame

    def create_controls_frame(self):
        controls_frame = tk.Frame(self.main_frame, bg=self.colors["panel"], bd=1, relief="solid")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=12, pady=12)
        return controls_frame

    def create_graph_frame(self):
        graph_frame = tk.Frame(self.main_frame, bg=self.colors["bg"])
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=12, pady=12)
        return graph_frame

    def create_widgets(self):
        self.create_style()
        self.create_back_button()
        self.create_title_label()
        self.create_objective_function_widgets()
        self.create_coefficient_widgets()
        self.create_restrictions_widgets()
        self.create_calculate_button()
        self.create_graph_widgets()
        self.create_footer_label()

    def create_style(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "TButton",
            font=("Helvetica", 10, "bold"),
            padding=7,
            background=self.colors["accent"],
            foreground="#0b132b",
            relief="flat",
        )
        self.style.map("TButton", background=[("active", self.colors["accent_active"])])
        self.style.configure(
            "TEntry",
            padding=5,
            font=("Helvetica", 10),
            fieldbackground=self.colors["input"],
            foreground=self.colors["text"],
        )
        self.style.map("TEntry", fieldbackground=[("focus", "#0b1220")])
        self.style.configure(
            "TRadiobutton",
            font=("Helvetica", 10),
            padding=5,
            background=self.colors["panel"],
            foreground=self.colors["text"],
            relief="flat",
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=self.colors["input"],
            background=self.colors["panel"],
            foreground=self.colors["text"],
            arrowcolor=self.colors["text"],
            bordercolor=self.colors["accent"],
        )

    def create_entry(self, parent, width=5):
        return ttk.Entry(parent, width=width, style="TEntry")

    def create_back_button(self):
        self.back_button = ttk.Button(self.controls_frame, text="Volver", command=self.volver_al_menu_anterior)
        self.back_button.pack(pady=20, padx=10, anchor="w")

    def create_title_label(self):
        title_label = tk.Label(
            self.controls_frame,
            text="Calculadora",
            font=("Helvetica", 24, "bold"),
            bg=self.colors["panel"],
            fg=self.colors["text"],
        )
        title_label.pack(pady=(10, 0))

        subtitle_label = tk.Label(
            self.controls_frame,
            text="Método Gráfico",
            font=("Helvetica", 14),
            bg=self.colors["panel"],
            fg=self.colors["muted"],
        )
        subtitle_label.pack(pady=(0, 20))

    def create_objective_function_widgets(self):
        self.obj_type = tk.StringVar(value="max")
        obj_frame = tk.Frame(self.controls_frame, bg=self.colors["panel"])
        obj_frame.pack(pady=10)
        tk.Label(
            obj_frame,
            text="Z:",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Helvetica", 12, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        self.create_radio_buttons(obj_frame)

    def create_radio_buttons(self, obj_frame):
        def on_enter(event):
            event.widget.config(background="#1f2937", foreground=self.colors["text"])

        def on_leave(event):
            event.widget.config(background=self.colors["panel"], foreground=self.colors["text"])

        radio_max = ttk.Radiobutton(obj_frame, text="Max", style="TRadiobutton", variable=self.obj_type, value="max")
        radio_max.pack(side=tk.LEFT, padx=5)
        radio_max.bind("<Enter>", on_enter)
        radio_max.bind("<Leave>", on_leave)

        radio_min = ttk.Radiobutton(obj_frame, text="Min", style="TRadiobutton", variable=self.obj_type, value="min")
        radio_min.pack(side=tk.LEFT, padx=5)
        radio_min.bind("<Enter>", on_enter)
        radio_min.bind("<Leave>", on_leave)

    def create_coefficient_widgets(self):
        coef_frame = tk.Frame(self.controls_frame, bg=self.colors["panel"])
        coef_frame.pack(pady=10)
        self.coef_x1 = self.create_entry(coef_frame)
        self.coef_x1.pack(side=tk.LEFT, padx=5)
        tk.Label(
            coef_frame,
            text="x1",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Helvetica", 12, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        self.coef_x2 = self.create_entry(coef_frame)
        self.coef_x2.pack(side=tk.LEFT, padx=5)
        tk.Label(
            coef_frame,
            text="x2",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Helvetica", 12, "bold"),
        ).pack(side=tk.LEFT, padx=5)

    def create_restrictions_widgets(self):
        restrictions_frame = tk.Frame(self.controls_frame, bg=self.colors["panel"])
        restrictions_frame.pack(pady=10, fill=tk.X)

        header_frame = tk.Frame(restrictions_frame, bg=self.colors["panel"])
        header_frame.pack(fill=tk.X)

        tk.Label(
            header_frame,
            text="Restricciones",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Helvetica", 12, "bold"),
        ).pack(side=tk.LEFT, padx=5)

        self.add_restriction_button = ttk.Button(
            header_frame, text="Agregar Restricción", command=self.add_restriction
        )
        self.add_restriction_button.pack(side=tk.RIGHT, pady=(0, 10))

        self.restrictions_container = tk.Frame(restrictions_frame, bg=self.colors["panel"])
        self.restrictions_container.pack(fill=tk.X, pady=(8, 0))

        for _ in range(self.initial_restrictions):
            self.add_restriction()

    def create_calculate_button(self):
        self.calculate_button = ttk.Button(self.controls_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(pady=20)

    def create_graph_widgets(self):
        self.figure, self.ax = plt.subplots(figsize=(6, 4), facecolor=self.colors["bg"])
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.result_label = tk.Label(
            self.graph_frame,
            text="",
            font=("Helvetica", 14),
            bg=self.colors["bg"],
            fg=self.colors["text"],
        )
        self.result_label.pack(pady=10)

    def create_footer_label(self):
        footer_label = tk.Label(
            self.root,
            text="© Felipe Bernal · Sofía Sánchez · Johan Barreto",
            font=("Helvetica", 10),
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        )
        footer_label.pack(side=tk.BOTTOM, pady=20)

    def volver_al_menu_anterior(self):
        """Cierra la ventana actual y vuelve al menú anterior."""
        self.root.destroy()
        from view.TwoPhaseMethodView import TwoPhaseMethodView  # Importación aquí

        TwoPhaseMethodView()

    def add_restriction(self):
        restriction_frame = tk.Frame(self.restrictions_container, bg=self.colors["panel"])
        restriction_frame.pack(pady=5, anchor="w")
        self.create_restriction_fields(restriction_frame)

    def create_restriction_fields(self, frame):
        tk.Label(
            frame,
            text="x1:",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Helvetica", 12, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        coef_x1 = self.create_entry(frame, width=3)
        coef_x1.pack(side=tk.LEFT, padx=5)

        tk.Label(
            frame,
            text="x2:",
            bg=self.colors["panel"],
            fg=self.colors["text"],
            font=("Helvetica", 12, "bold"),
        ).pack(side=tk.LEFT, padx=5)
        coef_x2 = self.create_entry(frame, width=3)
        coef_x2.pack(side=tk.LEFT, padx=5)
       
        inequality_type = ttk.Combobox(frame, values=["≤", "≥", "="], width=3, style="TCombobox")
        inequality_type.current(0)
        inequality_type.pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Límite:", bg=self.colors["panel"], fg=self.colors["text"]).pack(side=tk.LEFT, padx=5)
        limit = self.create_entry(frame, width=10)
        limit.pack(side=tk.LEFT, padx=5)

        self.restrictions.append((coef_x1, coef_x2, inequality_type, limit))


    def parse_float(self, value, error_message):
        try:
            return float(value.strip())
        except ValueError as exc:
            raise ValueError(error_message) from exc

    def calculate(self):
        """Recopila los datos y los envía al controlador."""
        try:
            obj_type = self.obj_type.get()
            coef_x1 = self.parse_float(self.coef_x1.get(), "Por favor, ingresa valores numéricos válidos.")
            coef_x2 = self.parse_float(self.coef_x2.get(), "Por favor, ingresa valores numéricos válidos.")

            restrictions = []
            for restriction in self.restrictions:
                coef1 = self.parse_float(
                    restriction[0].get(),
                    "Por favor, ingresa valores numéricos válidos para las restricciones.",
                )
                coef2 = self.parse_float(
                    restriction[1].get(),
                    "Por favor, ingresa valores numéricos válidos para las restricciones.",
                )
                limit = self.parse_float(
                    restriction[3].get(),
                    "Por favor, ingresa valores numéricos válidos para las restricciones.",
                )

                inequality = restriction[2].get()

                restrictions.append((coef1, coef2, inequality, limit))

            # Graficar y calcular la solución
            self.plot_solution(coef_x1, coef_x2, restrictions, obj_type)
            
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))

    def plot_solution(self, coef_x1, coef_x2, restrictions, obj_type):
        self.ax.clear()
        self.ax.set_facecolor('#0f172a')
        self.ax.set_xlabel('x1', color='#e5e7eb')
        self.ax.set_ylabel('x2', color='#e5e7eb')
        self.ax.spines['bottom'].set_color('#e5e7eb')
        self.ax.spines['top'].set_color('#e5e7eb')
        self.ax.spines['right'].set_color('#e5e7eb')
        self.ax.spines['left'].set_color('#e5e7eb')
        self.ax.tick_params(axis='x', colors='#e5e7eb')
        self.ax.tick_params(axis='y', colors='#e5e7eb')

        x = np.linspace(0, 100, 400)
        feasible_region = []
        for coef1, coef2, inequality, limit in restrictions:
            if abs(coef2) < 1e-9:
                x_val = limit / coef1 if coef1 != 0 else 0
                y_vals = np.linspace(0, max(10, limit * 1.5 if limit >= 0 else 10), 400)
                x_vals = np.full_like(y_vals, x_val)
                self.ax.plot(x_vals, y_vals, label=f"{coef1}x1 {inequality} {limit}")
            else:
                y_vals = (limit - coef1 * x) / coef2
                self.ax.plot(x, y_vals, label=f"{coef1}x1 + {coef2}x2 {inequality} {limit}")
            if inequality == '≤' or inequality == '<=':
                feasible_region.append((coef1, coef2, limit, '<='))
            elif inequality == '≥' or inequality == '>=':
                feasible_region.append((coef1, coef2, limit, '>='))
            else:
                feasible_region.append((coef1, coef2, limit, '='))

        self.ax.axhline(0, color='#e5e7eb')
        self.ax.axvline(0, color='#e5e7eb')
        self.ax.grid(color='#1f2937')

        corners = []
        for i in range(len(feasible_region)):
            for j in range(i + 1, len(feasible_region)):
                coef1_i, coef2_i, limit_i, sign_i = feasible_region[i]
                coef1_j, coef2_j, limit_j, sign_j = feasible_region[j]
                det = coef1_i * coef2_j - coef1_j * coef2_i
                if det == 0:
                    continue
                x_int = (limit_i * coef2_j - limit_j * coef2_i) / det
                y_int = (coef1_i * limit_j - coef1_j * limit_i) / det
                corners.append((x_int, y_int))

        corners.append((0, 0))
        corners.extend([(0, limit / coef2) for coef1, coef2, _, limit in restrictions if coef2 != 0])
        corners.extend([(limit / coef1, 0) for coef1, _, _, limit in restrictions if coef1 != 0])
        corners = [corner for corner in corners if corner[0] >= 0 and corner[1] >= 0]

        feasible_points = []
        for corner in corners:
            if all(self.satisfies_restriction(corner, coef1, coef2, limit, sign) for coef1, coef2, limit, sign in feasible_region):
                feasible_points.append(corner)

        if len(feasible_points) >= 3:
            hull = ConvexHull(feasible_points)
            polygon_points = [feasible_points[i] for i in hull.vertices]
            polygon = Polygon(polygon_points, closed=True, fill=True, color='#22d3ee', alpha=0.2)
            self.ax.add_patch(polygon)
        elif feasible_points:
            self.ax.fill(
                [p[0] for p in feasible_points],
                [p[1] for p in feasible_points],
                color=self.colors["accent"],
                alpha=0.15,
            )

        result = self.calculate_optimal_solution(coef_x1, coef_x2, feasible_region, obj_type)

        if result:
            x_opt, y_opt, z_opt = result
            self.ax.plot(x_opt, y_opt, 'ro', label='Óptimo')
            self.result_label.config(text=f"Solución óptima: x1 = {x_opt:.2f}, x2 = {y_opt:.2f}, Z = {z_opt:.2f}")
        else:
            self.result_label.config(text="No se encontró solución óptima")

        self.ax.legend(facecolor='#111827', edgecolor='#22d3ee', labelcolor='#e5e7eb')
        self.figure.tight_layout()
        self.canvas.draw()

    def calculate_optimal_solution(self, coef_x1, coef_x2, restrictions, obj_type):
        c = [-coef_x1, -coef_x2] if obj_type == 'max' else [coef_x1, coef_x2]
        A = []
        b = []

        for coef1, coef2, limit, sign in restrictions:
            if sign in ('<=', '≤'):
                A.append([coef1, coef2])
                b.append(limit)
            elif sign in ('>=', '≥'):
                A.append([-coef1, -coef2])
                b.append(-limit)
            else:
                A.append([coef1, coef2])
                b.append(limit)
                A.append([-coef1, -coef2])
                b.append(-limit)
        bounds = [(0, None), (0, None)]
        result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
        if result.success:
            x_opt, y_opt = result.x
            z_opt = coef_x1 * x_opt + coef_x2 * y_opt
            return x_opt, y_opt, z_opt
        return None

    def satisfies_restriction(self, point, coef1, coef2, limit, sign):
        x1, x2 = point
        if sign == '<=':
            return coef1 * x1 + coef2 * x2 <= limit + 1e-6
        elif sign == '>=':
            return coef1 * x1 + coef2 * x2 >= limit - 1e-6
        else:
            return abs(coef1 * x1 + coef2 * x2 - limit) < 1e-6