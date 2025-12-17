from src.Tests.params import towers, edges, colors
from src.Costs.cost1 import calculate_cost
from typing import List


def calculate_all_costs(pos: int = 0, asig: List = [0 for _ in range(len(towers))]):
    if pos == len(towers):
        total_cost = 0
        for i in range(len(asig)):
            total_cost += calculate_cost(towers[i], asig[i])
        for u, v in edges:
            if asig[u] == asig[v]:
                return
        print(f"Asignacion:{asig}, costo: {total_cost}")
        return
    for c in colors:
        asig[pos] = c
        calculate_all_costs(pos + 1, asig)
