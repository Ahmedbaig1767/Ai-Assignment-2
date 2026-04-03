import random
from part_a import decode, fitness, roulette_select, single_point_crossover, mutate

# ============================================
# Generate random chromosome (4-bit)
# ============================================
def random_chromosome():
    return [random.randint(0, 1) for _ in range(4)]

# ============================================
# GA Runner
# ============================================
def run_ga(pop_size, num_generations, pm, elitism=False):
    population = [random_chromosome() for _ in range(pop_size)]
    history = []

    for gen in range(num_generations):

        decoded = [decode(ch) for ch in population]
        fitness_vals = [fitness(ch) for ch in population]

        best_idx = fitness_vals.index(max(fitness_vals))
        best_ch = population[best_idx]
        best_fit = fitness_vals[best_idx]
        best_x = decoded[best_idx]

        # Save history
        history.append((gen, best_fit, best_x))

        # Print table row
        print(f"\nGeneration {gen}")
        for i in range(pop_size):
            print(f"{population[i]} -> x={decoded[i]}, f={fitness_vals[i]}")
        print(f"Best: {best_ch} -> x={best_x}, f={best_fit}")

        # New population
        new_population = []

        # Elitism
        if elitism:
            new_population.append(best_ch)

        while len(new_population) < pop_size:
            parent1 = roulette_select(population)
            parent2 = roulette_select(population)

            point = random.randint(1, 3)
            child1, child2 = single_point_crossover(parent1, parent2, point)

            child1 = mutate(child1, pm)
            child2 = mutate(child2, pm)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]

    return history

# ============================================
# Run required configuration
# ============================================
if __name__ == "__main__":
    run_ga(pop_size=4, num_generations=10, pm=0.1, elitism=False)