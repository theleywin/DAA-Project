from src.Solves.greedy import greedy_solve
from src.Solves.dsatur import dsatur_solve
from src.Solves.welsh_powell import welsh_powell_solve
from src.Solves.backtracking import backtracking_solve
from src.Solves.simulated_annealing import simulated_annealing_solve
from src.Generator.generator import GraphGenerator
from src.Tests.benchmark import BenchmarkRunner

def main():
    print("Optimization Algorithm Benchmark Tool")
    
    # 1. Setup Benchmark Runner
    runner = BenchmarkRunner()
    runner.register_solver("Basic Greedy", greedy_solve)
    runner.register_solver("DSATUR", dsatur_solve)
    # runner.register_solver("Welsh-Powell", welsh_powell_solve) # Commented out to focus on SA comparison
    runner.register_solver("Sim. Annealing", simulated_annealing_solve)
    
    # Special runner for Backtracking (only small cases)
    small_runner = BenchmarkRunner()
    small_runner.register_solver("Basic Greedy", greedy_solve)
    small_runner.register_solver("Backtracking", backtracking_solve)
    # small_runner.register_solver("DSATUR", dsatur_solve) # Optional comparisons
    
    # 2. Generate Test Cases
    test_cases = []
    
    print("Generating Test Cases...")
    
    # Case A: Small Random (N=8, Density=0.4) - Small enough for Backtracking
    g1 = GraphGenerator.generate_random_graph(8, 0.4)
    colors1 = list(range(1, 6)) # Reduced colors to reduce branching factor
    test_cases_small = [("Very Small (N=8)", g1, colors1)]

    # Case B: Medium Random (N=20, Density=0.4)
    g_med = GraphGenerator.generate_random_graph(20, 0.4)
    colors_med = list(range(1, 25))
    test_cases.append(("Small Random (N=20)", g_med, colors_med))

    # Case C: Geometric Graph (N=50, R=150 in 1000x1000)
    g2 = GraphGenerator.generate_geometric_graph(50, 200, 1000)
    colors2 = list(range(1, 51))
    test_cases.append(("Geometric (N=50)", g2, colors2))
    
    # Case D: Large Random (N=100, Density=0.1)
    g3 = GraphGenerator.generate_random_graph(100, 0.1)
    colors3 = list(range(1, 101))
    test_cases.append(("Large Random (N=100)", g3, colors3))

    # 3. Run Benchmark
    print("\n--- Running Small Instance Benchmarks (including Exact Solver) ---")
    small_runner.run_suite(test_cases_small)
    small_runner.report()

    print("\n--- Running Heuristic Benchmarks (Medium/Large) ---")
    runner.run_suite(test_cases)
    
    # 4. Show Report
    runner.report()
    
    # 5. Comparative Suite (New)
    from src.Tests.comparative_suite import ComparativeBenchmark
    print("\n\n" + "="*40)
    print("STARTING COMPARATIVE SUITE")
    print("="*40)
    
    comp_suite = ComparativeBenchmark()
    comp_suite.register_solver("Basic Greedy", greedy_solve)
    comp_suite.register_solver("DSATUR", dsatur_solve)
    comp_suite.register_solver("Sim. Annealing", simulated_annealing_solve)
    from src.Solves.tabu_repair import tabu_repair_solve
    comp_suite.register_solver("Tabu Repair", tabu_repair_solve)
    comp_suite.register_solver("Backtracking", backtracking_solve)
    
    # Run Experiments
    comp_suite.run_density_sweep(n_nodes=20, steps=9)
    comp_suite.run_scalability_sweep(density=0.1, start_n=10, end_n=50, step=10)
    comp_suite.run_high_cost_test()

if __name__ == "__main__":
    main()

