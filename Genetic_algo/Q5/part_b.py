import random
from part_a import random_chromosome, count_conflicts, fitness

# ============================================
# Crossover
# ============================================
def crossover(p1, p2, point):
    c1 = p1[:point] + p2[point:]
    c2 = p2[:point] + p1[point:]
    return c1, c2

# ============================================
# Repair function
# ============================================
def repair(chromosome):
    seen = {}

    for i in range(len(chromosome)):
        if chromosome[i] in seen:
            # conflict found → reassign
            while True:
                new_gene = (random.randint(0,2), random.randint(0,3))
                if new_gene not in chromosome:
                    chromosome[i] = new_gene
                    break
        else:
            seen[chromosome[i]] = True

    return chromosome

# ============================================
# Mutation
# ============================================
def mutate(chromosome, pm):
    for i in range(len(chromosome)):
        if random.random() < pm:
            chromosome[i] = (random.randint(0,2), random.randint(0,3))
    return chromosome

# ============================================
# Demonstration
# ============================================
if __name__ == "__main__":

    # Example parents
    p1 = random_chromosome()
    p2 = random_chromosome()

    print("Parent 1:", p1)
    print("Parent 2:", p2)

    c1, c2 = crossover(p1, p2, 3)

    print("\nAfter Crossover:")
    print("Child 1:", c1, "Conflicts:", count_conflicts(c1))
    print("Child 2:", c2, "Conflicts:", count_conflicts(c2))

    # Create conflict manually
    conflict_ch = [(0,0),(0,0),(1,1),(2,2),(1,2),(2,3)]

    print("\nBefore Repair:", conflict_ch, "Conflicts:", count_conflicts(conflict_ch))
    repaired = repair(conflict_ch)
    print("After Repair:", repaired, "Conflicts:", count_conflicts(repaired))