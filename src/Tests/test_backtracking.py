from src.Solves.backtracking import backtrack
from src.Tests.params import colors, network


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

