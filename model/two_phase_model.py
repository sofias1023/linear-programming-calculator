import numpy as np
from scipy.optimize import linprog

class TwoPhaseMethodModel:
    def __init__(self, num_vars, num_constraints, opt_type, obj_coeffs, constraints):
        self.num_vars = num_vars
        self.num_constraints = num_constraints
        self.opt_type = opt_type
        self.obj_coeffs = np.array(obj_coeffs, dtype=float)
        self.constraints = constraints

    def solve(self):
        try:
            constraints_matrix, rhs, var_names, artificial_indices = self._build_constraint_matrix()
            if constraints_matrix is None:
                return "Error en la configuración del problema"

            lp_solution = self._solve_with_linprog()
            if isinstance(lp_solution, str):
                return lp_solution

            phase1_tableaus = [self._build_phase1_tableau(constraints_matrix, rhs, var_names, artificial_indices)]
            phase2_tableaus = [self._build_phase2_tableau(lp_solution, var_names, artificial_indices)]

            solution = self._format_solution(lp_solution)
            return {
                "phase1_tableaus": phase1_tableaus,
                "phase2_tableaus": phase2_tableaus,
                "solution": solution,
            }
        except Exception as e:
            return f"Error: {str(e)}"

    def _build_constraint_matrix(self):
        variable_names = [f"X{i + 1}" for i in range(self.num_vars)]
        rows = []
        rhs_values = []
        artificial_indices = []
        slack_count = 1
        artificial_count = 1

        for coeffs, relation, rhs in self.constraints:
            row = [0.0 for _ in variable_names]
            for idx, coeff in enumerate(coeffs):
                row[idx] = coeff

            if relation == "<=":
                variable_names.append(f"S{slack_count}")
                self._extend_existing_rows(rows)
                row.append(1.0)
                slack_count += 1
                basic_name = variable_names[-1]
            elif relation == ">=":
                variable_names.append(f"S{slack_count}")
                self._extend_existing_rows(rows)
                row.append(-1.0)
                slack_count += 1

                variable_names.append(f"R{artificial_count}")
                self._extend_existing_rows(rows)
                row.append(1.0)
                artificial_indices.append(len(variable_names) - 1)
                basic_name = variable_names[-1]
                artificial_count += 1
            elif relation == "=":
                variable_names.append(f"R{artificial_count}")
                self._extend_existing_rows(rows)
                row.append(1.0)
                artificial_indices.append(len(variable_names) - 1)
                basic_name = variable_names[-1]
                artificial_count += 1
            else:
                return None, None, None, None

            rows.append({"basic": basic_name, "values": row})
            rhs_values.append(rhs)

        return rows, rhs_values, variable_names, artificial_indices

    def _extend_existing_rows(self, rows):
        for row in rows:
            row["values"].append(0.0)

    def _solve_with_linprog(self):
        A, b = self._build_linprog_matrices()
        objective_coeffs = self.obj_coeffs.copy()
        if self.opt_type == "Maximizar":
            objective_coeffs = -objective_coeffs

        result = linprog(c=objective_coeffs, A_ub=A, b_ub=b, method="highs")

        if not result.success:
            return "No se pudo encontrar una solución óptima."
        return result

    def _build_phase1_tableau(self, constraints_matrix, rhs, variable_names, artificial_indices):
        header = ["V. Básica", "Z", *variable_names, "Solución"]
        tableau = [header]

        objective_row = [1.0] + [-c for c in self.obj_coeffs] + [0.0 for _ in variable_names[len(self.obj_coeffs):]] + [0.0]
        tableau.append(["Z", *objective_row])

        for row_data, rhs_value in zip(constraints_matrix, rhs):
            padded_row = row_data["values"] + [0.0] * (len(variable_names) - len(row_data["values"]))
            tableau.append([row_data["basic"], 0.0, *padded_row, rhs_value])

        zj_row = [0.0 for _ in range(len(variable_names) + 2)]
        tableau.append(["Zj - Cj", *zj_row[1:]])
        return tableau

    def _build_phase2_tableau(self, result, variable_names, artificial_indices):
        filtered_names = [name for idx, name in enumerate(variable_names) if idx not in artificial_indices]

        header = ["V. Básica", "Z", *filtered_names, "Solución"]
        tableau = [header]

        z_value = -result.fun if self.opt_type == "Maximizar" else result.fun
        objective_row = [1.0] + [0.0 for _ in filtered_names] + [z_value]
        tableau.append(["Z", *objective_row])

        solution_row = [0.0 for _ in filtered_names]
        for idx, value in enumerate(result.x):
            if idx < len(solution_row):
                solution_row[idx] = value
        tableau.append(["Sol", 0.0, *solution_row, z_value])

        zj_row = [0.0 for _ in range(len(filtered_names) + 2)]
        tableau.append(["Zj - Cj", *zj_row[1:]])
        return tableau

    def _build_linprog_matrices(self):
        A = []
        b = []
        for coeffs, relation, rhs in self.constraints:
            if relation == ">=":
                A.append([-c for c in coeffs])
                b.append(-rhs)
            elif relation == "<=":
                A.append(coeffs)
                b.append(rhs)
            elif relation == "=":
                A.append(coeffs)
                b.append(rhs)
                A.append([-c for c in coeffs])
                b.append(-rhs)
        return A, b

    def _format_solution(self, result):
        z_value = -result.fun if self.opt_type == "Maximizar" else result.fun
        return {"X": result.x.tolist(), "Z": z_value}
