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
    def __init__(self):
        self.root = self.create_root_window()
        self.main_frame = self.create_main_frame()
        self.controls_frame = self.create_controls_frame()
        self.graph_frame = self.create_graph_frame()
        self.restrictions = []

        self.create_widgets()
        center_window(self.root)
        self.root.mainloop()

    def create_root_window(self):
        root = tk.Tk()
        root.title("Método Gráfico")
        root.state('zoomed')
        root.configure(bg="#2e2e2e")
        return root

    def create_main_frame(self):
        main_frame = tk.Frame(self.root, bg="#2e2e2e")
        main_frame.pack(expand=True, fill=tk.BOTH)
        return main_frame

    def create_controls_frame(self):
        controls_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        return controls_frame

    def create_graph_frame(self):
        graph_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
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
        self.style.configure("TButton", font=("Helvetica", 10, "bold"), padding=5, background="#3700b3", foreground="#000000", relief="flat")
        self.style.map("TButton", background=[("active", "#45a049")])
        self.style.configure("TEntry", padding=5, font=("Helvetica", 10), fieldbackground="#ffffff")
        self.style.map("TEntry", fieldbackground=[("focus", "#3700b3")])
        self.style.configure("TRadiobutton", font=("Helvetica", 10), padding=5, background="#2e2e2e", foreground="#ffffff", relief="flat")

    def create_back_button(self):
        self.back_button = ttk.Button(self.controls_frame, text="Volver al Menú Anterior", command=self.volver_al_menu_anterior)
        self.back_button.pack(pady=20)

    def create_title_label(self):
        title_label = tk.Label(self.controls_frame, text="Método Gráfico", font=("Helvetica", 24, "bold"), bg="#2e2e2e", fg="#ffffff")
        title_label.pack(pady=20)

    def create_objective_function_widgets(self):
        self.obj_type = tk.StringVar(value="max")
        obj_frame = tk.Frame(self.controls_frame, bg="#2e2e2e")
        obj_frame.pack(pady=10)
        tk.Label(obj_frame, text="Z:", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.create_radio_buttons(obj_frame)

    def create_radio_buttons(self, obj_frame):
        def on_enter(event):
            event.widget.config(background="#3a3a3a", foreground="#ffffff")

        def on_leave(event):
            event.widget.config(background="#2e2e2e", foreground="#000000")

        radio_max = ttk.Radiobutton(obj_frame, text="Max", style="TRadiobutton", variable=self.obj_type, value="max")
        radio_max.pack(side=tk.LEFT, padx=5)
        radio_max.bind("<Enter>", on_enter)
        radio_max.bind("<Leave>", on_leave)

        radio_min = ttk.Radiobutton(obj_frame, text="Min", style="TRadiobutton", variable=self.obj_type, value="min")
        radio_min.pack(side=tk.LEFT, padx=5)
        radio_min.bind("<Enter>", on_enter)
        radio_min.bind("<Leave>", on_leave)

    def create_coefficient_widgets(self):
        coef_frame = tk.Frame(self.controls_frame, bg="#2e2e2e")
        coef_frame.pack(pady=10)
        self.coef_x1 = ttk.Entry(coef_frame, width=5, style="TEntry")
        self.coef_x1.pack(side=tk.LEFT, padx=5)
        tk.Label(coef_frame, text="x1", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.coef_x2 = ttk.Entry(coef_frame, width=5, style="TEntry")
        self.coef_x2.pack(side=tk.LEFT, padx=5)
        tk.Label(coef_frame, text="x2", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)

    def create_restrictions_widgets(self):
        restrictions_frame = tk.Frame(self.controls_frame, bg="#2e2e2e")
        restrictions_frame.pack(pady=10)
        self.add_restriction_button = ttk.Button(restrictions_frame, text="Agregar Restricción", command=self.add_restriction)
        self.add_restriction_button.pack(pady=10)

    def create_calculate_button(self):
        self.calculate_button = ttk.Button(self.controls_frame, text="Calcular", command=self.calculate)
        self.calculate_button.pack(pady=20)

    def create_graph_widgets(self):
        self.figure, self.ax = plt.subplots(figsize=(6, 4), facecolor="#2e2e2e")
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        self.result_label = tk.Label(self.graph_frame, text="", font=("Helvetica", 14), bg="#2e2e2e", fg="#ffffff")
        self.result_label.pack(pady=10)

    def create_footer_label(self):
        footer_label = tk.Label(self.root, text="© Jhonattan Aponte - Karen Garzon", font=("Helvetica", 10), bg="#2e2e2e", fg="#888888")
        footer_label.pack(side=tk.BOTTOM, pady=20)

    def volver_al_menu_anterior(self):
        """Cierra la ventana actual y vuelve al menú anterior."""
        self.root.destroy()
        from view.MainView import MainView  # Importación aquí
        MainView()

    def add_restriction(self):
        restriction_frame = tk.Frame(self.controls_frame, bg="#2e2e2e")
        restriction_frame.pack(pady=5)
        self.create_restriction_fields(restriction_frame)

    def create_restriction_fields(self, frame):
        coef_x1 = ttk.Entry(frame, width=3)
        coef_x1.pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="x1:", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)

        coef_x2 = ttk.Entry(frame, width=3)
        coef_x2.pack(side=tk.LEFT, padx=5)
        tk.Label(frame, text="x2:", bg="#2e2e2e", fg="#ffffff", font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=5)

        inequality_type = ttk.Combobox(frame, values=["≤", "≥", "="], width=3)
        inequality_type.current(0)
        inequality_type.pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="Límite:", bg="#2e2e2e", fg="#ffffff").pack(side=tk.LEFT, padx=5)
        limit = ttk.Entry(frame, width=10)
        limit.pack(side=tk.LEFT, padx=5)

        self.restrictions.append((coef_x1, coef_x2, inequality_type, limit))

    def calculate(self):
        """Recopila los datos y los envía al controlador."""
        try:
            # Obtener la función objetivo
            obj_type = self.obj_type.get()
            coef_x1 = self.coef_x1.get().strip()  # Eliminar espacios innecesarios
            coef_x2 = self.coef_x2.get().strip()

            # Verificar si los valores son numéricos
            if not coef_x1.replace('.', '', 1).isdigit() or not coef_x2.replace('.', '', 1).isdigit():
                raise ValueError("Por favor, ingresa valores numéricos válidos.")

            coef_x1 = float(coef_x1)
            coef_x2 = float(coef_x2)

            # Obtener las restricciones
            restrictions = []
            for restriction in self.restrictions:
                coef1 = restriction[0].get().strip()
                coef2 = restriction[1].get().strip()
                limit = restriction[3].get().strip()

                if not coef1.replace('.', '', 1).isdigit() or not coef2.replace('.', '',
                                                                                1).isdigit() or not limit.replace('.',
                                                                                                                  '',
                                                                                                                  1).isdigit():
                    raise ValueError("Por favor, ingresa valores numéricos válidos para las restricciones.")

                coef1 = float(coef1)
                coef2 = float(coef2)
                limit = float(limit)

                inequality = restriction[2].get()

                restrictions.append((coef1, coef2, inequality, limit))

            # Graficar y calcular la solución
            self.plot_solution(coef_x1, coef_x2, restrictions, obj_type)

        except ValueError as e:
            print(e)

    def get_restrictions_data(self):
        restrictions = []
        for restriction in self.restrictions:
            coef1 = float(restriction[0].get())
            coef2 = float(restriction[1].get())
            inequality = restriction[2].get()
            limit = float(restriction[3].get())
            restrictions.append((coef1, coef2, inequality, limit))
        return restrictions

    def plot_solution(self, coef_x1, coef_x2, restrictions, obj_type):
        self.ax.clear()
        x = np.linspace(0, 100, 400)  # Usamos un rango amplio para cubrir posibles valores
        self.plot_restrictions(x, restrictions)
        self.plot_feasible_region(restrictions)
        self.plot_objective_function(x, coef_x1, coef_x2)
        x1_opt, x2_opt, z_opt = self.calculate_optimal_solution(coef_x1, coef_x2, restrictions, obj_type)
        self.plot_optimal_point(x1_opt, x2_opt)
        self.show_results(x1_opt, x2_opt, z_opt)
        self.adjust_graph_scale(restrictions, x1_opt, x2_opt)
        self.canvas.draw()

    def plot_optimal_point(self, x1_opt, x2_opt):
        self.ax.scatter(x1_opt, x2_opt, color="red", marker='*', s=200, zorder=5)
        self.ax.annotate(f"Óptimo ({x1_opt:.2f}, {x2_opt:.2f})", (x1_opt, x2_opt), textcoords="offset points",
                         xytext=(0, 10), ha='center', color="red", fontsize=12, fontweight='bold')

    def plot_feasible_region(self, restrictions):
        import numpy as np
        from itertools import combinations

        # Generar puntos de intersección entre las restricciones
        puntos = []
        for i in range(len(restrictions)):
            for j in range(i + 1, len(restrictions)):
                coef1_a, coef2_a, _, limit_a = restrictions[i]
                coef1_b, coef2_b, _, limit_b = restrictions[j]
                A = np.array([[coef1_a, coef2_a],
                              [coef1_b, coef2_b]])
                b = np.array([limit_a, limit_b])
                if np.linalg.det(A) != 0:
                    punto = np.linalg.solve(A, b)
                    if np.all(punto >= -0.1):  # Considera solo puntos en el primer cuadrante
                        puntos.append(punto)

        # Añadir intersecciones con los ejes
        for coef1, coef2, inequality, limit in restrictions:
            if coef1 != 0:
                x_intercept = limit / coef1
                if x_intercept >= -0.1:
                    puntos.append([x_intercept, 0])
            if coef2 != 0:
                y_intercept = limit / coef2
                if y_intercept >= -0.1:
                    puntos.append([0, y_intercept])

        # Filtrar puntos que satisfacen todas las restricciones
        vertices = []
        for punto in puntos:
            cumple = True
            for coef1, coef2, inequality, limit in restrictions:
                expr = coef1 * punto[0] + coef2 * punto[1]
                if inequality == "≤" and expr > limit + 1e-5:
                    cumple = False
                    break
                elif inequality == "≥" and expr < limit - 1e-5:
                    cumple = False
                    break
            if cumple:
                vertices.append(punto)

        if vertices:
            # Ordenar los puntos del polígono
            vertices = np.array(vertices)
            hull = ConvexHull(vertices)
            vertices = vertices[hull.vertices]
            # Crear y añadir el polígono a la gráfica
            poligono = Polygon(vertices, color='green', alpha=0.3)
            self.ax.add_patch(poligono)

    def plot_restrictions(self, x, restrictions):
        colores = ["cyan", "magenta", "yellow", "orange", "lime"]
        estilos = ["-", "--", "-.", ":", (0, (5, 5))]
        for idx, (coef1, coef2, inequality, limit) in enumerate(restrictions):
            color = colores[idx % len(colores)]
            estilo = estilos[idx % len(estilos)]
            if coef2 != 0:
                y = (limit - coef1 * x) / coef2
                self.ax.plot(x, y, label=f"{coef1}x₁ + {coef2}x₂ {inequality} {limit}", color=color, linestyle=estilo,
                             linewidth=2)

                # Intersección con el eje X
                if coef1 != 0:
                    x_intercept = limit / coef1
                    if 0 <= x_intercept <= max(x):
                        self.ax.scatter(x_intercept, 0, color=color, zorder=5)
                        self.ax.annotate(f"({x_intercept:.2f}, 0)", (x_intercept, 0), textcoords="offset points",
                                         xytext=(0, -15), ha='center', color=color)

                # Intersección con el eje Y
                if coef2 != 0:
                    y_intercept = limit / coef2
                    if 0 <= y_intercept <= max(x):
                        self.ax.scatter(0, y_intercept, color=color, zorder=5)
                        self.ax.annotate(f"(0, {y_intercept:.2f})", (0, y_intercept), textcoords="offset points",
                                         xytext=(-40, 0), ha='center', color=color)

    def fill_between_area(self, x, y, inequality):
        if inequality == "≤":
            self.ax.fill_between(x, y, 0, color="green", alpha=0.3)  # Zona factible con color verde
        elif inequality == "≥":
            self.ax.fill_between(x, y, 10, color="red", alpha=0.3)  # Zona factible con color rojo



    def plot_objective_function(self, x, coef_x1, coef_x2):
        # Graficar la función objetivo
        y_obj = (10 - coef_x1 * x) / coef_x2
        self.ax.plot(x, y_obj, label=f"Z = {coef_x1}x1 + {coef_x2}x2", linestyle="--", color="yellow", linewidth=2)

    def adjust_graph_scale(self, restrictions, x1_opt, x2_opt):
        # Listas para almacenar los valores de X y Y
        x_values = [x1_opt]
        y_values = [x2_opt]

        # Encontrar intersecciones entre restricciones
        for i in range(len(restrictions)):
            coef1_a, coef2_a, _, limit_a = restrictions[i]
            for j in range(i + 1, len(restrictions)):
                coef1_b, coef2_b, _, limit_b = restrictions[j]
                A = np.array([[coef1_a, coef2_a],
                              [coef1_b, coef2_b]])
                b = np.array([limit_a, limit_b])
                if np.linalg.det(A) != 0:
                    punto = np.linalg.solve(A, b)
                    if np.all(punto >= -0.1):  # Consideramos sólo puntos en el primer cuadrante
                        x_values.append(punto[0])
                        y_values.append(punto[1])

        # Intersecciones con los ejes
        for coef1, coef2, _, limit in restrictions:
            if coef1 != 0:
                x_intercept = limit / coef1
                if x_intercept >= -0.1:
                    x_values.append(x_intercept)
                    y_values.append(0)
            if coef2 != 0:
                y_intercept = limit / coef2
                if y_intercept >= -0.1:
                    x_values.append(0)
                    y_values.append(y_intercept)

        # Valores máximos de X y Y
        max_x = max(x_values)
        max_y = max(y_values)

        # Añadir un margen para mejor visualización
        margen_x = max_x * 0.1 if max_x != 0 else 1
        margen_y = max_y * 0.1 if max_y != 0 else 1

        # Establecer los límites de los ejes con los nuevos valores
        self.ax.set_xlim(0, max_x + margen_x)
        self.ax.set_ylim(0, max_y + margen_y)

        # Configuración estética (puedes ajustar los colores a tu gusto)
        self.ax.set_facecolor("white")
        self.ax.spines['bottom'].set_color('black')
        self.ax.spines['top'].set_color('black')
        self.ax.spines['left'].set_color('black')
        self.ax.spines['right'].set_color('black')
        self.ax.xaxis.label.set_color('black')
        self.ax.yaxis.label.set_color('black')
        self.ax.tick_params(axis='x', colors='black')
        self.ax.tick_params(axis='y', colors='black')
        self.ax.grid(True, linestyle="--", alpha=0.5, color="gray")
        self.ax.set_title("Método Gráfico de Programación Lineal", color="black", fontsize=14)
        self.ax.set_xlabel("Variable $x_1$", color="black", fontsize=12)
        self.ax.set_ylabel("Variable $x_2$", color="black", fontsize=12)
        self.ax.legend(facecolor="white", framealpha=1, edgecolor="black")

    def calculate_optimal_solution(self, coef_x1, coef_x2, restrictions, obj_type):
        A, b = self.convert_restrictions_to_matrix(restrictions)
        c = np.array([coef_x1, coef_x2])
        return self.solve_linear_programming(c, A, b, obj_type)

    def convert_restrictions_to_matrix(self, restrictions):
        A, b = [], []
        for coef1, coef2, inequality, limit in restrictions:
            if inequality == "≤":
                A.append([coef1, coef2])
                b.append(limit)
            elif inequality == "≥":
                A.append([-coef1, -coef2])
                b.append(-limit)
            elif inequality == "=":
                # Agregar restricciones iguales
                A.append([coef1, coef2])
                b.append(limit)
                A.append([-coef1, -coef2])
                b.append(-limit)
        return np.array(A), np.array(b)

    def solve_linear_programming(self, c, A, b, obj_type):
        if obj_type == "max":
            # Se invierte el signo de la función objetivo para maximizar
            res = linprog(-c, A_ub=A, b_ub=b, bounds=(0, None))
        else:
            # Para minimizar se utiliza directamente
            res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

        if res.success:
            return res.x[0], res.x[1], np.dot(c, res.x)
        else:
            messagebox.showerror("Error", "No se pudo encontrar una solución óptima.")
            return 0, 0, 0

    def show_results(self, x1_opt, x2_opt, z_opt):
        self.result_label.config(text=f"Resultado:\nx1 = {x1_opt:.2f}\nx2 = {x2_opt:.2f}\nPor tanto, Z = {z_opt:.2f}")

    def adjust_graph_scale(self, x, restrictions):
        x_vals, y_vals = [], []
        for coef1, coef2, _, _ in restrictions:
            y_vals.append((10 - coef1 * x) / coef2)
        self.ax.set_xlim(0, max(x) + 1)
        self.ax.set_ylim(0, max(y_vals) + 1)
        self.ax.set_xlabel("x1")
        self.ax.set_ylabel("x2")
        self.ax.legend()
        self.ax.grid(True, linestyle="--", alpha=0.6)
        self.ax.set_facecolor("#2e2e2e")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
