import random
import math
from typing import List, Tuple
from src.Network import Network
from src.Costs.cost1 import calculate_cost
from src.Solves.dsatur import dsatur_solve

def simulated_annealing_solve(
    network: Network, 
    colors: List, 
    initial_temp: float = 1000.0, 
    cooling_rate: float = 0.995, 
    max_iter: int = 10000
) -> Tuple[float, List]:
    """
    Simulated Annealing metaheuristic for Minimum Cost Graph Coloring.
    
    1. Start with an initial valid solution (from DSATUR).
    2. Perturb the solution (change one node's color).
    3. Accept if better or with prob exp(-delta/T).
    """
    
    # 1. Initialization
    # Start with a good greedy solution
    current_cost, current_assignments = dsatur_solve(network, colors)
    
    # Keep track of best found
    best_cost = current_cost
    best_assignments = list(current_assignments)
    
    current_temp = initial_temp
    
    n_towers = len(network.towers)
    
    for i in range(max_iter):
        # 2. Perturbation (Neighbor Generation)
        # Pick a random node
        node_idx = random.randint(0, n_towers - 1)
        
        # Pick a random NEW color for this node (different from current)
        # To avoid infinite loops if only 1 color exists, check len
        if len(colors) <= 1:
            break
            
        new_color = random.choice(colors)
        while new_color == current_assignments[node_idx]:
             new_color = random.choice(colors)
             
        # Check Validity of new color
        # Optimization: We could allow invalid moves with penalty (soft constraints),
        # but here we stick to "feasible solutions only" for simplicity.
        is_valid = True
        for neighbor in network.get_neighbors(node_idx):
            if current_assignments[neighbor] == new_color:
                is_valid = False
                break
        
        if not is_valid:
            continue # Try another move
            
        # 3. Calculate Cost Delta
        old_color = current_assignments[node_idx]
        old_node_cost = calculate_cost(network.towers[node_idx], old_color)
        new_node_cost = calculate_cost(network.towers[node_idx], new_color)
        
        # Since we only changed one node, delta is local
        delta_cost = new_node_cost - old_node_cost
        
        # 4. Acceptance Criteria
        accept = False
        if delta_cost < 0:
            accept = True
        else:
            # Metropolis criterion
            # Probability = exp(-delta / T)
            p = math.exp(-delta_cost / current_temp)
            if random.random() < p:
                accept = True
                
        if accept:
            current_assignments[node_idx] = new_color
            current_cost += delta_cost
            
            # Update Global Best
            if current_cost < best_cost:
                best_cost = current_cost
                best_assignments = list(current_assignments)
                
        # 5. Cooling
        current_temp *= cooling_rate
        
        # Stop if frozen
        if current_temp < 0.001:
            break
            
    return best_cost, best_assignments
