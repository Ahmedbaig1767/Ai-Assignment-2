import random
from part_b import run_ga

# ============================================
# Run experiment multiple times
# ============================================
def run_experiment(pop_size, num_generations, pm, elitism, trials=30):
    best_fitness_list = []
    found_optimum = 0
    generations_to_50 = []

    for _ in range(trials):
        history = run_ga(pop_size, num_generations, pm, elitism)

        best_fitness = max([h[1] for h in history])
        best_fitness_list.append(best_fitness)

        # Check if x = 7 found
        if any(h[2] == 7 for h in history):
            found_optimum += 1

        # First generation reaching f >= 50
        gen_found = None
        for h in history:
            if h[1] >= 50:
                gen_found = h[0]
                break

        if gen_found is not None:
            generations_to_50.append(gen_found)

    avg_best = sum(best_fitness_list) / trials
    avg_gen_50 = sum(generations_to_50) / len(generations_to_50) if generations_to_50 else None

    return avg_best, found_optimum, avg_gen_50

# ============================================
# Elitism comparison
# ============================================
def elitism_experiment():
    print("\n=== Elitism vs No Elitism ===")

    no_elite = run_experiment(4, 20, 0.1, False)
    elite = run_experiment(4, 20, 0.1, True)

    print(f"\nNo Elitism: Avg Fitness={no_elite[0]}, Found x=7={no_elite[1]}, Avg Gen>=50={no_elite[2]}")
    print(f"With Elitism: Avg Fitness={elite[0]}, Found x=7={elite[1]}, Avg Gen>=50={elite[2]}")

# ============================================
# Mutation rate experiment
# ============================================
def mutation_experiment():
    print("\n=== Mutation Rate Experiment ===")

    rates = [0.01, 0.1, 0.3, 0.5]

    for pm in rates:
        avg_best, _, _ = run_experiment(4, 20, pm, False)
        print(f"pm={pm} -> Avg Best Fitness={avg_best}")

# ============================================
# Run experiments
# ============================================
if __name__ == "__main__":
    elitism_experiment()
    mutation_experiment()