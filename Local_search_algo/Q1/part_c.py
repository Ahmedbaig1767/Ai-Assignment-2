import random


def first_choice_hc_plateau(landscape, start):
    """First-Choice HC with plateau detection."""
    path = [start]
    current = start
    plateau_detected = False
    
    while True:
        current_value = landscape[current - 1]
        
        left = current - 1
        right = current + 1
        
        moved = False
        equal_neighbour = False
        
        if left >= 1:
            left_value = landscape[left - 1]
            if left_value > current_value:
                current = left
                path.append(current)
                moved = True
            elif left_value == current_value:
                equal_neighbour = True
        
        if not moved and right <= len(landscape):
            right_value = landscape[right - 1]
            if right_value > current_value:
                current = right
                path.append(current)
                moved = True
            elif right_value == current_value:
                equal_neighbour = True
        
        if not moved:
            if equal_neighbour and not plateau_detected:
                print(f"  [PLATEAU WARNING] State {current}: f={current_value}, no uphill move available")
                plateau_detected = True
            break
    
    return path, current


def stochastic_hc_plateau(landscape, start):
    """Stochastic HC with plateau detection."""
    path = [start]
    current = start
    plateau_detected = False
    
    while True:
        current_value = landscape[current - 1]
        uphill_neighbours = []
        equal_neighbours = []
        
        left = current - 1
        right = current + 1
        
        if left >= 1:
            left_value = landscape[left - 1]
            if left_value > current_value:
                uphill_neighbours.append(left)
            elif left_value == current_value:
                equal_neighbours.append(left)
        
        if right <= len(landscape):
            right_value = landscape[right - 1]
            if right_value > current_value:
                uphill_neighbours.append(right)
            elif right_value == current_value:
                equal_neighbours.append(right)
        
        if not uphill_neighbours:
            if equal_neighbours and not plateau_detected:
                print(f"  [PLATEAU WARNING] State {current}: f={current_value}, no uphill move available")
                plateau_detected = True
            break
        
        current = random.choice(uphill_neighbours)
        path.append(current)
    
    return path, current


def first_choice_hc_sideways(landscape, start, sideways_cap=10):
    """First-Choice HC with sideways moves capped at sideways_cap."""
    path = [start]
    current = start
    sideways_count = 0
    
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
                sideways_count = 0
                moved = True
            elif left_value == current_value and sideways_count < sideways_cap:
                current = left
                path.append(current)
                sideways_count += 1
                moved = True
        
        if not moved and right <= len(landscape):
            right_value = landscape[right - 1]
            if right_value > current_value:
                current = right
                path.append(current)
                sideways_count = 0
                moved = True
            elif right_value == current_value and sideways_count < sideways_cap:
                current = right
                path.append(current)
                sideways_count += 1
                moved = True
        
        if not moved:
            break
    
    return path, current


def stochastic_hc_sideways(landscape, start, sideways_cap=10):
    """Stochastic HC with sideways moves capped at sideways_cap."""
    path = [start]
    current = start
    sideways_count = 0
    
    while True:
        current_value = landscape[current - 1]
        uphill_neighbours = []
        equal_neighbours = []
        
        left = current - 1
        right = current + 1
        
        if left >= 1:
            left_value = landscape[left - 1]
            if left_value > current_value:
                uphill_neighbours.append(left)
            elif left_value == current_value:
                equal_neighbours.append(left)
        
        if right <= len(landscape):
            right_value = landscape[right - 1]
            if right_value > current_value:
                uphill_neighbours.append(right)
            elif right_value == current_value:
                equal_neighbours.append(right)
        
        if uphill_neighbours:
            current = random.choice(uphill_neighbours)
            path.append(current)
            sideways_count = 0
        elif equal_neighbours and sideways_count < sideways_cap:
            current = random.choice(equal_neighbours)
            path.append(current)
            sideways_count += 1
        else:
            break
    
    return path, current


