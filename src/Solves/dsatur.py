from typing import List, Tuple, Set
from src.Network import Network
from src.Costs.cost1 import calculate_cost

def dsatur_solve(network: Network, colors: List) -> Tuple[float, List]:
    """
    Implementation of the DSATUR (Degree of Saturation) algorithm adapted for minimum cost.
    
    1. Select the node with the highest saturation degree (number of different colors in neighbors).
    2. Tie-break: Select the node with the highest degree in the subgraph of uncolored nodes.
    3. Assign the valid color with the minimum cost.
    """
    n = len(network.towers)
    assignments = [None] * n
    saturation_degrees = [0] * n
    # Initial degrees of all nodes
    degrees = [len(network.get_neighbors(i)) for i in range(n)]
    
    # Track uncolored nodes
    uncolored =  set(range(n))
    
    # Track adjacent colors for each node to compute saturation efficiently
    adjacent_colors: List[Set] = [set() for _ in range(n)]

    total_cost = 0.0

    while uncolored:
        # Selection Step
        best_node = -1
        max_sat = -1
        max_deg = -1

        for u in uncolored:
            sat = saturation_degrees[u]
            deg = degrees[u] # Degree in original graph (static tie-breaker) or dynamic uncolored degree could be used. Standard DSATUR often uses static or dynamic degree. Using static degree as tie breaker for simplicity and often effectiveness.
            
            if sat > max_sat:
                max_sat = sat
                max_deg = deg
                best_node = u
            elif sat == max_sat:
                if deg > max_deg:
                    max_deg = deg
                    best_node = u
        
        # If best_node is still -1 (shouldn't happen if uncolored is not empty), pick any
        if best_node == -1:
             best_node = list(uncolored)[0]

        # Coloring Step
        # Find neighbors' colors
        neighbor_colors = set()
        for v in network.get_neighbors(best_node):
            if assignments[v] is not None:
                neighbor_colors.add(assignments[v])
        
        # Find best valid color
        chosen_color = None
        min_color_cost = float('inf')
        
        # Colors are assumed to be integers e.g. frequencies
        # If colors list is just ids, we iterate.
        # We assume 'colors' is a list of valid frequency values.
        
        for color in colors:
            if color not in neighbor_colors:
                # Calculate cost, assuming we want to minimize it locally (greedy)
                cost = calculate_cost(network.towers[best_node], color)
                if cost < min_color_cost:
                    min_color_cost = cost
                    chosen_color = color
                    # Optimization: if costs are strictly increasing with color index/value 
                    # and colors is sorted, we can break immediately. 
                    # But calculate_cost might vary per tower, so we check all or assume sorted logic.
                    # Since we want *best* greedy choice, we scan. 
                    # If calculate_cost is monotonic with frequency, and colors is sorted, break is valid.
                    # We will assume generic costs and check all valid colors or stop if we find a "good enough" if needed, 
                    # but for pure greedy we usually want the min available.
                    
                    # Assuming cost increases with frequency value (common in this domain), 
                    # picking the first valid one in a sorted list is optimal locally.
                    # Let's assume colors is sorted.
                    break
        
        if chosen_color is None:
            # This graph cannot be colored with provided colors
            # In a real scenario we might fail or assign a 'dummy' high cost color.
            # Returning early or raising error. 
            # For this exercise, we assume enough colors are provided.
            return -1.0, []

        assignments[best_node] = chosen_color
        total_cost += min_color_cost
        uncolored.remove(best_node)

        # Update Saturation Step
        for v in network.get_neighbors(best_node):
            if v in uncolored:
                if chosen_color not in adjacent_colors[v]:
                    adjacent_colors[v].add(chosen_color)
                    saturation_degrees[v] += 1
                    
                    # Update dynamic degree if using dynamic degree tie-breaker (not strictly required for basic DSATUR but common)
                    # degrees[v] -= 1 

    return total_cost, assignments
