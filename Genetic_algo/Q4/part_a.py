import random

# this will convert binary string to inetger val
def decode(chromosome):
    x = int(''.join(map(str, chromosome)), 2)  
    return x

# firness function as defined in ques
def fitness(chromosome):
    x = decode(chromosome)
    return -x**2 + 14*x + 5

# this will sleect one from population acc to fitness proportionate
def roulette_select(population):
    #total fitness of the population
    total_fitness = sum(fitness(individual) for individual in population)
    # Spin the roulette wheel
    spin = random.random() * total_fitness
    cumulative_fitness = 0
    for individual in population:
        cumulative_fitness += fitness(individual)
        if cumulative_fitness >= spin:
            return individual

# this is sgnle point crossover that will combine 2 parents at poiunt
def single_point_crossover(parent1, parent2, point):
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2

#mutation to flip random bit
def mutate(chromosome, p_m):
    return [bit if random.random() > p_m else 1 - bit for bit in chromosome]

# Main Genetic Algorithm loop
def genetic_algorithm(population_size=10, num_generations=100, mutation_prob=0.1):
    # Generate an initial random population of 4-bit binary chromosomes
    population = [random.choices([0, 1], k=4) for _ in range(population_size)]    
    for generation in range(num_generations):
        # Select two parents using roulette wheel selection
        parent1 = roulette_select(population)
        parent2 = roulette_select(population)
        # Perform single-point crossover to create offspring
        point = random.randint(1, 3)  # Crossover at a random point
        offspring1, offspring2 = single_point_crossover(parent1, parent2, point)
        # Apply mutation to the offspring
        offspring1 = mutate(offspring1, mutation_prob)
        offspring2 = mutate(offspring2, mutation_prob)
        # Evaluate the fitness of the offspring and add them to the population
        population.append(offspring1)
        population.append(offspring2)
        # Sort the population by fitness in descending order and keep the best individuals
        population = sorted(population, key=lambda x: fitness(x), reverse=True)[:population_size]
        # Print the best solution of this generation
        best_individual = population[0]
        print(f"Generation {generation}: Best Solution = {best_individual}, Fitness = {fitness(best_individual)}")
    # Return the best solution found
    return population[0]

# Test the GA with the given chromosomes
def test_functions():
    chromosomes = [
        [0, 1, 1, 0],  # x = 6
        [1, 0, 0, 1],  # x = 9
        [1, 1, 0, 0],  # x = 12
        [0, 0, 1, 1]   # x = 3
    ]

    print("Testing Decode and Fitness for Chromosomes:")
    for chrom in chromosomes:
        decoded_value = decode(chrom)
        fitness_value = fitness(chrom)
        print(f"Chromosome: {chrom} => Decoded value: {decoded_value}, Fitness: {fitness_value}")
            

best_solution = genetic_algorithm(population_size=10, num_generations=100, mutation_prob=0.1)
print("\nBest Solution Found:")
print(f"Chromosome: {best_solution}, Decoded Value: {decode(best_solution)}, Fitness: {fitness(best_solution)}")

test_functions()
