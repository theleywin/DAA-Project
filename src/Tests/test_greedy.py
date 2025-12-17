from src.Solves.greedy import greedy
from src.Costs.cost1 import calculate_cost
from src.Tests.params import towers, edges, colors, network

def test():
    total_cost, assignments = greedy(
        network=network,
        colors=colors
    )

    print(f"El costo total encontrado es: {total_cost}")
    print(f"Las asignaciones de frecuencias son: {assignments[0:len(network.towers)]}")