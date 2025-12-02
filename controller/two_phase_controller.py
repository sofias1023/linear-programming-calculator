from scipy.optimize import linprog

class TwoPhaseMethodController:
    def __init__(self, view):
        self.view = view

    def create_matrix_entries(self):
        try:
            num_vars = int(self.view.num_vars_entry.get())
            num_constraints = int(self.view.num_constraints_entry.get())
        except ValueError:
            self.view.display_result("Número de variables o restricciones inválido.")
            return

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

        # Obtener los coeficientes de la función objetivo y las restricciones
        objective_coeffs = self.get_entries_values(self.view.obj_coeff_entries)
        A, b = self.get_constraints_values(num_constraints, num_vars)

        # Obtener el tipo de objetivo: "Maximizar" o "Minimizar"
        obj_type = self.view.opt_type.get()
        if obj_type == "Maximizar":
            objective_coeffs = [-c for c in objective_coeffs]

        # Resolver el problema de LP usando SciPy
        result = linprog(c=objective_coeffs, A_ub=A, b_ub=b, method='highs')

        if not result.success:
            self.view.display_result("No se pudo encontrar una solución óptima.")
            return

        # Mostrar los resultados
        result_text = f"Z = {result.fun}\n"
        for i in range(num_vars):
            result_text += f"x{i+1} = {result.x[i]}\n"
        self.view.display_result(result_text)
