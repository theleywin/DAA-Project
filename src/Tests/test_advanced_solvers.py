import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.Network import Network
from src.Tower import Tower
from src.Solves.dsatur import dsatur_solve
from src.Solves.welsh_powell import welsh_powell_solve
from src.Solves.greedy import greedy_solve
import random

def create_random_network(num_towers=10, density=0.3):
    network = Network()
    # Create towers
    for i in range(num_towers):
        # random attributes
        t = Tower(
            location=i,
            equipment_level=random.randint(1, 5),
            electricity_consumption=random.randint(10, 100),
            regulations=random.randint(0, 1)
        )
        network.add_tower(t)
    
    # Add random edges
    for i in range(num_towers):
        for j in range(i + 1, num_towers):
            if random.random() < density:
                network.add_edge(i, j)
    return network

def verify_validity(network, assignments):
    if len(assignments) != len(network.towers):
        print("Error: Assignment length mismatch")
        return False
    
    for i in range(len(network.towers)):
        for neighbor in network.get_neighbors(i):
            if assignments[i] == assignments[neighbor]:
                print(f"Error: Conflict between {i} and {neighbor} with value {assignments[i]}")
                return False
    return True

def run_tests():
    print("Running Advanced Greedy Solver Tests...")
    
    # 1. Simple Test Case
    print("\n--- Test Case 1: Random Small Graph ---")
    network = create_random_network(num_towers=20, density=0.4)
    colors = list(range(1, 21)) # Frequencies 1 to 20
    
    # Run Basic Greedy
    cost_g, assign_g = greedy_solve(network, colors)
    valid_g = verify_validity(network, assign_g)
    print(f"Basic Greedy: Cost={cost_g}, Valid={valid_g}")

    # Run DSATUR
    cost_d, assign_d = dsatur_solve(network, colors)
    valid_d = verify_validity(network, assign_d)
    print(f"DSATUR: Cost={cost_d}, Valid={valid_d}")

    # Run Welsh-Powell
    cost_w, assign_w = welsh_powell_solve(network, colors)
    valid_w = verify_validity(network, assign_w)
    print(f"Welsh-Powell: Cost={cost_w}, Valid={valid_w}")
    
    if valid_g and valid_d and valid_w:
        print("\nAll solutions valid!")
    else:
        print("\nSome solutions invalid.")

    # 2. Larger Test Case
    print("\n--- Test Case 2: Random Medium Graph (50 nodes) ---")
    network2 = create_random_network(num_towers=50, density=0.2)
    colors2 = list(range(1, 51))

    cost_g2, _ = greedy_solve(network2, colors2)
    cost_d2, _ = dsatur_solve(network2, colors2)
    cost_w2, _ = welsh_powell_solve(network2, colors2)
    
    print(f"Basic Greedy Cost: {cost_g2}")
    print(f"DSATUR Cost: {cost_d2}")
    print(f"Welsh-Powell Cost: {cost_w2}")

if __name__ == "__main__":
    run_tests()
