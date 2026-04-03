import random

# Diagnose Hill Climbing detects local maxima, plateau and ridge
def diagnose_hc(landscape, start):
    current = start
    path = [current]
    visited = set([current])  # To detect (ridge)
    previous_state = None     # To track previous state for detecting ridge

    while True:
        current_value = landscape[current]
        moved = False

        # Check left neighbour first
        if current > 0:
            left = current - 1
            if landscape[left] > current_value:  # A better neighbour found
                current = left
                path.append(current)
                moved = True
            elif landscape[left] == current_value:  # Plateau detected
                print(f"Terminated at state {current} with f={current_value}. Failure mode: Plateau")
                return

        # Check right neighbour (if not moved yet)
        if not moved and current < len(landscape) - 1:
            right = current + 1
            if landscape[right] > current_value:  # A better neighbour found
                current = right
                path.append(current)
                moved = True
            elif landscape[right] == current_value:  # Plateau detected
                print(f"Terminated at state {current} with f={current_value}. Failure mode: Plateau")
                return

        # Detect local maximum: No better neighbors and no equal-value neighbours
        if not moved:
            left_value = landscape[current - 1] if current > 0 else float('-inf')
            right_value = landscape[current + 1] if current < len(landscape) - 1 else float('-inf')
            if current_value > left_value and current_value > right_value:
                print(f"Terminated at state {current} with f={current_value}. Failure mode: Local Maximum")
                return

        # Detect ridge (oscillation between states)
        if current in visited:
            if current == previous_state:  # Oscillating back and forth
                print(f"Terminated at state {current} with f={current_value}. Failure mode: Ridge")
                return

        visited.add(current)
        previous_state = current  # Update previous state


landscape_1 = [5, 8, 6, 4, 3]
landscape_2 = [5, 6, 7, 7, 6]
landscape_3 = [3,7,3,7,3,7]



diagnose_hc(landscape_1, 1)

diagnose_hc(landscape_2, 2)

diagnose_hc(landscape_3, 0)