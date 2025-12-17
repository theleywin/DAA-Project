from src.Network import Network
from src.Costs.cost1 import calculate_cost
from typing import List


def backtrack(
    network: Network,
    colors: List,
    current_tower_idx: int,
    total_cost: float,
    min_cost: float,
    min_asignments: List,
    actual_asignments: List,
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

    if total_cost >= min_cost:
        return min_cost, min_asignments.copy()
    
    if current_tower_idx == len(network.towers): # Ya se asignaron frecuencias a todas las torres
        return total_cost, actual_asignments.copy()

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
