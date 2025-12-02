class GraphicMethodModel:
    def __init__(self):
        self.objective = None
        self.restrictions = []

    def set_objective(self, obj_type, coef_x1, coef_x2):
        """Define la función objetivo."""
        self.objective = {
            "type": obj_type,
            "coef_x1": coef_x1,
            "coef_x2": coef_x2
        }

    def set_restrictions(self, restrictions):
        """Define las restricciones."""
        self.restrictions = restrictions

    def solve(self):
        """Resuelve el problema de programación lineal."""
        # Aquí implementarías el método gráfico
        return "Solución calculada"  # Placeholder