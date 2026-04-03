import random
import numpy as np

from Q6_part_a import demands, state_fitness, random_state
from part_b import rrhc_driver
from part_c import run_driver_ga

# ============================================
# Run experiments for comparison
# ============================================
def run_experiments():
    num_trials = 20

    rrhc_results = []
    
    ga_results = []

    # ============================
    # RRHC trials
    # ============================
    for _ in range(num_trials):
        best_state, best_fit, _ = rrhc_driver(30, demands)
        rrhc_results.append(best_fit)

    # ============================
    # GA trials
    # ============================
    for _ in range(num_trials):
        best_sol, best_fit = run_driver_ga(30, 100, 0.1)
        ga_results.append(best_fit)

    # ============================
    # Statistics
    # ============================
    rrhc_mean = np.mean(rrhc_results)
    rrhc_std = np.std(rrhc_results)
    rrhc_best = max(rrhc_results)

    ga_mean = np.mean(ga_results)
    ga_std = np.std(ga_results)
    ga_best = max(ga_results)

    # ============================
    # Print results
    # ============================
    print("\n=== GA vs RRHC Comparison (20 Trials) ===\n")

    print(f"{'Algorithm':<10} {'Mean Fitness':<15} {'Std Dev':<15} {'Best Run'}")
    print("-" * 55)

    print(f"{'RRHC':<10} {rrhc_mean:<15.2f} {rrhc_std:<15.2f} {rrhc_best}")
    print(f"{'GA':<10} {ga_mean:<15.2f} {ga_std:<15.2f} {ga_best}")


# ============================================
# Run
# ============================================
if __name__ == "__main__":
    run_experiments()