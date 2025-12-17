from typing import List, Tuple
from src.Network import Network
from src.Costs.cost1 import calculate_cost


def greedy(network: Network, colors: List) -> Tuple[float, List]:
    """
    Función que implementa un algoritmo voraz para asignar frecuencias a las torres.
    :param network: La red de torres y sus interferencias.
    :param colors: La lista de frecuencias disponibles.
    :return: Una tupla que contiene el costo total y la lista de asignaciones de frecuencias.
    """
    total_cost = 0.0
    assignments = [0] * len(network.towers)

    for t in range(len(network.towers)):
        used_colors = set()
        for neighbor_idx in network.get_neighbors(t):
            neighbor_color = assignments[neighbor_idx]
            if neighbor_color != 0:
                used_colors.add(neighbor_color)

        for color in colors:
            if color not in used_colors:
                assignments[t] = color
                total_cost += calculate_cost(network.towers[t], color)
                break

    return total_cost, assignments
