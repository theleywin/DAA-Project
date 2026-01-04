import matplotlib.pyplot as plt
import os
from typing import List, Tuple, Dict, Any

class Visualizer:
    
    OUTPUT_DIR = "doc/article/figures"
    
    @staticmethod
    def ensure_dir():
        if not os.path.exists(Visualizer.OUTPUT_DIR):
            os.makedirs(Visualizer.OUTPUT_DIR)

    @staticmethod
    def plot_convergence_history(history: List[Tuple[int, float, float]], filename="convergence.png"):
        """
        Plots Cost vs Iteration for Simulated Annealing.
        history: list of (iteration, current_cost, best_cost)
        """
        Visualizer.ensure_dir()
        
        iterations = [x[0] for x in history]
        current_costs = [x[1] for x in history]
        best_costs = [x[2] for x in history]
        
        plt.figure(figsize=(10, 6))
        plt.plot(iterations, current_costs, label='Current Cost', alpha=0.5, color='orange')
        plt.plot(iterations, best_costs, label='Best Cost Found', linewidth=2, color='blue')
        
        plt.title('Simulated Annealing Convergence Profile')
        plt.xlabel('Iteration')
        plt.ylabel('Cost')
        plt.legend()
        plt.grid(True)
        
        path = os.path.join(Visualizer.OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"Figure saved: {path}")

    @staticmethod
    def plot_complexity_profile(results: List[Dict[str, Any]], filename="complexity.png"):
        """
        Plots Time vs N for multiple solvers.
        """
        Visualizer.ensure_dir()
        
        # Organize data by solver
        solvers_data = {}
        for r in results:
            name = r['Solver']
            if name not in solvers_data:
                solvers_data[name] = {'N': [], 'Time': []}
            solvers_data[name]['N'].append(r['N'])
            solvers_data[name]['Time'].append(r['Time'])
            
        plt.figure(figsize=(10, 6))
        
        for name, data in solvers_data.items():
            # Sort just in case
            sorted_pairs = sorted(zip(data['N'], data['Time']))
            ns = [p[0] for p in sorted_pairs]
            ts = [p[1] for p in sorted_pairs]
            plt.plot(ns, ts, marker='o', label=name)
            
        plt.title('Algorithm Time Complexity (Scalability)')
        plt.xlabel('Number of Nodes (N)')
        plt.ylabel('Execution Time (ms)')
        plt.legend()
        plt.grid(True)
        
        path = os.path.join(Visualizer.OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"Figure saved: {path}")

    @staticmethod
    def plot_stability_comparison(data_list: List[Dict[str, Any]], filename="stability.png"):
        """
        Bar chart for stability (Mean Cost with Error Bars).
        data_list: List of dicts with 'Name', 'Mean', 'StdDev'
        """
        Visualizer.ensure_dir()
        
        names = [x['Name'] for x in data_list]
        means = [x['Mean'] for x in data_list]
        stds = [x['StdDev'] for x in data_list]
        
        plt.figure(figsize=(10, 6))
        plt.bar(names, means, yerr=stds, capsize=10, color=['skyblue', 'lightgreen'])
        
        plt.title('Algorithm Stability (15 Runs)')
        plt.ylabel('Mean Cost')
        # Zoom in Y axis if needed (e.g. costs are high)
        min_y = min(means) * 0.9
        max_y = max(means) * 1.1
        plt.ylim(min_y, max_y)
        
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        path = os.path.join(Visualizer.OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"Figure saved: {path}")
