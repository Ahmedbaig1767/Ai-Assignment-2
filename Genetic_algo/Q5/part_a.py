import random

# ============================================
# Generate random chromosome
# ============================================
def random_chromosome():
    chromosome = []
    for _ in range(6):  # 6 courses
        room = random.randint(0, 2)   # 3 rooms
        slot = random.randint(0, 3)   # 4 time slots
        chromosome.append((room, slot))
    return chromosome

# ============================================
# Count conflicts
# ============================================
def count_conflicts(chromosome):
    conflicts = 0
    n = len(chromosome)

    for i in range(n):
        for j in range(i+1, n):
            if chromosome[i] == chromosome[j]:
                conflicts += 1
    return conflicts

# ============================================
# Fitness function
# ============================================
def fitness(chromosome):
    conflicts = count_conflicts(chromosome)
    return 100 - (10 * conflicts)

# ============================================
# Test: Generate 5 chromosomes
# ============================================
if __name__ == "__main__":
    print("Chromosome | Conflicts | Fitness\n")

    for _ in range(5):
        ch = random_chromosome()
        c = count_conflicts(ch)
        f = fitness(ch)
        print(f"{ch} | {c} | {f}")