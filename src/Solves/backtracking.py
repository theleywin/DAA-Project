from src.Network import Network
from src.Costs.cost1 import calculate_cost
from typing import List, Tuple
from src.Solves.greedy import greedy_solve  # Optimization: Use greedy to set bound

def backtracking_solve(network: Network, colors: List) -> Tuple[float, List]:
    """
    Standard wrapper for the backtracking solver.
    Initializes the recursion.
    """
    n = len(network.towers)
    initial_assignments = [None] * n
    
    # HEURISTIC OPTIMIZATION:
    # Run a fast greedy algorithm first to get a valid upper bound.
    # This allows the backtracking to prune expensive branches immediately.
    print("  (Backtracking: Running greedy init to prune search space...)")
    greedy_cost, _ = greedy_solve(network, colors)
    
    # We set min_cost to the greedy result. 
    # If backtracking doesn't find anything better, we return the greedy cost.
    # Note: We don't store the greedy assignment as 'min_assignments' here to keep it simple,
    # but strictly speaking we should if we want to return it as fallback.
    # Since we want EXACT optimal, if we finish and min_assignments is empty, it means greedy was optimal 
    # (or we didn't store it). 
    # Let's verify: If we start with min_cost = greedy_cost, and find nothing strictly smaller,
    # we return min_cost with EMPTY assignment if we don't init it.
    # So we MUST store the greedy assignment or handle the fallback.
    
    # Let's capture the greedy assignment too.
    _, greedy_assignments = greedy_solve(network, colors) # re-run or unpack above
    
    min_cost = greedy_cost
    min_assignments = list(greedy_assignments)
    
    # Find OPTIMAL
    min_cost, min_assignments = backtrack(
        network,
        colors,
        0,
        0.0,
        min_cost,
        min_assignments,
        initial_assignments
    )
    
    return min_cost, min_assignments

def backtrack(
    network: Network,
    colors: List,
    current_tower_idx: int,
    total_cost: float,
    min_cost: float,
    min_asignments: List,
    actual_asignments: List,
):
    """
    Función recursiva de backtracking para asignar frecuencias a las torres.
    """

    # Pruning: If current cost already exceeds best found, stop.
    if total_cost >= min_cost:
        return min_cost, min_asignments
    
    # Base Case: All towers assigned
    if current_tower_idx == len(network.towers): 
        return total_cost, actual_asignments.copy()

    tower = network.towers[current_tower_idx]

    # Intentamos asignar cada frecuencia disponible
    # Optimization: Sort colors by cost for this tower could help find good solutions faster
    # but the order in 'colors' is respected.
    
    for color in colors:
        valid = True
        
        # Validity Check
        for neighbor_id in network.get_neighbors(current_tower_idx):
            # Check only against neighbors that have been assigned
            # We assume assignments are done in order 0..current_tower_idx
            # But the graph neighbors might have higher indices (not assigned yet)
            # or lower indices (already assigned).
            assigned_val = actual_asignments[neighbor_id]
            if assigned_val is not None and assigned_val == color:
                valid = False
                break

        # Si la frecuencia es válida, asignamos y continuamos recursivamente
        if valid:
            actual_asignments[current_tower_idx] = color
            cost = calculate_cost(tower, color)
            
            new_min_cost, new_min_asignments = backtrack(
                network,
                colors,
                current_tower_idx + 1,
                total_cost + cost,
                min_cost,
                min_asignments,
                actual_asignments,
            )
            
            if new_min_cost < min_cost:
                min_cost = new_min_cost
                min_asignments = new_min_asignments
            
            # BACKTRACK STEP: Reset the state for the next iteration
            actual_asignments[current_tower_idx] = None

    return min_cost, min_asignments