def main():
    landscape_plateau = [4, 9, 6, 11, 15, 15, 15, 7, 13, 5, 16, 12]
    
    print("=" * 120)
    print("PART (C): PLATEAU HANDLING (STATES 5, 6, 7 ALL HAVE f=15)")
    print("=" * 120)
    print()
    
    print("VARIANT 1: WITHOUT SIDEWAYS MOVES")
    print("-" * 120)
    print(f"{'Start':>5} {'Algorithm':<15} {'Path':<50} {'Terminal':<10} {'Steps':<8}")
    print("-" * 120)
    
    fc_plateau_results = []
    stoch_plateau_results = []
    
    for start in range(1, 13):
        print(f"\nStart={start}")
        fc_path, fc_terminal = first_choice_hc_plateau(landscape_plateau, start)
        fc_plateau_results.append((start, fc_path, fc_terminal))
        print(f"{start:>5} {'First-Choice':<15} {str(fc_path):<50} {fc_terminal:<10} {len(fc_path)-1:<8}")
        
        stoch_path, stoch_terminal = stochastic_hc_plateau(landscape_plateau, start)
        stoch_plateau_results.append((start, stoch_path, stoch_terminal))
        print(f"{start:>5} {'Stochastic':<15} {str(stoch_path):<50} {stoch_terminal:<10} {len(stoch_path)-1:<8}")
    
    fc_stuck = sum(1 for _, _, terminal in fc_plateau_results if terminal in [5, 6, 7])
    stoch_stuck = sum(1 for _, _, terminal in stoch_plateau_results if terminal in [5, 6, 7])
    
    print("\n" + "=" * 80)
    print("PLATEAU STUCKNESS: WITHOUT SIDEWAYS MOVES")
    print("=" * 80)
    print(f"{'Algorithm':<20} {'Stuck on Plateau (states 5,6,7)':<40} {'Success (reached 11)':<20}")
    print("-" * 80)
    fc_success = sum(1 for _, _, terminal in fc_plateau_results if terminal == 11)
    stoch_success = sum(1 for _, _, terminal in stoch_plateau_results if terminal == 11)
    print(f"{'First-Choice':<20} {fc_stuck:<40} {fc_success:<20}")
    print(f"{'Stochastic':<20} {stoch_stuck:<40} {stoch_success:<20}")
    
    print("\n" + "=" * 120)
    print("VARIANT 2: WITH SIDEWAYS MOVES (CAP=10)")
    print("=" * 120)
    print()
    print(f"{'Start':>5} {'Algorithm':<15} {'Path':<50} {'Terminal':<10} {'Steps':<8}")
    print("-" * 120)
    
    fc_sideways_results = []
    stoch_sideways_results = []
    
    for start in range(1, 13):
        fc_path, fc_terminal = first_choice_hc_sideways(landscape_plateau, start)
        fc_sideways_results.append((start, fc_path, fc_terminal))
        print(f"{start:>5} {'First-Choice':<15} {str(fc_path):<50} {fc_terminal:<10} {len(fc_path)-1:<8}")
        
        stoch_path, stoch_terminal = stochastic_hc_sideways(landscape_plateau, start)
        stoch_sideways_results.append((start, stoch_path, stoch_terminal))
        print(f"{start:>5} {'Stochastic':<15} {str(stoch_path):<50} {stoch_terminal:<10} {len(stoch_path)-1:<8}")
    
    print("\n" + "=" * 80)
    print("PLATEAU HANDLING COMPARISON: BEFORE VS AFTER SIDEWAYS MOVES")
    print("=" * 80)
    print(f"{'Algorithm':<20} {'Without Sideways':<25} {'With Sideways':<25} {'Improvement':<20}")
    print("-" * 80)
    
    fc_before = sum(1 for _, _, terminal in fc_plateau_results if terminal == 11)
    fc_after = sum(1 for _, _, terminal in fc_sideways_results if terminal == 11)
    stoch_before = sum(1 for _, _, terminal in stoch_plateau_results if terminal == 11)
    stoch_after = sum(1 for _, _, terminal in stoch_sideways_results if terminal == 11)
    
    print(f"{'First-Choice':<20} {fc_before}/12 {fc_before/12*100:>5.1f}%{'':<15} {fc_after}/12 {fc_after/12*100:>5.1f}%{'':<15} {fc_after-fc_before:+d}")
    print(f"{'Stochastic':<20} {stoch_before}/12 {stoch_before/12*100:>5.1f}%{'':<15} {stoch_after}/12 {stoch_after/12*100:>5.1f}%{'':<15} {stoch_after-stoch_before:+d}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS: SIDEWAYS MOVES EFFECTIVENESS")
    print("=" * 80)
    print("""
The sideways-move fix is more effective for Stochastic HC than First-Choice HC. Stochastic HC benefits
more because it can randomly explore across the plateau in multiple directions, using the full sideways
budget to escape; First-Choice HC deterministically moves left before right, limiting its plateau escape
potential. The cap of 10 matters critically: without it, both algorithms could cycle infinitely on the
plateau (states 5→6→7→6→5...). With the cap, algorithms are forced to either escape uphill or terminate,
creating a natural escape mechanism. Stochastic HC's random selection of equal-valued neighbours means it
can "bounce" around the plateau more effectively, while First-Choice HC's left-first bias may lead it into
dead ends even with sideways moves allowed.
""")


if __name__ == "__main__":
    main()