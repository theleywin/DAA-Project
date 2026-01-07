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
    def plot_cost_distribution(results: List[Dict[str, Any]], filename="boxplot_cost.png"):
        """
        Box plot of Cost Distribution per Algorithm (Normalized to Best Known).
        """
        Visualizer.ensure_dir()
        
        # Filter only valid results
        valid_results = [r for r in results if r['Valid']]
        if not valid_results: return

        # Normalize costs: (Cost - BestKnown) / BestKnown
        data_by_algo = {}
        for r in valid_results:
            algo = r['Algorithm']
            best = r['BestKnownCost']
            if best <= 0: continue
            gap = (r['Cost'] - best) / best
            
            if algo not in data_by_algo:
                data_by_algo[algo] = []
            data_by_algo[algo].append(gap)
            
        labels = []
        data = []
        for algo, gaps in data_by_algo.items():
            labels.append(algo)
            data.append(gaps)
            
        plt.figure(figsize=(10, 6))
        plt.boxplot(data, tick_labels=labels, showfliers=False) # Hide outliers for cleaner view
        plt.title('Cost Distribution (Gap to Best Known Solution)')
        plt.ylabel('Optimality Gap (%)')
        # Format Y axis as percentage
        plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0%}'.format(y)))
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        path = os.path.join(Visualizer.OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"Figure saved: {path}")

    @staticmethod
    def plot_scalability_loglog(results: List[Dict[str, Any]], filename="time_loglog.png"):
        """
        Time vs Size on Log-Log scale.
        """
        Visualizer.ensure_dir()
        
        # Group by Algo -> Size -> Mean Time
        data_map = {}
        for r in results:
            algo = r['Algorithm']
            size = r['Size']
            time_val = r['Time']
            
            if algo not in data_map: data_map[algo] = {}
            if size not in data_map[algo]: data_map[algo][size] = []
            data_map[algo][size].append(time_val)
            
        plt.figure(figsize=(10, 6))
        
        for algo, sizes_map in data_map.items():
            sizes = sorted(sizes_map.keys())
            times = [sum(sizes_map[s])/len(sizes_map[s]) for s in sizes]
            
            # Filter out 0 times for log scale (replace with small epsilon)
            times = [t if t > 0 else 0.01 for t in times]
            
            plt.plot(sizes, times, marker='o', label=algo)
            
        plt.xscale('log')
        plt.yscale('log')
        plt.title('Algorithm Scalability (Log-Log)')
        plt.xlabel('Number of Nodes (N)')
        plt.ylabel('Execution Time (ms)')
        plt.legend()
        plt.grid(True, which="both", ls="-", alpha=0.5)
        
        path = os.path.join(Visualizer.OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"Figure saved: {path}")

    @staticmethod
    def plot_optimality_rate(results: List[Dict[str, Any]], filename="optimality_rate.png"):
        """
        Bar chart showing % of runs where the algorithm found the Best Known solution.
        """
        Visualizer.ensure_dir()
        
        valid_results = [r for r in results if r['Valid']]
        total_counts = {}
        optimal_counts = {}
        
        for r in valid_results:
            algo = r['Algorithm']
            total_counts[algo] = total_counts.get(algo, 0) + 1
            # Allow small float tolerance
            if r['Cost'] <= r['BestKnownCost'] + 1e-9:
                optimal_counts[algo] = optimal_counts.get(algo, 0) + 1
                
        algos = list(total_counts.keys())
        rates = [(optimal_counts.get(a, 0) / total_counts[a]) * 100 for a in algos]
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(algos, rates, color='teal', alpha=0.7)
        plt.title('Optimality Success Rate (% Best Known Found)')
        plt.ylabel('Success Rate (%)')
        plt.ylim(0, 105)
        
        # Add text labels
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:.1f}%',
                     ha='center', va='bottom')
                     
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
        plt.bar(names, means, yerr=stds, capsize=5, color='salmon', alpha=0.7)
        plt.title('Algorithm Stability (Mean Cost with Std Dev)')
        plt.ylabel('Mean Cost')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        path = os.path.join(Visualizer.OUTPUT_DIR, filename)
        plt.savefig(path)
        plt.close()
        print(f"Figure saved: {path}")

    @staticmethod
    def save_results_as_table_image(results: List[Dict[str, Any]], output_prefix="table"):
        """
        Generates images of tables from results, grouped by Graph Size (N=...).
        Parses 'Instance' string to find size.
        """
        Visualizer.ensure_dir()
        
        if not results:
            print("No results to visualize as table.")
            return

        # 1. Group by Size
        # Expected Instance format: "Random(N=10, ...)"
        import re
        grouped_results = {}
        
        for r in results:
            instance = r['Instance']
            match = re.search(r"N=(\d+)", instance)
            if match:
                n = int(match.group(1))
            else:
                n = "Unknown"
                
            if n not in grouped_results:
                grouped_results[n] = []
            grouped_results[n].append(r)
            
        # 2. Generate Table for each group
        for n, rows in grouped_results.items():
            # Prepare data
            # Columns: Solver, Cost, Valid, Time(ms)
            # We aggregate to show Mean Cost/Time or list all?
            # User likely wants the raw list or aggregated. Given the quantity, raw list per N might be big (10 samples * 5 solvers = 50 rows).
            # Let's try to aggregate by Solver if rows > 20, or just print all.
            # Request implies "lista con tamaños... generate graphs... guardar resultados".
            # Probably wants the full results table split by N.
            
            # Sort by Instance Name (Sample #) then Solver
            rows.sort(key=lambda x: (x['Instance'], x['Solver']))
            
            # Extract columns
            columns = ['Instance', 'Solver', 'Cost', 'Time(ms)']
            cell_text = []
            for r in rows:
                # Clean instance name to just #Num if N is constant in this table
                short_inst = r['Instance'].split(",")[-1].strip().replace(")", "") # e.g. "#1"
                cell_text.append([short_inst, r['Solver'], f"{r['Cost']:.1f}", f"{r['Time(ms)']:.2f}"])
                
            # Plot
            # Adjust height based on number of rows
            row_height = 0.3
            header_height = 0.5
            num_rows = len(cell_text)
            fig_height = (num_rows * row_height) + header_height + 1
            
            plt.figure(figsize=(10, fig_height))
            plt.axis('off')
            plt.title(f"Benchmark Results - Graph Size N={n}")
            
            table = plt.table(cellText=cell_text,
                              colLabels=columns,
                              cellLoc='center',
                              loc='center')
            
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1, 1.5)
            
            path = os.path.join(Visualizer.OUTPUT_DIR, f"{output_prefix}_N{n}.png")
            plt.savefig(path, bbox_inches='tight')
            plt.close()
            print(f"Table image saved: {path}")