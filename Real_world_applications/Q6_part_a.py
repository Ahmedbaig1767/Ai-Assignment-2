import random

demands = [12,45,23,67,34,19, 56,38,72,15,49,61,
           27,83,41,55,30,77, 64,18,52,39,71,26,
           44,91,33,58,22,85, 16,69,47,74,31,53]

# ============================================
# Fitness
# ============================================
def state_fitness(state, demands):
    return sum(demands[i] for i in state) - (5 * 10)

# ============================================
# Random state
# ============================================
def random_state():
    return set(random.sample(range(36), 10))

# ============================================
# Neighbours
# ============================================
def get_neighbours(state):
    neighbours = []
    all_zones = set(range(36))
    unused = list(all_zones - state)

    for s in state:
        for u in unused:
            new_state = set(state)
            new_state.remove(s)
            new_state.add(u)
            neighbours.append(new_state)

    return neighbours

# ============================================
# Test
# ============================================
if __name__ == "__main__":
    for i in range(3):
        st = random_state()
        print("State:", st)
        print("Fitness:", state_fitness(st, demands))
        print("Neighbours:", len(get_neighbours(st)))
        print()