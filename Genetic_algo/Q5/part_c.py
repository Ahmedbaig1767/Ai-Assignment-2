import random
from part_a import random_chromosome, count_conflicts, fitness
from part_b import crossover, repair, mutate

# ============================================
# Tournament Selection
# ============================================
def tournament_select(pop):
    a = random.choice(pop)
    b = random.choice(pop)
    return a if fitness(a) > fitness(b) else b

# ============================================
# GA
# ============================================
def run_scheduling_ga(pop_size, generations, pm):

    population = [random_chromosome() for _ in range(pop_size)]

    best_overall = None
    best_fit = -1

    for gen in range(generations):

        new_population = []

        for _ in range(pop_size // 2):
            p1 = tournament_select(population)
            p2 = tournament_select(population)

            c1, c2 = crossover(p1, p2, random.randint(1,5))

            c1 = repair(c1)
            c2 = repair(c2)

            c1 = mutate(c1, pm)
            c2 = mutate(c2, pm)

            new_population.extend([c1, c2])

        population = new_population

        # Track best
        for ch in population:
            f = fitness(ch)
            if f > best_fit:
                best_fit = f
                best_overall = ch

        print(f"Generation {gen}: Best Fitness = {best_fit}")

        if best_fit == 100:
            print(f"Solution found at generation {gen}: {best_overall}")
            break

    print("\nFinal Best Schedule:", best_overall)
    print("Conflicts:", count_conflicts(best_overall))


# ============================================
# Run
# ============================================
if __name__ == "__main__":
    run_scheduling_ga(20, 50, 0.1)