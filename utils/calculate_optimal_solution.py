import numpy as np


def calculate_optimal_solution(coef_x1, coef_x2, restrictions, obj_type):
    """
    Calcula la solución óptima usando el método gráfico.

    Parámetros:
    - coef_x1: Coeficiente de x1 en la función objetivo.
    - coef_x2: Coeficiente de x2 en la función objetivo.
    - restrictions: Lista de restricciones en formato [(coef1, coef2, inequality, limit)].
    - obj_type: Tipo de objetivo ("max" para maximizar, "min" para minimizar).

    Retorna:
    - x1_opt: Valor óptimo de x1.
    - x2_opt: Valor óptimo de x2.
    - z_opt: Valor óptimo de Z.
    """
    # Paso 1: Encontrar los puntos de intersección de las restricciones
    intersection_points = []

    # Generar todas las combinaciones de restricciones para encontrar intersecciones
    for i in range(len(restrictions)):
        for j in range(i + 1, len(restrictions)):
            A = np.array([
                [restrictions[i][0], restrictions[i][1]],
                [restrictions[j][0], restrictions[j][1]]
            ])
            b = np.array([restrictions[i][3], restrictions[j][3]])

            try:
                # Resolver el sistema de ecuaciones para encontrar la intersección
                intersection = np.linalg.solve(A, b)
                intersection_points.append(intersection)
            except np.linalg.LinAlgError:
                # Si el sistema no tiene solución única, ignorar
                continue

    # Paso 2: Filtrar los puntos que cumplen todas las restricciones
    feasible_points = []
    for point in intersection_points:
        x1, x2 = point
        feasible = True
        for coef1, coef2, inequality, limit in restrictions:
            if inequality == "≤" and coef1 * x1 + coef2 * x2 > limit:
                feasible = False
                break
            elif inequality == "≥" and coef1 * x1 + coef2 * x2 < limit:
                feasible = False
                break
            elif inequality == "=" and not np.isclose(coef1 * x1 + coef2 * x2, limit):
                feasible = False
                break
        if feasible:
            feasible_points.append((x1, x2))

    # Paso 3: Calcular el valor de Z para cada punto factible
    z_values = []
    for x1, x2 in feasible_points:
        z = coef_x1 * x1 + coef_x2 * x2
        z_values.append(z)

    # Paso 4: Encontrar la solución óptima
    if obj_type == "max":
        optimal_index = np.argmax(z_values)
    else:
        optimal_index = np.argmin(z_values)

    x1_opt, x2_opt = feasible_points[optimal_index]
    z_opt = z_values[optimal_index]

    return x1_opt, x2_opt, z_opt