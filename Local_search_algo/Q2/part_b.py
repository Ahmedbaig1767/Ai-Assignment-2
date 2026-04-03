import random
from part_a import random_restart_hc

def experiment(landscape, r, trials):
    success = 0

    for _ in range(trials):
        best, val, _ = random_restart_hc(landscape, r, "first_choice")
        if val == max(landscape):
            success += 1

    return success / trials


if __name__ == "__main__":
    landscape = [5, 8, 6, 12, 9, 7, 17, 14, 10, 6, 19, 15, 11, 8]
    trials = 100

    print("r\tEmpirical\tTheoretical")

    for r in [1, 3, 5, 10, 20]:
        p = 1 / len(landscape)
        empirical = experiment(landscape, r, trials)
        theoretical = 1 - (1 - p) ** r

        print(r, "\t", round(empirical, 3), "\t\t", round(theoretical, 3))