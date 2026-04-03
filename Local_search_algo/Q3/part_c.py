import random

# Count the number of attacking pairs of queens (conflicts)
def count_conflicts(board):
    conflicts = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            # Check if queens are in the same row or diagonal
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

# Stochastic Hill Climbing for N-Queens
def stochastic_hc_nqueens(board):
    path = [list(board)]  # Store the path of board configurations
    current_conflicts = count_conflicts(board)
    
    while current_conflicts > 0:
        # Generate random neighbours (swap any two queens)
        neighbours = []
        for i in range(len(board)):
            for j in range(i + 1, len(board)):
                new_board = board[:]
                new_board[i], new_board[j] = new_board[j], new_board[i]  # Swap queens
                neighbours.append((new_board, count_conflicts(new_board)))

        # Sort neighbours by fitness (conflicts) and pick the best one
        neighbours.sort(key=lambda x: x[1])  # Sort by conflict count
        best_neighbour, best_fitness = neighbours[0]

        # If the best neighbour reduces conflicts, move to it
        if best_fitness < current_conflicts:
            board = best_neighbour
            current_conflicts = best_fitness
            path.append(list(board))  # Store the path of board configurations
        else:
            break  # No improvement, stop the search

    return path, board

# Solve N-Queens using Random Restarts
def solve_nqueens_rrhc(num_restarts):
    best_board = None
    best_conflicts = float('inf')
    restart_count = 0

    while restart_count < num_restarts:
        # Start with a random board
        board = random.sample(range(8), 8)

        # Perform Stochastic Hill Climbing to solve the board
        path, solution_board = stochastic_hc_nqueens(board)

        # If no conflicts (a solution is found)
        if count_conflicts(solution_board) == 0:
            best_board = solution_board
            break

        restart_count += 1

    return restart_count, best_board

# Function to run the experiment for multiple values of k
def run_experiment(k_values, num_trials):
    results = []

    for k in k_values:
        success_count = 0
        total_restarts = 0

        for _ in range(num_trials):
            restarts, final_board = solve_nqueens_rrhc(k)
            if final_board is not None:  # If a solution was found
                success_count += 1
                total_restarts += restarts

        # Calculate success rate and average restarts
        success_rate = success_count / num_trials
        avg_restarts = total_restarts / success_count if success_count > 0 else 0

        results.append([k, success_rate, avg_restarts])

    return results

# Main function to display results
def main():
    k_values = [5, 10, 25, 50, 100]
    num_trials = 30
    results = run_experiment(k_values, num_trials)

    print(f"{'k':<10} {'Success Rate':<20} {'Avg. Restarts to Solution'}")
    for result in results:
        k, success_rate, avg_restarts = result
        print(f"{k:<10} {success_rate:<20.2f} {avg_restarts:.2f}")

if __name__ == "__main__":
    main()