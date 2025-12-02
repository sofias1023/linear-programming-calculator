import numpy as np

class TwoPhaseMethodModel:
    def __init__(self, num_vars, num_constraints, opt_type, obj_coeffs, constraints):
        self.num_vars = num_vars
        self.num_constraints = num_constraints
        self.opt_type = opt_type
        self.obj_coeffs = np.array(obj_coeffs, dtype=float)
        self.constraints = constraints

    def solve(self):
        try:
            self._normalize_constraints()
            A, b, artificial_vars = self._setup_initial_tableau()
            if A is None:
                return "Error en la configuración del problema"

            tableau_phase1 = self._solve_phase1(A, b, artificial_vars)
            if isinstance(tableau_phase1, str):
                return tableau_phase1

            if not self._check_phase1_feasibility(tableau_phase1, artificial_vars):
                return "El problema no tiene solución factible"

            tableau_phase1 = self._remove_artificial_variables(tableau_phase1, artificial_vars)
            result = self._solve_phase2(tableau_phase1)
            return self._extract_solution(result)
        except Exception as e:
            return f"Error: {str(e)}"

    def _normalize_constraints(self):
        for i, (coeffs, relation, rhs) in enumerate(self.constraints):
            if rhs < 0:
                self.constraints[i] = ([-x for x in coeffs], relation, -rhs)

    def _setup_initial_tableau(self):
        A_list, artificial_vars = [], []
        b = np.array([cons[2] for cons in self.constraints], dtype=float)
        total_vars = self.num_vars + sum(1 if rel in ('<=', '=') else 2 for _, rel, _ in self.constraints)

        for i, (coeffs, relation, _) in enumerate(self.constraints):
            row = np.zeros(total_vars)
            row[:self.num_vars] = coeffs
            curr_pos = self.num_vars + sum(1 if self.constraints[j][1] in ('<=', '=') else 2 for j in range(i))

            if relation == '<=':
                row[curr_pos] = 1
            elif relation == '>=':
                row[curr_pos], row[curr_pos + 1] = -1, 1
                artificial_vars.append(curr_pos + 1)
            else:
                row[curr_pos] = 1
                artificial_vars.append(curr_pos)

            A_list.append(row)

        return np.array(A_list), b, artificial_vars

    def _remove_artificial_variables(self, tableau, artificial_vars):
        return tableau[:, [i for i in range(tableau.shape[1] - 1) if i not in artificial_vars] + [-1]]

    def _check_phase1_feasibility(self, tableau, artificial_vars):
        return abs(tableau[-1, -1]) < 1e-6

    def _extract_solution(self, tableau):
        solution = np.zeros(self.num_vars)
        for i in range(self.num_vars):
            col = tableau[:-1, i]
            if np.count_nonzero(col) == 1:
                row = np.where(abs(col - 1) < 1e-6)[0]
                if row.size > 0:
                    solution[i] = tableau[row[0], -1]

        z_value = -tableau[-1, -1] if self.opt_type == 'Minimizar' else tableau[-1, -1]
        return {"X": solution.tolist(), "Z": z_value}
