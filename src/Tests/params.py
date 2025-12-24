from src.Network import Network
from src.Tower import Tower

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
