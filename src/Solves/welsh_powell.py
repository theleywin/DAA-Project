from typing import List, Tuple
from src.Network import Network
from src.Costs.cost1 import calculate_cost

def welsh_powell_solve(network: Network, colors: List) -> Tuple[float, List]:
    """
    Implementation of the Welsh-Powell algorithm adapted for minimum cost.
    
    1. Calculate the degree of all nodes.
    2. Sort nodes by degree in descending order.
    3. Iterate through the sorted list and assign the first valid color (minimum cost).
    """
    n = len(network.towers)
    assignments = [None] * n
    
    # 1. Calculate degrees
    degrees = []
    for i in range(n):
        deg = len(network.get_neighbors(i))
        degrees.append((deg, i))
    
    # 2. Sort by degree descending
    degrees.sort(key=lambda x: x[0], reverse=True)
    sorted_nodes = [x[1] for x in degrees]
    
    total_cost = 0.0
    
    # 3. Coloring Step
    # Standard Welsh-Powell usually tries to color non-adjacent nodes with the SAME color in one pass.
    # However, for cost minimization with diverse costs per node/color, iterating through sorted nodes
    # and assigning the best local color is a common greedy adaptation (First-Fit on ordered nodes).
    # We will use the sequential greedy approach on sorted nodes.
    
    for node in sorted_nodes:
        # Check neighbors
        neighbor_colors = set()
        for neighbor in network.get_neighbors(node):
            if assignments[neighbor] is not None:
                neighbor_colors.add(assignments[neighbor])
        
        chosen_color = None
        min_color_cost = float('inf')
        
        for color in colors:
            if color not in neighbor_colors:
                # Calculate cost adaptation
                cost = calculate_cost(network.towers[node], color)
                if cost < min_color_cost:
                    min_color_cost = cost
                    chosen_color = color
                    # Assuming sorted colors and monotonic cost:
                    break
        
        if chosen_color is None:
            return -1.0, []
            
        assignments[node] = chosen_color
        total_cost += min_color_cost
        
    return total_cost, assignments
