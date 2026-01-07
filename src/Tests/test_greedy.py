from src.Solves.greedy import greedy_solve_2 as greedy
from src.Tests.params import colors, network


def test():
    total_cost, assignments = greedy(network=network, colors=colors)

    # print(f"El costo total encontrado es: {total_cost}")
    # print(f"Las asignaciones de frecuencias son: {assignments[0:len(network.towers)]}")
