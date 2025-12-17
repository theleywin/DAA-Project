from src.Network import Network
from src.Costs.cost1 import calculate_cost
from typing import List


def backtrack(
    network: Network,
    colors: List,
    current_tower_idx: int = 0,
    total_cost: float = 0.0,
    min_cost: float = "inf",
    min_asignments: List = [0*1000],
    actual_asignments: List = [0*1000],
):
    """
    Función recursiva de backtracking para asignar frecuencias a las torres.

    :param network: Objeto Network que contiene las torres y sus conexiones.
    :param colors: Lista de frecuencias disponibles.
    :param current_tower_idx: Índice de la torre actual que se está procesando.
    :param total_cost: Costo total acumulado hasta el momento.
    :param min_cost: El costo mínimo encontrado hasta el momento.
    :return: El costo mínimo encontrado después de intentar asignar frecuencias a todas las torres.
    """
    if current_tower_idx == len(network.towers): # Ya se asignaron frecuencias a todas las torres
        if total_cost < min_cost:
            min_cost = total_cost
            min_asignments = actual_asignments.copy()
        return min_cost, min_asignments.copy()

    tower = network.towers[current_tower_idx]

    # Intentamos asignar cada frecuencia disponible
    for color in colors:
        valid = True
        for neighbor_id in network.get_neighbors(current_tower_idx):
            if actual_asignments[neighbor_id] == color:
                valid = False
                break

        # Si la frecuencia es válida, asignamos y continuamos recursivamente
        if valid:
            actual_asignments[current_tower_idx] = color
            cost = calculate_cost(tower, color)
            new_min_cost, new_min_asignments = backtrack(
                network,
                colors,
                current_tower_idx + 1,
                total_cost + cost,
                min_cost,
                min_asignments,
                actual_asignments,
            )
            if new_min_cost < min_cost:
                min_cost = new_min_cost
                min_asignments = new_min_asignments

    return min_cost, min_asignments
