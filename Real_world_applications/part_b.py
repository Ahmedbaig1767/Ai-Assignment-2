import random
from Q6_part_a import state_fitness, random_state, get_neighbours, demands

# ============================================
# Hill Climbing
# ============================================
def hc_driver(state, demands, variant="stochastic"):
    current = state
    current_fit = state_fitness(current, demands)
    steps = 0

    while True:
        neighbours = get_neighbours(current)
        improved = False

        if variant == "first_choice":
            random.shuffle(neighbours)
            for n in neighbours:
                if state_fitness(n, demands) > current_fit:
                    current = n
                    current_fit = state_fitness(n, demands)
                    improved = True
                    break

        else:  # stochastic
            better = [n for n in neighbours if state_fitness(n, demands) > current_fit]
            if better:
                current = random.choice(better)
                current_fit = state_fitness(current, demands)
                improved = True

        if not improved:
            break

        steps += 1

    return current, current_fit, steps

# ============================================
# RRHC
# ============================================
def rrhc_driver(num_restarts, demands):
    best_state = None
    best_fit = -1
    history = []

    for _ in range(num_restarts):
        st = random_state()
        final_state, fit, _ = hc_driver(st, demands)

        history.append(fit)

        if fit > best_fit:
            best_fit = fit
            best_state = final_state

    return best_state, best_fit, history


if __name__ == "__main__":
    best_state, best_fit, history = rrhc_driver(30, demands)

    print("Best State:", best_state)
    print("Best Fitness:", best_fit)
    print("Fitness per restart:", history)