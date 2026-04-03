import random
from Q6_part_a import demands

# ============================================
# Fitness
# ============================================
def ga_fitness(ch, demands):
    return sum(demands[i] for i in ch) - 50

# ============================================
# Initial population
# ============================================
def random_chromosome():
    return sorted(random.sample(range(36), 10))

# ============================================
# Tournament selection
# ============================================
def tournament(pop):
    sample = random.sample(pop, 3)
    return max(sample, key=lambda x: ga_fitness(x, demands))

# ============================================
# Ordered Crossover (OX)
# ============================================
def ordered_crossover(p1, p2):
    size = len(p1)
    a, b = sorted(random.sample(range(size), 2))

    child = [-1]*size
    child[a:b] = p1[a:b]

    fill = [x for x in p2 if x not in child]
    j = 0

    for i in range(size):
        if child[i] == -1:
            child[i] = fill[j]
            j += 1

    return sorted(child)

# ============================================
# Mutation
# ============================================
def ga_mutate(ch, pm):
    if random.random() < pm:
        idx = random.randint(0, 9)
        new_gene = random.choice(list(set(range(36)) - set(ch)))
        ch[idx] = new_gene
    return sorted(ch)

# ============================================
# GA
# ============================================
def run_driver_ga(pop_size, generations, pm):
    pop = [random_chromosome() for _ in range(pop_size)]

    best = None
    best_fit = -1

    for gen in range(generations):
        new_pop = []

        for _ in range(pop_size):
            p1 = tournament(pop)
            p2 = tournament(pop)

            child = ordered_crossover(p1, p2)
            child = ga_mutate(child, pm)

            new_pop.append(child)

        pop = new_pop

        for ch in pop:
            f = ga_fitness(ch, demands)
            if f > best_fit:
                best_fit = f
                best = ch

    return best, best_fit


if __name__ == "__main__":
    best, fit = run_driver_ga(30, 100, 0.1)
    print("Best Solution:", best)
    print("Fitness:", fit)