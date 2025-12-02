from model.GraphicMethodModel import GraphicMethodModel


class GraphicMethodController:
    def __init__(self):
        self.model = GraphicMethodModel()

    def solve(self, obj_type, coef_x1, coef_x2, restrictions):
        """Resuelve el problema de programación lineal."""
        self.model.set_objective(obj_type, coef_x1, coef_x2)
        self.model.set_restrictions(restrictions)
        return self.model.solve()