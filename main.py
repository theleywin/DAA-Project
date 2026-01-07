from src.Solves.greedy import greedy_solve
from src.Solves.dsatur import dsatur_solve
from src.Solves.welsh_powell import welsh_powell_solve
from src.Solves.backtracking import backtracking_solve
from src.Solves.tabu_repair import tabu_repair_solve
from src.Solves.simulated_annealing import simulated_annealing_solve
from src.Generator.generator import GraphGenerator
from src.Tests.benchmark import BenchmarkRunner

def main():
    print("Optimization Algorithm Benchmark Tool")
    
    # 1. Setup Benchmark Runner
    runner = BenchmarkRunner()
    runner.register_solver("Basic Greedy", greedy_solve)
    runner.register_solver("DSATUR", dsatur_solve)
    runner.register_solver("Welsh-Powell", welsh_powell_solve) # Commented out to focus on SA comparison
    runner.register_solver("Sim. Annealing", simulated_annealing_solve)
    runner.register_solver("Tabu Repair", tabu_repair_solve)
    
    # Special runner for Backtracking (only small cases)
    small_runner = BenchmarkRunner()
    small_runner.register_solver("Basic Greedy", greedy_solve)
    # small_runner.register_solver("Backtracking", backtracking_solve)
    # small_runner.register_solver("DSATUR", dsatur_solve) # Optional comparisons
    
    # 2. Configuration
    GRAPH_SIZES = [10, 20, 50, 100]
    SAMPLES = 10
    SMALL_GRAPH_LIMIT = 15

    # 3. Generate Test Cases & Run Benchmark
    print(f"Starting Benchmark using sizes: {GRAPH_SIZES} with {SAMPLES} samples each.")

    test_cases_heuristics = []
    test_cases_exact = []

    for n in GRAPH_SIZES:
        print(f"Generating {SAMPLES} graphs of size {n}...")
        for i in range(SAMPLES):
            # Using a fixed density or a range, here using 0.5 as a middle ground or random
            density = 0.5 
            g = GraphGenerator.generate_random_graph(n, density)
            
            # Estimate necessary colors (simple heuristic for range) or just give enough
            colors = list(range(1, (n + 1))) 
            
            instance_name = f"Random(N={n}, D={density}, #{i+1})"
            
            # Add to heuristics suite
            test_cases_heuristics.append((instance_name, g, colors))
            
            # Add to exact suite only if small
            if n <= SMALL_GRAPH_LIMIT:
                test_cases_exact.append((instance_name, g, colors))

    # # 4. Run Benchmark
    # if test_cases_exact:
        # print("\n--- Running Small Instance Benchmarks (including Exact Solver) ---")
        # small_runner.run_suite(test_cases_exact)
        # small_runner.report()
        # small_runner.save_to_csv("results/benchmark_exact.csv")

    print("\n--- Running Heuristic Benchmarks (All Sizes) ---")
    runner.run_suite(test_cases_heuristics)
    runner.report()
    runner.save_to_csv("resultsbenchmark_results.csv")
    
    # # 5. Comparative Suite (New)
    # from src.Tests.comparative_suite import ComparativeBenchmark
    # print("\n\n" + "="*40)
    # print("STARTING COMPARATIVE SUITE")
    # print("="*40)
    
    # comp_suite = ComparativeBenchmark()
    # comp_suite.register_solver("Basic Greedy", greedy_solve)
    # comp_suite.register_solver("DSATUR", dsatur_solve)
    # comp_suite.register_solver("Sim. Annealing", simulated_annealing_solve)
    # comp_suite.register_solver("Welsh-Powell", welsh_powell_solve)
    # comp_suite.register_solver("Tabu Repair", tabu_repair_solve)
    # # comp_suite.register_solver("Backtracking", backtracking_solve)
    
    # # Run Experiments
    # # comp_suite.run_density_sweep(n_nodes=20, steps=9)
    # # comp_suite.run_scalability_sweep(density=0.1, start_n=10, end_n=50, step=10)
    # # comp_suite.run_high_cost_test()

    # # 6. Deep Empirical Analysis (New)
    # from src.Tests.empirical_analysis import EmpiricalAnalyzer
    # print("\n\n" + "="*40)
    # print("STARTING DEEP EMPIRICAL ANALYSIS")
    # print("="*40)
    
    # # A. Convergence
    # g_conv = GraphGenerator.generate_random_graph(50, 0.4)
    # history = EmpiricalAnalyzer.run_convergence_tracker(g_conv, list(range(1, 51)), max_iter=2000)
    
    # # B. Complexity
    # solvers_map = {
    #     "Basic Greedy": greedy_solve,
    #     "DSATUR": dsatur_solve,
    #     "Sim. Annealing": simulated_annealing_solve,
    #     "Welsh-Powell": welsh_powell_solve,
    #     "Tabu Repair": tabu_repair_solve,
    #     # "Backtracking": backtracking_solve
    # }
    # complexity_results = EmpiricalAnalyzer.run_complexity_profile(solvers_map, max_n=100, step=10)
    
    # # C. Stability
    # sa_stats = EmpiricalAnalyzer.run_stability_test("Sim. Annealing", simulated_annealing_solve, g_conv, list(range(1,51)), runs=15)
    # tabu_stats = EmpiricalAnalyzer.run_stability_test("Tabu Repair", tabu_repair_solve, g_conv, list(range(1,51)), runs=15)
    # wp_stats = EmpiricalAnalyzer.run_stability_test("Welsh-Powell", welsh_powell_solve, g_conv, list(range(1,51)), runs=15)
    # # bp_stats = EmpiricalAnalyzer.run_stability_test("Backtracking", backtracking_solve, g_conv, list(range(1,51)), runs=15)
    # g_stats = EmpiricalAnalyzer.run_stability_test("Basic Greedy", greedy_solve, g_conv, list(range(1,51)), runs=15)
    # ds_stats = EmpiricalAnalyzer.run_stability_test("DSATUR", dsatur_solve, g_conv, list(range(1,51)), runs=15)

    # # 7. Visualization
    # from src.Tests.visualizer import Visualizer
    # print("\n\nGenerating Figures...")
    # Visualizer.plot_convergence_history(history, "convergence.png")
    # Visualizer.plot_complexity_profile(complexity_results, "complexity.png")
    
    # stability_data = [
    #     {"Name": "Sim. Annealing", "Mean": sa_stats['Mean'], "StdDev": sa_stats['StdDev']},
    #     {"Name": "Tabu Repair", "Mean": tabu_stats['Mean'], "StdDev": tabu_stats['StdDev']},
    #     {"Name": "Welsh-Powell", "Mean": wp_stats['Mean'], "StdDev": wp_stats['StdDev']},
    #     # {"Name": "Backtracking", "Mean": bp_stats['Mean'], "StdDev": bp_stats['StdDev']},
    #     {"Name": "Basic Greedy", "Mean": g_stats['Mean'], "StdDev": g_stats['StdDev']},
    #     {"Name": "DSATUR", "Mean": ds_stats['Mean'], "StdDev": ds_stats['StdDev']},
    # ]
    # Visualizer.plot_stability_comparison(stability_data, "stability.png")

if __name__ == "__main__":
    main()

