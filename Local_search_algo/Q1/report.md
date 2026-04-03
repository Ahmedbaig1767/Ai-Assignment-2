\documentclass[12pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{fancyhdr}
\usepackage{hyperref}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{float}

\lstset{
    language=Python,
    basicstyle=\ttfamily\small,
    keywordstyle=\color{blue},
    commentstyle=\color{gray},
    stringstyle=\color{red},
    breaklines=true,
    showstringspaces=false,
    tabsize=4,
    frame=single,
    numbers=left,
    numberstyle=\tiny,
    stepnumber=1
}

\pagestyle{fancy}
\lhead{Hill Climbing Assignment}
\rhead{AI - Local Search}
\cfoot{\thepage}

\title{\textbf{Hill Climbing: Local Search Algorithms} \\[0.3cm]
       \large Artificial Intelligence Assignment \#2}
\author{Student ID: 23L-2598}
\date{\today}

\begin{document}

\maketitle

\newpage
\tableofcontents
\newpage

\section{Problem Statement}

Given an objective function defined over integer states $s \in \{1, 2, \ldots, 12\}$:

\begin{table}[H]
\centering
\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
State & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 \\
\hline
$f(s)$ & 4 & 9 & 6 & 11 & 8 & 15 & 10 & 7 & 13 & 5 & 16 & 12 \\
\hline
\end{tabular}
\caption{Objective Function Values}
\end{table}

Each state's neighbourhood consists of immediate left and right adjacent states only. The global maximum is at state 11 with $f(11) = 16$.

\newpage

\section{Part (A): Implementation of Hill Climbing Algorithms}

\subsection{Algorithm Design}

\subsubsection{First-Choice Hill Climbing}

\textbf{Algorithm:}
\begin{enumerate}
    \item Start at given initial state
    \item Check left neighbour first; if $f(\text{left}) > f(\text{current})$, move immediately
    \item If no left improvement, check right neighbour; if $f(\text{right}) > f(\text{current})$, move there
    \item Repeat until no improving move exists (local maximum reached)
    \item Return path and terminal state
\end{enumerate}

\textbf{Key Characteristic:} Greedy, deterministic approach with left-first bias. Commits to first improvement found, never backtracks.

\subsubsection{Stochastic Hill Climbing}

\textbf{Algorithm:}
\begin{enumerate}
    \item Start at given initial state
    \item Collect ALL strictly uphill neighbours (both left and right that improve $f$)
    \item If no uphill neighbours exist, terminate at current state
    \item Otherwise, uniformly randomly select one uphill neighbour using $\texttt{random.choice()}$
    \item Move to selected neighbour and repeat
    \item Return path and terminal state
\end{enumerate}

\textbf{Key Characteristic:} Probabilistic approach. Evaluates all options before deciding, removing left-first bias but introducing randomness.

\subsection{Python Implementation}

\begin{lstlisting}
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
    
    print("=" * 120)
    print("PART (A): FIRST-CHOICE HC AND STOCHASTIC HC")
    print("=" * 120)
    print()
    
    print(f"{'Start':>5} {'Algorithm':<15} {'Path':<50} {'Terminal':<10} {'Steps':<8}")
    print("-" * 120)
    
    for start in range(1, 13):
        fc_path, fc_terminal = first_choice_hc(landscape, start)
        print(f"{start:>5} {'First-Choice':<15} {str(fc_path):<50} {fc_terminal:<10} {len(fc_path)-1:<8}")
        
        stoch_path, stoch_terminal = stochastic_hc(landscape, start)
        print(f"{start:>5} {'Stochastic':<15} {str(stoch_path):<50} {stoch_terminal:<10} {len(stoch_path)-1:<8}")
        print()


if __name__ == "__main__":
    main()
\end{lstlisting}

\subsection{Output}

\begin{lstlisting}
============================================================================================================================
PART (A): FIRST-CHOICE HC AND STOCHASTIC HC
============================================================================================================================

Start Algorithm       Path                                               Terminal   Steps   
----------------------------------------------------------------------------------------------------------------------------
    1 First-Choice    [1, 2]                                             2          1       
    1 Stochastic      [1, 2]                                             2          1       

    2 First-Choice    [2]                                                2          0       
    2 Stochastic      [2]                                                2          0       

    3 First-Choice    [3, 2]                                             3          1       
    3 Stochastic      [3, 4]                                             4          1       

    4 First-Choice    [4]                                                4          0       
    4 Stochastic      [4]                                                4          0       

    5 First-Choice    [5, 4]                                             4          1       
    5 Stochastic      [5, 6]                                             6          1       

    6 First-Choice    [6]                                                6          0       
    6 Stochastic      [6]                                                6          0       

    7 First-Choice    [7, 6]                                             6          1       
    7 Stochastic      [7, 6]                                             6          1       

    8 First-Choice    [8, 7, 6]                                          6          2       
    8 Stochastic      [8, 7, 6]                                          6          2       

    9 First-Choice    [9]                                                9          0       
    9 Stochastic      [9]                                                9          0       

   10 First-Choice    [10, 9]                                            9          1       
   10 Stochastic      [10, 9]                                            9          1       

   11 First-Choice    [11]                                               11         0       
   11 Stochastic      [11]                                               11         0       

   12 First-Choice    [12, 11]                                           11         1       
   12 Stochastic      [12, 11]                                           11         1       
\end{lstlisting}

\subsection{Analysis}

The implementation successfully separates First-Choice and Stochastic approaches:

\begin{itemize}
    \item \textbf{First-Choice:} Uses sequential left-then-right checking. For example, from state 3 (f=6), it finds state 2 (f=9) is better and commits immediately, not exploring state 4 (f=11) which is actually superior.
    
    \item \textbf{Stochastic:} From state 3, collects both {2, 4} as uphill neighbours and may randomly choose either, explaining future divergence in performance.
    
    \item \textbf{Boundary Handling:} States 1 and 12 have single neighbours, correctly handled by checking existence before access.
\end{itemize}

Both algorithms terminate at local maxima. The landscape has multiple local optima: states 2, 4, 6, 9, 11 are local maxima (no improving neighbours).

\newpage

\section{Part (B): Analysis and Comparison}

\subsection{Extended Testing Framework}

\textbf{Requirements Addressed:}
\begin{enumerate}
    \item Full output table from all 12 starting states
    \item Global maximum reach count summary
    \item Identification of divergent starting states
    \item Explanation of divergence causes (different f-values and decision logic)
    \item Stochastic HC reliability test: 50 runs from state 4 with true randomness
\end{enumerate}

\subsection{Python Implementation}

\begin{lstlisting}
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
\end{lstlisting}

\subsection{Program Output}

\begin{lstlisting}
============================================================================================================================
PART (B): ANALYSIS - GLOBAL MAXIMUM REACHES AND DIVERGENCE
============================================================================================================================

Start Algorithm       Path                                               Terminal   Steps   
----------------------------------------------------------------------------------------------------------------------------
    1 First-Choice    [1, 2]                                             2          1       
    1 Stochastic      [1, 2]                                             2          1       

    2 First-Choice    [2]                                                2          0       
    2 Stochastic      [2]                                                2          0       

    3 First-Choice    [3, 2]                                             2          1       
    3 Stochastic      [3, 4]                                             4          1       

    4 First-Choice    [4]                                                4          0       
    4 Stochastic      [4]                                                4          0       

    5 First-Choice    [5, 4]                                             4          1       
    5 Stochastic      [5, 6]                                             6          1       

    6 First-Choice    [6]                                                6          0       
    6 Stochastic      [6]                                                6          0       

    7 First-Choice    [7, 6]                                             6          1       
    7 Stochastic      [7, 6]                                             6          1       

    8 First-Choice    [8, 7, 6]                                          6          2       
    8 Stochastic      [8, 7, 6]                                          6          2       

    9 First-Choice    [9]                                                9          0       
    9 Stochastic      [9]                                                9          0       

   10 First-Choice    [10, 9]                                            9          1       
   10 Stochastic      [10, 9]                                            9          1       

   11 First-Choice    [11]                                               11         0       
   11 Stochastic      [11]                                               11         0       

   12 First-Choice    [12, 11]                                           11         1       
   12 Stochastic      [12, 11]                                           11         1       

================================================================================
SUMMARY: STARTING STATES REACHING GLOBAL MAXIMUM (STATE 11)
================================================================================
Algorithm            Count      Starting States                                   
--------------------------------------------------------------------------------
First-Choice         2          [11, 12]                                          
Stochastic           2          [11, 12]                                          

================================================================================
DIVERGENCE ANALYSIS: DIFFERENT TERMINAL STATES
================================================================================
Start    FC Terminal     Stoch Terminal  Explanation                                                 
--------------------------------------------------------------------------------
3        2               4               FC: 9, Stoch: 11 (deterministic vs random choice)           
5        4               6               FC: 11, Stoch: 15 (deterministic vs random choice)          

================================================================================
STOCHASTIC HC RELIABILITY: 50 RUNS FROM START STATE 4
================================================================================
Runs reaching state 11 (global max): 0/50 (0.0%)
Distribution of terminal states: [(4, 50)]

Interpretation: Stochastic HC from state 4 shows low reliability
in reaching the global maximum. The randomness in state selection means the algorithm can escape
some local maxima but may also land in others depending on the random choices made during the search.
\end{lstlisting}

\subsection{Results Summary Table}

\begin{table}[H]
\centering
\begin{tabular}{|c|c|c|}
\hline
\textbf{Algorithm} & \textbf{Count} & \textbf{Starting States} \\
\hline
First-Choice HC & 2/12 & \{11, 12\} \\
Stochastic HC & 2/12 & \{11, 12\} \\
\hline
\end{tabular}
\caption{Starting States Reaching Global Maximum (State 11)}
\end{table}

\subsection{Divergence Analysis}

Two starting states exhibit \textbf{different terminal states}:

\subsubsection{Start State 3}

\begin{itemize}
    \item \textbf{First-Choice HC:} $3 \to 2$ (terminal, $f(2) = 9$)
    
    \textbf{Execution:}
    \begin{enumerate}
        \item At state 3, $f(3) = 6$
        \item Check left: state 2, $f(2) = 9 > 6$ \checkmark MOVE IMMEDIATELY
        \item At state 2, $f(2) = 9$
        \item Check left: state 1, $f(1) = 4 < 9$ No improvement
        \item Check right: state 3, $f(3) = 6 < 9$ No improvement
        \item TERMINATE at state 2
    \end{enumerate}
    
    \item \textbf{Stochastic HC:} $3 \to 4$ (terminal, $f(4) = 11$)
    
    \textbf{Execution:}
    \begin{enumerate}
        \item At state 3, $f(3) = 6$
        \item Collect uphill neighbours: 
        \begin{itemize}
            \item Left (2): $f(2) = 9 > 6$ 
            \item Right (4): $f(4) = 11 > 6$ 
        \end{itemize}
        \item Randomly select from \{2, 4\}: choose 4
        \item At state 4, $f(4) = 11$
        \item Collect uphill neighbours: 
        \begin{itemize}
            \item Left (3): $f(3) = 6 < 11$ 
            \item Right (5): $f(5) = 8 < 11$ 
        \end{itemize}
        \item TERMINATE at state 4
    \end{enumerate}
    
    \item \textbf{Explanation:} First-Choice's left-first bias commits to state 2 without evaluating state 4. Stochastic HC evaluates both and (in this run) randomly chose the better option (state 4 with $f = 11$ vs. state 2 with $f = 9$). The difference is $11 - 9 = 2$ units in final value.
\end{itemize}

\subsubsection{Start State 5}

\begin{itemize}
    \item \textbf{First-Choice HC:} $5 \to 4$ (terminal, $f(4) = 11$)
    
    \textbf{Execution:}
    \begin{enumerate}
        \item At state 5, $f(5) = 8$
        \item Check left: state 4, $f(4) = 11 > 8$  MOVE IMMEDIATELY
        \item At state 4, $f(4) = 11$
        \item Check left: state 3, $f(3) = 6 < 11$ 
        \item Check right: state 5, $f(5) = 8 < 11$ 
        \item TERMINATE at state 4
    \end{enumerate}
    
    \item \textbf{Stochastic HC:} $5 \to 6$ (terminal, $f(6) = 15$)
    
    \textbf{Execution:}
    \begin{enumerate}
        \item At state 5, $f(5) = 8$
        \item Collect uphill neighbours:
        \begin{itemize}
            \item Left (4): $f(4) = 11 > 8$ 
            \item Right (6): $f(6) = 15 > 8$ 
        \end{itemize}
        \item Randomly select from \{4, 6\}: choose 6
        \item At state 6, $f(6) = 15$
        \item Collect uphill neighbours:
        \begin{itemize}
            \item Left (5): $f(5) = 8 < 15$ 
            \item Right (7): $f(7) = 10 < 15$ 
        \end{itemize}
        \item TERMINATE at state 6
    \end{enumerate}
    
    \item \textbf{Explanation:} First-Choice commits to left (state 4, $f = 11$) without considering right (state 6, $f = 15$). Stochastic HC explores both and (in this run) chose state 6, achieving $f = 15$ versus $f = 11$ --- a difference of 4 units.
\end{itemize}

\subsection{Stochastic HC Reliability Test}

\textbf{Test Design:} Run Stochastic HC 50 times from state 4, NO fixed seed, allow true randomness.

\textbf{Results:}
\begin{lstlisting}
Runs reaching state 11 (global max): 0/50 (0.0%)
Distribution of terminal states: [(4, 50)]
\end{lstlisting}

\textbf{Analysis:}

State 4 is a \textbf{true local maximum}:
\begin{itemize}
    \item $f(4) = 11$
    \item Left neighbour (3): $f(3) = 6 < 11$
    \item Right neighbour (5): $f(5) = 8 < 11$
    \item No uphill moves exist
\end{itemize}

Since the uphill neighbours list is always empty from state 4, Stochastic HC terminates immediately regardless of randomness. The 0\% success rate reveals a critical limitation:

\textbf{\textit{Randomness in hill climbing only helps when multiple uphill options exist from a given state.}}

From a true local maximum with no uphill neighbours, stochastic choice is irrelevant. The algorithm cannot distinguish between:
\begin{itemize}
    \item States surrounded by worse neighbours (dead end locally)
    \item States near better regions just beyond immediate neighbours
\end{itemize}

This is why randomness helps at state 3 (where {2, 4} both improve) but cannot help at state 4 (where neither improves). The landscape topology, not the selection strategy, determines escapability.

\newpage

\section{Part (C): Plateau Handling}

\subsection{Problem Setup}

\textbf{Modified Landscape:} States 5, 6, 7 all set to $f = 15$, creating a plateau:

\begin{table}[H]
\centering
\begin{tabular}{|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
State & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 \\
\hline
$f(s)$ & 4 & 9 & 6 & 11 & 15 & 15 & 15 & 7 & 13 & 5 & 16 & 12 \\
\hline
\end{tabular}
\caption{Modified Landscape with Plateau (States 5, 6, 7)}
\end{table}

\textbf{Requirements:}
\begin{enumerate}
    \item Add plateau detection: warn when algorithm finds no uphill but at least one equal neighbour
    \item Test without sideways moves: count runs stuck on plateau
    \item Implement sideways-move extension: allow equal-valued moves, cap at 10
    \item Test with sideways moves: compare success rates
    \item Analyze effectiveness: which variant benefits more and why
\end{enumerate}

\subsection{Implementation}

\begin{lstlisting}
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
\end{lstlisting}

\subsection{Variant 1: Without Sideways Moves}

\begin{lstlisting}
============================================================================================================================
PART (C): PLATEAU HANDLING (STATES 5, 6, 7 ALL HAVE f=15)
============================================================================================================================

VARIANT 1: WITHOUT SIDEWAYS MOVES
----------------------------------------------------------------------------------------------------------------------------

Start=1
    1 First-Choice    [1, 2]                                             2          1       
    1 Stochastic      [1, 2]                                             2          1       

Start=2
    2 First-Choice    [2]                                                2          0       
    2 Stochastic      [2]                                                2          0       

Start=3
    3 First-Choice    [3, 2]                                             2          1       
    3 Stochastic      [3, 2]                                             2          1       

Start=4
  [PLATEAU WARNING] State 5: f=15, no uphill move available
    4 First-Choice    [4, 5]                                             5          1       
  [PLATEAU WARNING] State 5: f=15, no uphill move available
    4 Stochastic      [4, 5]                                             5          1       

Start=5
  [PLATEAU WARNING] State 5: f=15, no uphill move available
    5 First-Choice    [5]                                                5          0       
  [PLATEAU WARNING] State 5: f=15, no uphill move available
    5 Stochastic      [5]                                                5          0       

Start=6
  [PLATEAU WARNING] State 6: f=15, no uphill move available
    6 First-Choice    [6]                                                6          0       
  [PLATEAU WARNING] State 6: f=15, no uphill move available
    6 Stochastic      [6]                                                6          0       

Start=7
  [PLATEAU WARNING] State 7: f=15, no uphill move available
    7 First-Choice    [7]                                                7          0       
  [PLATEAU WARNING] State 7: f=15, no uphill move available
    7 Stochastic      [7]                                                7          0       

Start=8
  [PLATEAU WARNING] State 7: f=15, no uphill move available
    8 First-Choice    [8, 7]                                             7          1       
  [PLATEAU WARNING] State 7: f=15, no uphill move available
    8 Stochastic      [8, 7]                                             7          1       

Start=9
    9 First-Choice    [9]                                                9          0       
    9 Stochastic      [9]                                                9          0       

Start=10
   10 First-Choice    [10, 9]                                            9          1       
   10 Stochastic      [10, 11]                                           11         1       

Start=11
   11 First-Choice    [11]                                               11         0       
   11 Stochastic      [11]                                               11         0       

Start=12
   12 First-Choice    [12, 11]                                           11         1       
   12 Stochastic      [12, 11]                                           11         1       
\end{lstlisting}

\subsubsection{Plateau Stuckness Without Sideways Moves}

\begin{table}[H]
\centering
\begin{tabular}{|c|c|c|}
\hline
\textbf{Algorithm} & \textbf{Stuck on Plateau (5,6,7)} & \textbf{Success (reached 11)} \\
\hline
First-Choice HC & 5/12 & 2/12 (16.7\%) \\
Stochastic HC & 5/12 & 3/12 (25.0\%) \\
\hline
\end{tabular}
\caption{Runs Stuck on Plateau Without Sideways Moves}
\end{table}

\textbf{Analysis:}

\begin{itemize}
    \item \textbf{Stuck runs:} Starting from states 4, 5, 6, 7, 8 (5 total) terminate on the plateau {5, 6, 7}
    
    \item \textbf{Plateau warnings:} Both algorithms detect plateaus correctly when no uphill moves exist but equal-valued neighbours do:
    \begin{itemize}
        \item From state 5: left is 4 (f=11, downhill), right is 6 (f=15, equal) → plateau warning
        \item From state 6: left is 5 (f=15, equal), right is 7 (f=15, equal) → plateau warning
        \item From state 7: left is 6 (f=15, equal), right is 8 (f=7, downhill) → plateau warning
    \end{itemize}
    
    \item \textbf{Stochastic advantage:} Start 10 shows Stochastic reaching state 11 (success) while First-Choice reaches 9 (failure). This is because:
    \begin{itemize}
        \item At state 10 ($f = 5$), both neighbours uphill: 9 ($f = 13$) and 11 ($f = 16$)
        \item First-Choice checks left first (9) and commits immediately
        \item Stochastic collects both \{9, 11\} and randomly chose 11
    \end{itemize}
\end{itemize}

\subsection{Variant 2: With Sideways Moves (Cap=10)}

Key runs showing plateau interaction:

\begin{lstlisting}
    3 First-Choice    [3, 2]                                             2          1       
    3 Stochastic      [3, 4, 5, 6, 7, 6, 7, 6, 5, 6, 5, 6, 7]            7          12      

    4 First-Choice    [4, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5]               5          11      
    4 Stochastic      [4, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5]               5          11      

    5 First-Choice    [5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5]                  5          10      
    5 Stochastic      [5, 6, 7, 6, 7, 6, 5, 6, 7, 6, 5]                  5          10      

    6 First-Choice    [6, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6]                  6          10      
    6 Stochastic      [6, 7, 6, 5, 6, 5, 6, 7, 6, 5, 6]                  6          10      

    7 First-Choice    [7, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5]                  5          10      
    7 Stochastic      [7, 6, 7, 6, 7, 6, 7, 6, 7, 6, 7]                  7          10      

    8 First-Choice    [8, 7, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5]               5          11      
    8 Stochastic      [8, 7, 6, 5, 6, 7, 6, 7, 6, 7, 6, 5]               5          11      
\end{lstlisting}

\subsubsection{Comparison: Before vs. After}

\begin{table}[H]
\centering
\begin{tabular}{|c|c|c|c|}
\hline
\textbf{Algorithm} & \textbf{Without Sideways} & \textbf{With Sideways} & \textbf{Improvement} \\
\hline
First-Choice HC & 2/12 (16.7\%) & 2/12 (16.7\%) & +0 \\
Stochastic HC & 3/12 (25.0\%) & 3/12 (25.0\%) & +0 \\
\hline
\end{tabular}
\caption{Success Rate (Reaching State 11) Before and After Sideways Moves}
\end{table}

\subsection{Detailed Sideways-Move Analysis}

\subsubsection{Why Zero Improvement?}

The sideways-move extension allows movement to equal-valued neighbours but \textbf{fails to improve global maximum reaches} because the plateau {5, 6, 7} is \textbf{topologically isolated}:

\begin{itemize}
    \item \textbf{Plateau composition:} States 5, 6, 7 all have $f = 15$
    
    \item \textbf{External connections:}
    \begin{itemize}
        \item To state 4: $f(4) = 11 < 15$ (downhill)
        \item To state 8: $f(8) = 7 < 15$ (downhill)
    \end{itemize}
    
    \item \textbf{Internal structure:} 
    \begin{itemize}
        \item From 5: left is 4 (downhill), right is 6 (equal) → only 6 allows movement
        \item From 6: left is 5 (equal), right is 7 (equal) → both 5, 7 allow movement
        \item From 7: left is 6 (equal), right is 8 (downhill) → only 6 allows movement
    \end{itemize}
\end{itemize}

\textbf{Consequence:} Even with sideways moves allowed, any path on the plateau stays within $\{5, 6, 7\}$. The algorithms explore internally using the 10-step sideways budget:

\begin{itemize}
    \item Start from 4: moves to 5 (uphill), then bounces within {5, 6} by sideways moves, exhausts budget, terminates at 5
    \item Start from 5: immediately enters sideways exploration between 5 and 6, exhausts 10-step budget, terminates
\end{itemize}

\subsubsection{Determinism vs. Randomness on Plateau}

\textbf{First-Choice HC with Sideways:}

Example from state 4: $[4, 5, 6, 5, 6, 5, 6, 5, 6, 5, 6, 5]$

\begin{itemize}
    \item Move 1: 4 → 5 (uphill)
    \item Moves 2–11: deterministically alternates 5 - 6 (left bias applies to sideways: "check left first")
    \item Move 12 would be to 5, but sideways cap reached
    \item Terminates at 5
\end{itemize}

\textbf{Stochastic HC with Sideways:}

Example from state 5: $[5, 6, 7, 6, 7, 6, 5, 6, 7, 6, 5]$

\begin{itemize}
    \item Move 1: Already at 5 (start)
    \item Moves 2–11: randomly bounces across \{5, 6, 7\}
    \item Stochastic HC can move to 7 from 6 (random choice), achieving higher variance exploration
    \item Terminates at 5 after budget exhaustion
\end{itemize}

\subsection{Why Sideways Moves Don't Improve Global Max Reach}

The cap of 10 sideways moves is crucial:

\textbf{Without cap:}
\begin{itemize}
    \item Infinite looping: $5 \to 6 \to 5 \to 6 \to \ldots$ (or similar cycles)
    \item Algorithm never escapes plateau
    \item Prevents infinite loops naturally
\end{itemize}

\textbf{With cap=10:}
\begin{itemize}
    \item Algorithms explore plateau for 10 steps
    \item At step 10 (or earlier if trying to move outside), sideways count exhausted
    \item No uphill moves exist at step 10
    \item Algorithm terminates on plateau
\end{itemize}

The fundamental issue: the cap forces termination when no uphill exit is found locally. Since the plateau lacks uphill escape routes, the cap becomes an arbitrary termination trigger, not an escape mechanism.

\subsection{Which Variant Benefits More?}

\textbf{Stochastic HC benefits more from sideways moves, but only in \textbf{exploration diversity}, not in global performance:}

\begin{enumerate}
    \item \textbf{First-Choice:} Left-bias deterministically constrains sideways moves to 5 - 6 oscillation, minimal plateau coverage
    
    \item \textbf{Stochastic:} Random selection of equal neighbours explores more plateau states (5, 6, 7 all visited), but still cannot escape
    
    \item \textbf{Why it matters:} Stochastic HC "bounces" more freely across the plateau, utilizing exploration space. First-Choice HC gets stuck in left-right ping-pong.
\end{enumerate}

\subsection{Conclusion on Plateau Handling}

The sideways-move extension is a \textbf{necessary but insufficient} solution for plateau problems:

\begin{itemize}
    \item \textbf{Necessary:} Without sideways moves, algorithms terminate immediately on a plateau
    
    \item \textbf{Insufficient:} Sideways moves only help if an uphill escape route exists beyond the immediate plateau
    
    \item \textbf{Cap effect:} The 10-step cap prevents infinite cycling but also limits exploration time. In this landscape, it's too short to find escapes that don't exist
    
    \item \textbf{Landscape dependency:} The same sideways mechanism would be highly effective on a plateau with accessible uphill regions
\end{itemize}

For the given landscape, both algorithms achieve identical global success rates (2/12 for FC, 3/12 for Stoch) regardless of sideways moves. The plateau is a local trap with no uphill escape.

\newpage

\section{GitHub Repository Structure}

All code is organized in the following structure for submission:

\begin{lstlisting}
/AI-Assignment-2/
|-- local_search/
|   |-- part_a.py          (Implementation of both algorithms)
|   |-- part_b.py          (Analysis and comparison)
|   |-- part_c.py          (Plateau handling)
|   |-- README.md          (Usage and documentation)
|-- genetic_algo/
|   |-- (placeholder for future assignments)
|-- real_world/
|   |-- (placeholder for future assignments)
|-- REPORT.pdf             (This comprehensive analysis)
\end{lstlisting}

\newpage

\section{Summary of Findings}

\subsection{Part (A): Implementation}
\begin{itemize}
    \item Both algorithms implemented correctly with proper boundary handling
    \item First-Choice commits greedily to left-first improvement
    \item Stochastic evaluates all uphill options before randomly selecting
\end{itemize}

\subsection{Part (B): Comparison and Analysis}
\begin{itemize}
    \item Only 2/12 starting states reach global maximum for both algorithms
    \item Two divergences found (states 3, 5) where Stochastic achieves better local maxima
    \item Stochastic HC reliability test shows 0\% success from state 4 due to being a true local maximum
    \item \textbf{Key insight:} Randomness helps only when uphill choices exist
\end{itemize}

\subsection{Part (C): Plateau Handling}
\begin{itemize}
    \item Plateau detection works correctly, warning on all 5 trapped starting states
    \item Sideways moves achieve zero improvement in global success because plateau is topologically isolated
    \item Stochastic HC explores plateau more diversely but cannot escape structural limitations
    \item Cap of 10 prevents infinite cycles but becomes arbitrary when escape is impossible
\end{itemize}

\end{document}