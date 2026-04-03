import random

def get_neighbors(state, n):
    neighbors = []
    if state > 0:
        neighbors.append(state - 1)
    if state < n - 1:
        neighbors.append(state + 1)
    return neighbors

def first_choice(landscape, start):
    current = start
    path = [current]

    while True:
        neighbors = get_neighbors(current, len(landscape))
        moved = False

        for n in neighbors:
            if landscape[n] > landscape[current]:
                current = n
                path.append(current)
                moved = True
                break

        if not moved:
            break

    return current, landscape[current], path

def stochastic(landscape, start):
    current = start
    path = [current]

    while True:
        neighbors = get_neighbors(current, len(landscape))
        uphill = [n for n in neighbors if landscape[n] > landscape[current]]

        if not uphill:
            break

        current = random.choice(uphill)
        path.append(current)

    return current, landscape[current], path

def random_restart_hc(landscape, num_restarts, variant="first_choice"):
    results = []
    best_state = None
    best_value = -1

    for _ in range(num_restarts):
        start = random.randint(0, len(landscape) - 1)

        if variant == "first_choice":
            state, value, path = first_choice(landscape, start)
        else:
            state, value, path = stochastic(landscape, start)

        results.append((start, state, value))

        if value > best_value:
            best_value = value
            best_state = state

    return best_state, best_value, results

def find_local_maxima(landscape):
    maxima = []
    for i in range(len(landscape)):
        neighbors = get_neighbors(i, len(landscape))
        if all(landscape[i] >= landscape[n] for n in neighbors):
            maxima.append(i)
    return maxima


if __name__ == "__main__":
    landscape = [5, 8, 6, 12, 9, 7, 17, 14, 10, 6, 19, 15, 11, 8]

    print("First Choice RRHC")
    best, val, res = random_restart_hc(landscape, 20, "first_choice")
    print("Best:", best, val)
    print("Runs:", res)

    print("\nStochastic RRHC")
    best, val, res = random_restart_hc(landscape, 20, "stochastic")
    print("Best:", best, val)
    print("Runs:", res)

    print("\nLocal Maxima:", find_local_maxima(landscape))