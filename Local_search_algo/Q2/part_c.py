import random
from part_a import random_restart_hc

def plateau_rrhc(landscape, num_restarts):
    plateau_count = 0
    best_state = None
    best_value = -1

    for _ in range(num_restarts):
        start = random.randint(0, len(landscape) - 1)

        current = start
        plateau_counter = 0

        while True:
            neighbors = []
            if current > 0:
                neighbors.append(current - 1)
            if current < len(landscape) - 1:
                neighbors.append(current + 1)

            uphill = [n for n in neighbors if landscape[n] > landscape[current]]
            equal = [n for n in neighbors if landscape[n] == landscape[current]]

            if uphill:
                current = random.choice(uphill)
                plateau_counter = 0
            elif equal and plateau_counter < 5:
                current = random.choice(equal)
                plateau_counter += 1
            else:
                break

        if landscape[current] == 17:
            plateau_count += 1

        if landscape[current] > best_value:
            best_value = landscape[current]
            best_state = current

    return plateau_count, best_state, best_value


if __name__ == "__main__":
    landscape = [5, 8, 6, 12, 17, 17, 17, 14, 10, 6, 19, 15, 11, 8]

    plateau_hits, best, val = plateau_rrhc(landscape, 20)

    print("Plateau restarts:", plateau_hits)
    print("Best:", best, val)