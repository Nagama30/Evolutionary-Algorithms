import numpy as np

# Fix the random seed
np.random.seed(1234567)

# N for the N-Queens problem
N = 8

# Population size
population_size = 100

# Initialize the population
pop = []
for i in range(population_size):
	ind = []
	for j in range(N):
		ind.append(np.random.randint(N))
	pop.append(ind)
#pop = [np.random.permutation(N) for _ in range(population_size)]
    
print("Initial population:", pop) 

# Fitness function to count the number of attacking pairs of queens
def fitness(individual):
    attacks = 0
    for i in range(N):
        for j in range(i + 1, N):
            # Check for same column or diagonal attack
            if individual[i] == individual[j] or abs(individual[i] - individual[j]) == j - i:
                attacks += 1
    return attacks

# Calculate fitness for the population
def fitness_pop(pop):
    return [fitness(ind) for ind in pop]

# Crossover function 
def crossover(parent1, parent2):
    size = len(parent1)
    point1, point2 = sorted(np.random.choice(range(1, size - 1), 2, replace=False))  # Two crossover points
    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    return child1, child2

# Mutation function 
def mutation(individual, prob = 0.1):
    if np.random.rand() < prob:
        idx1, idx2 = np.random.randint(0, N, 2)
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# Selection function
def selection(pop, n):
    selected = []
    for _ in range(n):
        competitors = np.random.choice(len(pop), 5, replace=False)
        winner = min(competitors, key=lambda i: fitness(pop[i]))  # Select the one with best fitness
        selected.append(pop[winner])
    return selected

# Evolution
num_iters = 100
mate_prob = 0.6

for generation in range(num_iters):
    next_gen = []
    for i in range(len(pop)):
        for j in range(i + 1, len(pop)):  # Make sure you're not re-pairing the same individual
            if np.random.rand() < mate_prob:
                # Perform crossover
                child_1, child_2 = crossover(pop[i], pop[j])
                # Mutate the children
                next_gen.append(mutation(child_1))
                next_gen.append(mutation(child_2))
    
    # Combine current population with the new offspring
    combined_pop = pop + next_gen
    
    # Apply selection to the combined population
    pop = selection(combined_pop, population_size)  
    
        # Calculate the best fitness for the current generation
    fitness_scores = fitness_pop(pop)  # Calculate fitness for the population
    best_fitness = min(fitness_scores)  # Get the best fitness
    
    print(f'Generation {generation + 1}: Best fitness = {best_fitness}')
    
    # Stop if an optimal solution is found
    if best_fitness == 0:
        print("Optimal solution found.")
        break

# Final best solution
best_solution = pop[min(range(len(pop)), key=lambda i: fitness(pop[i]))]
print("Best solution:", best_solution)