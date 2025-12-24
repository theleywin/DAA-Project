import time
from typing import List, Callable, Dict, Any
from src.Network import Network
from src.Generator.generator import GraphGenerator

class ComparativeBenchmark:
    """
    Suite for running comparative tests on graph coloring algorithms.
    """
    
    def __init__(self):
        self.solvers: Dict[str, Callable] = {}

    def register_solver(self, name: str, solve_function: Callable):
        self.solvers[name] = solve_function

    def run_density_sweep(self, n_nodes: int = 50, steps: int = 9):
        """
        Runs solvers on graphs with increasing density (0.1 to 0.9).
        """
        print(f"\n--- Density Sweep (N={n_nodes}) ---")
        print(f"{'Density':<10} | {'Solver':<15} | {'Cost':<10} | {'Time(ms)':<10}")
        print("-" * 60)
        
        densities = [i/10.0 for i in range(1, steps + 1)]
        colors = list(range(1, 101)) # Ample colors
        
        results = []

        for d in densities:
            # Generate graph
            network = GraphGenerator.generate_random_graph(n_nodes, d)
            
            for name, func in self.solvers.items():
                # Safeguard for Backtracking
                if "Backtracking" in name and n_nodes > 12:
                    continue
                
                start = time.time()
                try:
                    cost, _ = func(network, colors)
                    duration = (time.time() - start) * 1000
                except Exception:
                    cost = -1
                    duration = -1
                
                print(f"{d:<10} | {name:<15} | {cost:<10} | {duration:.2f}")
                results.append({"Density": d, "Solver": name, "Cost": cost, "Time": duration})

    def run_scalability_sweep(self, density: float = 0.3, start_n: int = 10, end_n: int = 100, step: int = 10):
        """
        Runs solvers on graphs with increasing size (N).
        """
        print(f"\n--- Scalability Sweep (Density={density}) ---")
        print(f"{'N':<5} | {'Solver':<15} | {'Cost':<10} | {'Time(ms)':<10}")
        print("-" * 60)
        
        sizes = range(start_n, end_n + 1, step)
        colors = list(range(1, 201))
        
        results = []
        
        for n in sizes:
            network = GraphGenerator.generate_random_graph(n, density)
            
            for name, func in self.solvers.items():
                # Skip backtracking for large N
                if "Backtracking" in name and n > 8:
                    continue
                    
                start = time.time()
                try:
                    cost, _ = func(network, colors)
                    duration = (time.time() - start) * 1000
                except Exception:
                    cost = -1
                    duration = -1
                    
                print(f"{n:<5} | {name:<15} | {cost:<10} | {duration:.2f}")
                results.append({"N": n, "Solver": name, "Cost": cost, "Time": duration})

    def run_high_cost_test(self):
        """
        Test with extreme cost differences to verify priority.
        """
        print(f"\n--- High Cost Variance Test (N=20) ---")
        # Generate modest graph
        network = GraphGenerator.generate_random_graph(20, 0.4)
        
        # Colors where some are CHEAP (1-5) and others EXPENSIVE (100-105)
        # Algorithms should avoid the expensive ones if possible
        colors = [1, 2, 3, 4, 5, 100, 101, 102, 103, 104, 105]
        
        print(f"{'Solver':<15} | {'Cost':<10} | {'Time(ms)':<10} | {'Used Expensive?'}")
        print("-" * 70)
        
        for name, func in self.solvers.items():
            if "Backtracking" in name: continue # skip for now
            
            start = time.time()
            cost, assignments = func(network, colors)
            duration = (time.time() - start) * 1000
            
            used_expensive = any(c >= 100 for c in assignments)
            
            print(f"{name:<15} | {cost:<10} | {duration:<10.2f} | {str(used_expensive)}")
