from typing import List
from src.Network import Network
from src.Tower import Tower
from src.Solves.backtracking import backtrack
from src.Costs.cost1 import calculate_cost


towers = [
    Tower(location=(0, 1), equipment_level=4, electricity_consumption=2, regulations=1),
    Tower(location=(0, 0), equipment_level=3, electricity_consumption=3, regulations=1),
    Tower(location=(1, 0), equipment_level=2, electricity_consumption=1, regulations=2),
]

edges = [(0, 1), (1, 2)]

colors = [1, 2, 3, 4]

network = Network()

for tower in towers:
    network.add_tower(tower)

for u, v in edges:
    network.add_edge(u, v)


def test():
    min_cost, min_asignments = backtrack(
        network=network,
        colors=colors,
        current_tower_idx=0,
        total_cost=0.0,
        min_cost=float("inf"),
        actual_asignments=[0 for _ in range(len(network.towers))],
        min_asignments=[0 for _ in range(len(network.towers))],
    )

    print(f"El costo mínimo encontrado es: {min_cost}")
    print(
        f"Las asignaciones de frecuencias son: {min_asignments[0:len(network.towers)]}"
    )


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
