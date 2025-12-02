import tkinter as tk
from tkinter import ttk
from utils.center_window import center_window
from view.GraphicMethodView import GraphicMethodView
from view.TwoPhaseMethodView import TwoPhaseMethodView


class MainView:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora de Métodos")
        self.root.state('zoomed')  # Para Windows

        self.root.configure(bg="#2e2e2e")

        self.frame = tk.Frame(self.root, bg="#2e2e2e")
        self.frame.pack(expand=True)

        self.style = ttk.Style()
        self.style.configure("TButton",
                             font=("Helvetica", 14),
                             padding=10,
                             background="#3700b3",
                             foreground="#000000",  # Cambiar a negro
                             relief="flat")
        self.style.map("TButton",
                       background=[("active", "#6200ee"), ("pressed", "#3700b3")],
                       foreground=[("active", "#000000"), ("pressed", "#000000")]  # Cambiar a negro
                       )

        self.title_label = tk.Label(
            self.frame,
            text="Calculadora de Métodos",
            font=("Helvetica", 24, "bold"),
            bg="#2e2e2e",
            fg="#ffffff"
        )
        self.title_label.pack(pady=30)

        self.graphic_method_button = ttk.Button(
            self.frame,
            text="Método Gráfico",
            command=self.open_graphic_method_view
        )
        self.graphic_method_button.pack(pady=20)

        self.two_phase_method_button = ttk.Button(
            self.frame,
            text="Método Dos Fases",
            command=self.open_two_phase_method_view
        )
        self.two_phase_method_button.pack(pady=20)

        self.footer_label = tk.Label(
            self.root,
            text="© Jhonattan Aponte - Karen Garzon",
            font=("Helvetica", 10),
            bg="#2e2e2e",
            fg="#888888"
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=20)

        center_window(self.root)  # Centrar la ventana en la pantalla
        self.root.mainloop()

    def open_graphic_method_view(self):
        self.root.destroy()  # Cierra la ventana actual
        GraphicMethodView()  # Abre la vista del método gráfico

    def open_two_phase_method_view(self):
        self.root.destroy()  # Cierra la ventana actual
        TwoPhaseMethodView()  # Abre la vista del método de dos fases