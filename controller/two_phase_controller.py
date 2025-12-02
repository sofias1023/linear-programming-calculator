from model.two_phase_model import TwoPhaseMethodModel

class TwoPhaseMethodController:
    def __init__(self, view):
        self.view = view

    def create_matrix_entries(self, num_vars, num_constraints):
        self.view.create_objective_entries(num_vars)
        self.view.create_constraint_entries(num_constraints, num_vars)
        self.view.create_calculate_button(self.calculate_solution)

    def get_entries_values(self, entries):
        values = []
        for entry in entries:
            value = entry.get()
            try:
                num = float(value)
            except ValueError:
                num = 0
            values.append(num)
        return values

    def get_constraints_values(self, num_constraints, num_vars):
        A = []
        b = []
        for cons in self.view.constraint_entries:
            coeff_entries = cons.get("coeff_entries", [])
            coeffs = self.get_entries_values(coeff_entries[:num_vars])
            sign = cons.get("sign").get()
            try:
                rhs = float(cons.get("rhs").get())
            except ValueError:
                rhs = 0
            if sign == ">=":
                A.append([-c for c in coeffs])
                b.append(-rhs)
            elif sign == "<=":
                A.append(coeffs)
                b.append(rhs)
            elif sign == "=":
                A.append(coeffs)
                b.append(rhs)
                A.append([-c for c in coeffs])
                b.append(-rhs)
        return A, b

    def calculate_solution(self):
        try:
            num_vars = int(self.view.num_vars_entry.get())
            num_constraints = int(self.view.num_constraints_entry.get())
        except ValueError:
            self.view.display_result("Número de variables o restricciones inválido.")
            return

        obj_type = self.view.opt_type.get()        
        objective_coeffs = self.get_entries_values(self.view.obj_coeff_entries)
        constraints = self.get_constraints(num_vars)

        model = TwoPhaseMethodModel(num_vars, num_constraints, obj_type, objective_coeffs, constraints)
        result = model.solve()

        self.view.display_result(result)

    def get_constraints(self, num_vars):
        constraints = []
        for cons in self.view.constraint_entries:
            coeffs = self.get_entries_values(cons.get("coeff_entries", [])[:num_vars])
            relation = cons.get("sign").get()
            try:
                rhs = float(cons.get("rhs").get())
            except ValueError:
                rhs = 0
            constraints.append((coeffs, relation, rhs))
        return constraints
