import numpy as np
import matplotlib.pyplot as plt

# Function to parse .tsp file
def read_tsp_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    start = False
    cities = []
    
    for line in lines:
        if 'NODE_COORD_SECTION' in line:
            start = True
            continue
        if 'EOF' in line:
            break
        if start:
            parts = line.split()
            if len(parts) >= 3:
                cities.append([float(parts[1]), float(parts[2])])
    
    return np.array(cities)

# Fitness function
def fitness(tour, cities):
    distance = 0
    for i in range(len(tour)):
        # Euclidean distance calculation
        city1 = np.array(cities[tour[i]])
        city2 = np.array(cities[tour[(i + 1) % len(tour)]])
        distance += np.linalg.norm(city1 - city2)
    return distance

# Crossover function (ordered crossover)
def crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(np.random.randint(0, size, 2))
    
    child1 = [None] * size
    child2 = [None] * size

    # Copy the selected segment from parent1 to child1, and from parent2 to child2
    child1[start:end] = parent1[start:end]
    child2[start:end] = parent2[start:end]

    # Fill the remaining positions in child1 with the order of genes in parent2
    p2_index = end
    for i in range(size):
        if parent2[p2_index % size] not in child1:
            child1[i % size] = parent2[p2_index % size]
            p2_index += 1
    
    # Fill the remaining positions in child2 with the order of genes in parent1
    p1_index = end
    for i in range(size):
        if parent1[p1_index % size] not in child2:
            child2[i % size] = parent1[p1_index % size]
            p1_index += 1

    return child1, child2

# Mutation function
def mutation(tour, prob=0.1):
    if np.random.rand() < prob:
        idx1 = np.random.randint(0, len(tour))  
        idx2 = np.random.randint(0, len(tour))
        tour[idx1], tour[idx2] = tour[idx2], tour[idx1]
    return tour

# Validate tour to ensure no None values
def validate_tour(tour):
    return all(isinstance(x, int) and x is not None for x in tour)

# Selection function
def selection(population, cities, n):
    selected = []
    for _ in range(n):
        competitors = np.random.randint(0, len(population), 5)
        winner = min(competitors, key=lambda i: fitness(population[i], cities))
        selected.append(population[winner])
    return selected

# Plot the tour and save it as an image
def plot_tour(tour, cities, filename='tour_plot.png'):
    if None in tour:
        print("Invalid tour: contains None values", tour)
        return

    tour_coords = [cities[i] for i in tour] + [cities[tour[0]]]  
    xs, ys = zip(*tour_coords)
    plt.figure()
    plt.plot(xs, ys, 'o-', markersize=8)
    plt.title(f"Tour Plot for {len(cities)} Cities")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.savefig(filename)
    plt.close()
    print(f"Tour plot saved as {filename}")

# Read cities from a .tsp file
filename = 'xqf131.tsp'
cities = read_tsp_file(filename)
#print(f"Loaded cities: {cities}")

# Parameters
num_generations = 500
population_size = 50
mate_prob = 0.6

# Initialize population with random permutations
population = [np.random.permutation(len(cities)).tolist() for _ in range(population_size)]

# Evolution
for generation in range(num_generations):
    next_gen = []
    for i in range(len(population)):
        for j in range(i + 1, len(population)):
            if np.random.rand() < mate_prob:
                child_1, child_2 = crossover(population[i], population[j])
                # Ensure that the child tours are valid
                if validate_tour(child_1) and validate_tour(child_2):
                    next_gen.append(mutation(child_1))
                    next_gen.append(mutation(child_2))

    population += next_gen
    population = selection(population, cities, population_size)

    # Calculate fitness
    fitness_scores = [fitness(tour, cities) for tour in population]
    best_fitness = min(fitness_scores)

    print(f'Generation {generation + 1}: Best fitness = {best_fitness}')

# Return the best solution
best_solution_idx = np.argmin(fitness_scores)
best_solution = population[best_solution_idx]

# Output results
print("Best tour:", best_solution)
print("Best tour distance:", fitness(best_solution, cities))

# Plot the best solution and save it as 'tour_plot.png'
plot_tour(best_solution, cities)
