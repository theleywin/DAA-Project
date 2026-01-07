import time
import random
import math
import statistics
from typing import List, Callable, Dict, Any, Tuple
from src.Network import Network
from src.Costs.cost1 import calculate_cost
from src.Generator.generator import GraphGenerator
from src.Solves.dsatur import dsatur_solve

class EmpiricalAnalyzer:
    """
    Tools for deep scientific analysis of algorithm behavior.
    """

    @staticmethod
    def run_convergence_tracker(network: Network, colors: List, max_iter: int = 5000):
        """
        Runs an instrumented version of Simulated Annealing to return cost history.
        """
        print(f"\n--- SA Convergence Analysis (Max Iter={max_iter}) ---")
        
        # Instrumented SA Implementation
        current_temp = 1000.0
        cooling_rate = 0.995
        
        # Init
        current_cost, current_assignments = dsatur_solve(network, colors)
        best_cost = current_cost
        best_assignments = list(current_assignments)
        
        history = [] # List of (iter, current, best)
        
        n_towers = len(network.towers)
        
        for i in range(max_iter):
             # Record history every 10 iterations to save space
            if i % 10 == 0:
                history.append((i, current_cost, best_cost))

            node_idx = random.randint(0, n_towers - 1)
            
            if len(colors) <= 1: break
            
            new_color = random.choice(colors)
            while new_color == current_assignments[node_idx]:
                 new_color = random.choice(colors)
                 
            is_valid = True
            for neighbor in network.get_neighbors(node_idx):
                if current_assignments[neighbor] == new_color:
                    is_valid = False
                    break
            
            if not is_valid: continue
                
            old_color = current_assignments[node_idx]
            delta = calculate_cost(network.towers[node_idx], new_color) - calculate_cost(network.towers[node_idx], old_color)
            
            accept = False
            if delta < 0:
                accept = True
            else:
                 if random.random() < math.exp(-delta / current_temp):
                    accept = True
                    
            if accept:
                current_assignments[node_idx] = new_color
                current_cost += delta
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_assignments = list(current_assignments)
                    
            current_temp *= cooling_rate
            if current_temp < 0.001: break
            
        print(f"Convergence Run Complete. Final Cost: {best_cost}")
        print(f"History Sample (Head/Tail):")
        for x in history[:5]: print(f"  Iter {x[0]}: Curr={x[1]:.1f}, Best={x[2]:.1f}")
        print("  ...")
        for x in history[-5:]: print(f"  Iter {x[0]}: Curr={x[1]:.1f}, Best={x[2]:.1f}")
        
        return history

    @staticmethod
    def run_complexity_profile(solvers: Dict[str, Callable], max_n: int = 200, step: int = 20, colors: List = None):
        """
        Runs solvers against N size to analyze Time Complexity.
        """
        print(f"\n--- Complexity Analysis (N=10 to {max_n}) ---")
        print(f"{'N':<5} | {'Solver':<15} | {'Time(ms)':<10}")
        print("-" * 40)
        
        results = []
        sizes = range(10, max_n + 1, step)
        if colors is None:
            colors = list(range(1, 101))
        
        for n in sizes:
            network = GraphGenerator.generate_random_graph(n, 0.3)
            for name, func in solvers.items():
                if "Backtracking" in name and n > 12: continue
                
                # Measure multiple times for stability
                times = []
                for _ in range(3):
                    start = time.process_time() # CPU time better for algo analysis
                    try:
                        func(network, colors)
                        dur = (time.process_time() - start) * 1000
                        times.append(dur)
                    except:
                        pass
                
                if times:
                    avg_time = sum(times) / len(times)
                    print(f"{n:<5} | {name:<15} | {avg_time:.2f}")
                    results.append({"N": n, "Solver": name, "Time": avg_time})
        
        return results

    @staticmethod
    def run_stability_test(name: str, func: Callable, network: Network, colors: List, runs: int = 20):
        """
        Analyzes the variance of a stochastic solver.
        """
        print(f"\n--- Stability Analysis: {name} ({runs} runs) ---")
        costs = []
        
        for i in range(runs):
            c, _ = func(network, colors)
            costs.append(c)
            
        mean = statistics.mean(costs)
        stdev = statistics.stdev(costs) if runs > 1 else 0
        min_c = min(costs)
        max_c = max(costs)
        
        print(f"Mean Cost: {mean:.2f}")
        print(f"Std Dev  : {stdev:.2f}")
        print(f"Min/Max  : {min_c:.2f} / {max_c:.2f}")
        
        return {"Mean": mean, "StdDev": stdev, "Min": min_c, "Max": max_c}
