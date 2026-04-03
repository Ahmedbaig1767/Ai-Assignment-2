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
        # Randomly pick two queens to swap rows
        i, j = random.sample(range(len(board)), 2)

        # Swap the queens' rows
        board[i], board[j] = board[j], board[i]

        # If conflicts are reduced, keep the new configuration
        new_conflicts = count_conflicts(board)
        if new_conflicts < current_conflicts:
            current_conflicts = new_conflicts
            path.append(list(board))  # Add new board configuration to path
        else:
            # Undo the move if no improvement
            board[i], board[j] = board[j], board[i]

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

# Visualize the N-Queens board
def print_board(board):
    for row in range(8):
        line = ['.'] * 8
        line[board[row]] = 'Q'
        print(' '.join(line))

# Main function
def main():
    restarts, final_board = solve_nqueens_rrhc(100)
    print(f"Restarts needed: {restarts}")
    print("Final board (row indices where queens are placed):", final_board)
    print("\nVisual representation of the board:")
    print_board(final_board)

if __name__ == "__main__":
    main()