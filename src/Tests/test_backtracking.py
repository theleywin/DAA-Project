from src.Network import Network
from src.Tower import Tower
from src.Solves.backtracking import backtrack

network = Network()

tower0 = Tower(
    location=(0, 1), equipment_level=4, electricity_consumption=2, regulations=1
)
tower1 = Tower(
    location=(0, 0), equipment_level=3, electricity_consumption=3, regulations=1
)
tower2 = Tower(
    location=(1, 0), equipment_level=2, electricity_consumption=1, regulations=2
)

network.add_tower(tower0)
network.add_tower(tower1)
network.add_tower(tower2)

network.add_edge(0, 1)
network.add_edge(1, 2)

frequencies = [1, 2, 3, 4]


min_cost, min_asignments = backtrack(
    network=network,
    colors=frequencies,
    current_tower_idx=0,
    total_cost=0.0,
    min_cost=float("inf"),
    actual_asignments=[0 for _ in range(len(network.towers))],
    min_asignments=[0 for _ in range(len(network.towers))],
)

print(f"El costo mínimo encontrado es: {min_cost}")
print(f"Las asignaciones de frecuencias son: {min_asignments[0:len(network.towers)]}")
