import random
import math
from typing import List, Tuple
from src.Network import Network
from src.Tower import Tower

class GraphGenerator:
    """
    Generator for creating different types of Network graphs for testing.
    """

    @staticmethod
    def _create_random_tower(id: int, area_size: int = 1000) -> Tower:
        """Helper to create a tower with random attributes."""
        return Tower(
            location=id, # Using ID as location for simplicity in non-geometric context
            equipment_level=random.randint(1, 5),
            electricity_consumption=random.randint(10, 100),
            regulations=random.randint(0, 1)
        )

    @staticmethod
    def generate_random_graph(num_towers: int, density: float) -> Network:
        """
        Generates an Erdos-Renyi random graph.
        
        :param num_towers: Number of nodes.
        :param density: Probability of edge creation between any two nodes.
        :return: A Network instance.
        """
        network = Network()
        
        # Create towers
        for i in range(num_towers):
            network.add_tower(GraphGenerator._create_random_tower(i))
            
        # Create edges
        for i in range(num_towers):
            for j in range(i + 1, num_towers):
                if random.random() < density:
                    network.add_edge(i, j)
                    
        return network

    @staticmethod
    def generate_geometric_graph(num_towers: int, radius: float, area_size: int = 100) -> Network:
        """
        Generates a Random Geometric Graph. Nodes are placed randomly in a 2D plane.
        Edges exist if distance between nodes is <= radius.
        
        :param num_towers: Number of nodes.
        :param radius: Connection radius.
        :param area_size: Size of the square area (area_size x area_size).
        :return: A Network instance.
        """
        network = Network()
        positions: List[Tuple[float, float]] = []
        
        # Create towers and assign random 2D positions
        for i in range(num_towers):
            tower = GraphGenerator._create_random_tower(i, area_size)
            # We can store the 2D position in the tower object if we modify Tower,
            # but for now we'll just keep it local for edge generation.
            # Ideally Tower.location would be more complex, but here we just need the graph topology.
            x = random.uniform(0, area_size)
            y = random.uniform(0, area_size)
            positions.append((x, y))
            network.add_tower(tower)
            
        # Create edges based on distance
        for i in range(num_towers):
            for j in range(i + 1, num_towers):
                dist = math.hypot(positions[i][0] - positions[j][0], positions[i][1] - positions[j][1])
                if dist <= radius:
                    network.add_edge(i, j)
                    
        return network
