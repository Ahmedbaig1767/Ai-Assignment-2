import random


def first_choice_hc(landscape, start):
    """First-Choice HC: check left, then right; move on first improvement."""
    path = [start]
    current = start
    
    while True:
        current_value = landscape[current - 1]
        
        left = current - 1
        right = current + 1
        
        moved = False
        
        if left >= 1:
            left_value = landscape[left - 1]
            if left_value > current_value:
                current = left
                path.append(current)
                moved = True
        
        if not moved and right <= len(landscape):
            right_value = landscape[right - 1]
            if right_value > current_value:
                current = right
                path.append(current)
                moved = True
        
        if not moved:
            break
    
    return path, current


def stochastic_hc(landscape, start):
    """Stochastic HC: collect all strictly uphill neighbours, pick one randomly."""
    path = [start]
    current = start
    
    while True:
        current_value = landscape[current - 1]
        uphill_neighbours = []
        
        left = current - 1
        right = current + 1
        
        if left >= 1:
            left_value = landscape[left - 1]
            if left_value > current_value:
                uphill_neighbours.append(left)
        
        if right <= len(landscape):
            right_value = landscape[right - 1]
            if right_value > current_value:
                uphill_neighbours.append(right)
        
        if not uphill_neighbours:
            break
        
        current = random.choice(uphill_neighbours)
        path.append(current)
    
    return path, current


def main():
    landscape = [4, 9, 6, 11, 8, 15, 10, 7, 13, 5, 16, 12]
    global_max_state = 11
    
    print("=" * 120)
    print("PART (B): ANALYSIS - GLOBAL MAXIMUM REACHES AND DIVERGENCE")
    print("=" * 120)
    print()
    
    fc_results = []
    stoch_results = []
    
    print(f"{'Start':>5} {'Algorithm':<15} {'Path':<50} {'Terminal':<10} {'Steps':<8}")
    print("-" * 120)
    
    for start in range(1, 13):
        fc_path, fc_terminal = first_choice_hc(landscape, start)
        fc_results.append((start, fc_path, fc_terminal))
        print(f"{start:>5} {'First-Choice':<15} {str(fc_path):<50} {fc_terminal:<10} {len(fc_path)-1:<8}")
        
        stoch_path, stoch_terminal = stochastic_hc(landscape, start)
        stoch_results.append((start, stoch_path, stoch_terminal))
        print(f"{start:>5} {'Stochastic':<15} {str(stoch_path):<50} {stoch_terminal:<10} {len(stoch_path)-1:<8}")
        print()
    
    fc_to_global = sum(1 for _, _, terminal in fc_results if terminal == global_max_state)
    stoch_to_global = sum(1 for _, _, terminal in stoch_results if terminal == global_max_state)
    
    print("\n" + "=" * 80)
    print("SUMMARY: STARTING STATES REACHING GLOBAL MAXIMUM (STATE 11)")
    print("=" * 80)
    print(f"{'Algorithm':<20} {'Count':<10} {'Starting States':<50}")
    print("-" * 80)
    fc_starts = [start for start, _, terminal in fc_results if terminal == global_max_state]
    stoch_starts = [start for start, _, terminal in stoch_results if terminal == global_max_state]
    print(f"{'First-Choice':<20} {fc_to_global:<10} {str(fc_starts):<50}")
    print(f"{'Stochastic':<20} {stoch_to_global:<10} {str(stoch_starts):<50}")
    
    print("\n" + "=" * 80)
    print("DIVERGENCE ANALYSIS: DIFFERENT TERMINAL STATES")
    print("=" * 80)
    divergences = []
    for i, (start, fc_term) in enumerate([(s, t) for s, _, t in fc_results]):
        stoch_term = stoch_results[i][2]
        if fc_term != stoch_term:
            divergences.append((start, fc_term, stoch_term))
    
    if divergences:
        print(f"{'Start':<8} {'FC Terminal':<15} {'Stoch Terminal':<15} {'Explanation':<60}")
        print("-" * 80)
        for start, fc_term, stoch_term in divergences:
            fc_val = landscape[fc_term - 1]
            stoch_val = landscape[stoch_term - 1]
            explanation = f"FC: {fc_val}, Stoch: {stoch_val} (deterministic vs random choice)"
            print(f"{start:<8} {fc_term:<15} {stoch_term:<15} {explanation:<60}")
    else:
        print("No divergences found.")
    
    print("\n" + "=" * 80)
    print("STOCHASTIC HC RELIABILITY: 50 RUNS FROM START STATE 4")
    print("=" * 80)
    runs_to_global = 0
    terminal_state_counts = {}
    
    for _ in range(50):
        _, terminal = stochastic_hc(landscape, 4)
        if terminal == global_max_state:
            runs_to_global += 1
        terminal_state_counts[terminal] = terminal_state_counts.get(terminal, 0) + 1
    
    print(f"Runs reaching state 11 (global max): {runs_to_global}/50 ({100*runs_to_global/50:.1f}%)")
    print(f"Distribution of terminal states: {sorted(terminal_state_counts.items())}")
    print(f"\nInterpretation: Stochastic HC from state 4 shows {'high' if runs_to_global >= 40 else 'moderate' if runs_to_global >= 20 else 'low'} reliability")
    print(f"in reaching the global maximum. The randomness in state selection means the algorithm can escape")
    print(f"some local maxima but may also land in others depending on the random choices made during the search.")


if __name__ == "__main__":
    main()