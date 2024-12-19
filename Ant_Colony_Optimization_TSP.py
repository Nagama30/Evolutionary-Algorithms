import numpy as np

# Fix the random seed
np.random.seed(1234567)

# Constants for ACO
nAnt = 20  # Number of ants
n = 10  # Number of cities
Iteration = 100
initial_pheromone = 0.01  # Initial pheromone level
anfa = 1.0  # Pheromone influence
beta = 2.0  # Visibility (distance) influence
P = 0.6  # Evaporation coefficient
Q = 0.1  # Pheromone deposited per ant

# Distance matrix 
np.random.seed(0)
distances = np.random.randint(10, 100, size=(n, n))
distances = (distances + distances.T) / 2  # Symmetrize the matrix
#print(distances)
# Initialize pheromones
pheromones = np.full((n, n), initial_pheromone)
#print(pheromones)
# Fitness (cost) calculation
def calculate_cost(path, distance_matrix):
    cost = 0
    for i in range(len(path)):
        cost += distance_matrix[path[i]][path[(i + 1) % len(path)]]
    return cost

# Visibility (inverse distance)
visibility = 1 / (distances + 1e-10)  # Avoid division by zero

# Stochastic selection of next city based on probability
def select_next_city(current_city, visited):
    probabilities = []
    for next_city in range(n):
        if next_city not in visited:
            prob = (pheromones[current_city][next_city] ** anfa) * (visibility[current_city][next_city] ** beta)
            probabilities.append(prob)
        else:
            probabilities.append(0)
    
    probabilities = np.array(probabilities)
    if np.sum(probabilities) == 0:
        return np.random.choice([city for city in range(n) if city not in visited])
    
    probabilities /= np.sum(probabilities)
    
    next_city = np.random.choice(range(n), p=probabilities)
    return next_city

# 2-opt mutation to improve path locally
def two_opt_mutation(path, distance_matrix):
    best_path = path.copy()
    best_cost = calculate_cost(path, distance_matrix)
    for i in range(1, len(path) - 1):
        for j in range(i + 1, len(path)):
            if j - i == 1:
                continue  # Consecutive nodes are not swapped
            new_path = path[:i] + path[i:j][::-1] + path[j:]
            new_cost = calculate_cost(new_path, distance_matrix)
            if new_cost < best_cost:
                best_path = new_path
                best_cost = new_cost
    return best_path

# Find the path for each ant
def find_path(start):
    path = [start]
    visited = set(path)
    while len(path) < n:
        next_city = select_next_city(path[-1], visited)
        path.append(next_city)
        visited.add(next_city)
    return path

# Ant Colony Optimization
best_path = None
best_cost = float('inf')

for it in range(Iteration):
    delta_pheromones = np.zeros_like(pheromones)  # Delta for pheromone updates
    
    for _ in range(nAnt):
        # Start from a random city
        start_city = np.random.randint(n)
        path = find_path(start_city)
        path = two_opt_mutation(path, distances)  # Apply 2-opt mutation
        cost = calculate_cost(path, distances)
        
        # Update the best solution
        if cost < best_cost:
            best_path = path.copy()
            best_cost = cost
        
        # Pheromone update contribution by this ant
        for i in range(n):
            delta_pheromones[path[i]][path[(i + 1) % n]] += Q / cost
    
    # Pheromone evaporation and update
    pheromones = P * pheromones + delta_pheromones
    
    print(f"Generation {it + 1}: Best fitness = {best_cost}")

# Output best result
print("Best path found:", best_path)
print("Best path cost:", best_cost)
