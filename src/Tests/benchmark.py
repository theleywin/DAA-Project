import time
from typing import List, Callable, Dict, Any, Tuple
from src.Network import Network

class BenchmarkRunner:
    """
    Runner for benchmarking different graph coloring algorithms.
    """
    def __init__(self):
        self.solvers: Dict[str, Callable] = {}
        self.results: List[Dict[str, Any]] = []

    def register_solver(self, name: str, solve_function: Callable):
        """Registers a solver function to be tested."""
        self.solvers[name] = solve_function

    def run_suite(self, test_instances: List[Tuple[str, Network, List[int]]]):
        """
        Runs all registered solvers on the provided test instances.
        
        :param test_instances: List of tuples (Instance Name, Network, Colors List)
        """
        self.results = []
        print(f"Starting Benchmark Suite on {len(test_instances)} instances with {len(self.solvers)} solvers...")
        
        for instance_name, network, colors in test_instances:
            print(f"\nRunning Instance: {instance_name} (|V|={len(network.towers)})")
            
            for solver_name, solver_func in self.solvers.items():
                start_time = time.time()
                try:
                    # Run solver
                    total_cost, assignments = solver_func(network, colors)
                    end_time = time.time()
                    duration_ms = (end_time - start_time) * 1000
                    
                    # Verify validity
                    is_valid = self._verify(network, assignments)
                    
                    result = {
                        "Instance": instance_name,
                        "Solver": solver_name,
                        "Cost": total_cost,
                        "Valid": is_valid,
                        "Time(ms)": round(duration_ms, 2)
                    }
                    self.results.append(result)
                    print(f"  -> {solver_name}: Cost={total_cost}, Valid={is_valid}, Time={round(duration_ms, 2)}ms")
                    
                except Exception as e:
                    print(f"  -> {solver_name}: FAILED with error {e}")
                    self.results.append({
                        "Instance": instance_name,
                        "Solver": solver_name,
                        "Cost": -1,
                        "Valid": False,
                        "Time(ms)": -1,
                        "Error": str(e)
                    })

    def _verify(self, network: Network, assignments: List[int]) -> bool:
        """Internal helper to verify coloring validity."""
        if not assignments or len(assignments) != len(network.towers):
            return False
            
        for i in range(len(network.towers)):
            # Check adjacency constraint
            curr_color = assignments[i]
            for neighbor in network.get_neighbors(i):
                if assignments[neighbor] == curr_color:
                    return False
        return True

    def report(self):
        """Prints a summary table of the results."""
        print("\n" + "="*80)
        print(f"{'Instance':<20} | {'Solver':<15} | {'Cost':<10} | {'Valid':<6} | {'Time(ms)':<10}")
        print("-" * 80)
        
        for res in self.results:
            print(f"{res['Instance']:<20} | {res['Solver']:<15} | {res['Cost']:<10} | {str(res['Valid']):<6} | {res['Time(ms)']:<10}")
        print("="*80 + "\n")
