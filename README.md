## Problem 1: EA for N-Queens Problem - EA_N_Queens.py 

This program first generates the initial population of random solutions. Each individual 
is a list of size N, where each entry represents a queen placed in a random row in a 
specific column. This process is repeated population_size times to create diverse 
individuals that will evolve. 

a) Fitness Function: This function calculates the number of attacking queen pairs for a 
given individual solution. It compares every pair of queens to check if they share the 
same column or diagonal and increments the attack count for each such pair. The 
fewer the attacks, the better the fitness. 

b) Fitness of the Population: This function applies the fitness function to each 
individual in the population. It returns a list of fitness scores, allowing the algorithm 
to evaluate which individuals have fewer attacking queens and are better 
candidates for reproduction. 

c) Crossover Function: This function takes two parent solutions and produces two 
children by swapping segments between the parents. Two random crossover points 
are chosen, and the middle portion between those points is exchanged, combining 
traits from both parents in the child. 

d) Mutation Function: This function introduces variation into a solution by randomly 
swapping the positions of two queens with a certain probability. 

e) Selection Function: This function performs tournament selection, where small 
groups of individuals compete, and the one with the best fitness is chosen. 

f) Evolution Loop: In each generation, new children are created by crossover and 
mutation. The current population is combined with the children, and the best 
solutions are selected for the next generation. This process continues until an 
optimal solution is found or the maximum number of generations is reached. 

At the end of the evolution process, the best individual in the population is identified 
based on their fitness. If an optimal solution (with zero attacking queens) is found, the 
algorithm outputs this solution as the final result. 

![image](https://github.com/user-attachments/assets/8d61d591-39eb-4c1a-a7a9-92f3592f6d56)

## Problem 2: EA for TSP – EA_TSP.py & EA_TSP_for_large_data.py 

a) Fitness Function: This function calculates the total distance of a given tour. It 
iterates through each city in the tour, calculating the Euclidean distance between 
consecutive cities, including the return to the starting city. The sum of these 
distances is returned as the tour’s fitness value, where lower values represent 
shorter distances and better solutions. 

b) Crossover Function: This function performs ordered crossover between two parent 
tours. Two random points are chosen to define a segment, and this segment is 
copied from each parent to the respective child. The remaining positions in each 
child are filled with cities from the other parent while maintaining the original order, 
ensuring no city is repeated. 

c) Mutation Function: The mutation function introduces random changes in the tour 
with a given probability. If mutation occurs, it swaps the positions of two randomly 
selected cities in the tour. 

d) Validate Tour Function: This function ensures that the tour generated is valid by 
checking if all positions in the tour contain valid city indices (i.e., no None values). 

e) Selection Function: In function a small group of individuals from the population is 
randomly selected, and the one with the best fitness (shortest distance) is chosen 
to continue to the next generation. 

f) Plot Tour Function: This function visualizes a given tour by plotting it on a graph, 
where the cities are represented as points, and the tour as a path connecting them. 
It saves the resulting plot as an image. 

g) Evolution Process: The evolutionary loop generates new children using crossover 
and mutation. It combines the current population with the new children and then 
applies selection to retain the best individuals for the next generation. This process 
is repeated for a fixed number of generations or until an optimal solution is found.

EA_TSP.py (N=10) 

In the program, cities are generated randomly using the NumPy function 
np.random.randint(0, 100, size=(N, 2)). This creates an array of N cities, where each city 
has two coordinates (x, y), representing its location on a 2D plane. The x and y values are 
integers between 0 and 100, simulating the random placement of cities within a 100x100 
grid. These coordinates are then used to calculate distances between cities during the 
evolution process. 

![image](https://github.com/user-attachments/assets/da9afb14-6cff-49c7-b7f6-81c11c482716)

![image](https://github.com/user-attachments/assets/43acd411-a2db-43cc-95ce-62fcd18776b6)

![image](https://github.com/user-attachments/assets/fe975699-3362-4189-8db3-122202c8e84d)

![image](https://github.com/user-attachments/assets/3f6af854-43bb-46f0-83f9-1d88d50a369c)

EA_TSP_for_large_data.py 

The input to this program comes from a .tsp file, which contains a list of city coordinates for 
solving the Traveling Salesman Problem (TSP). The read_tsp_file function parses the file by 
looking for the section marked NODE_COORD_SECTION, which signifies the start of the 
city data. Each line after this section contains the index of the city followed by its x and y 
coordinates. The function reads these coordinates until it reaches the EOF marker, and 
stores them as a list of city coordinates. These coordinates are then converted into a 
NumPy array, where each city has a pair of floating-point numbers representing its x and y 
positions on a 2D plane. The total number of cities is determined by the length of this array, 
which in the case of the provided example (xqf131.tsp), would typically contain 131 cities. 
This data serves as the input for the genetic algorithm to calculate the optimal tour. 

OUTPUT: Output of the EA_TSP_for_large_data.py program is copied in 
EA_TSP_for_large_data_OUTPUT.txt. I have ran the program for 500 iterations as its taking 
time for finding the solution.

![image](https://github.com/user-attachments/assets/8bc9a9de-f4b9-48b9-a09d-5c987542c43c)


## Problem 3: Ant Colony Optimization for TSP – Ant_Colony_Optimization_TSP.py 

a) calculate_cost(path, distance_matrix): This function calculates the total distance 
(cost) of a given path based on the provided distance matrix. It iterates over each 
city in the path, summing up the distances between consecutive cities and the final 
city back to the first one, ensuring the tour is complete. The result is the total cost of 
traveling through the cities in the specified order. 

b) select_next_city(current_city, visited): This function selects the next city to visit 
using a probabilistic approach based on pheromone levels and visibility (inverse of 
distance). For each unvisited city, the probability is computed as a function of 
pheromone strength and visibility raised to their respective powers. After 
normalizing the probabilities, the next city is chosen using stochastic sampling. If no 
valid probabilities are left, a random unvisited city is selected.

c) two_opt_mutation(path, distance_matrix): This function applies the 2-opt mutation, 
a local search algorithm, to improve the current path. It generates new paths by 
reversing sections of the current path and compares their costs. If a new path has a 
lower cost, it replaces the current path. The function returns the best path found 
after evaluating all possible 2-opt swaps. 

d) find_path(start): Starting from a given city, this function builds a complete path for 
an ant. It iteratively selects the next city to visit using the select_next_city function 
until all cities are visited. The cities are stored in the path list, and a set visited keeps 
track of cities already included in the path. 

The main loop runs the Ant Colony Optimization (ACO) for a specified number of 
iterations. For each ant, it finds a path, applies 2-opt mutation, and calculates the cost. 
If the ant's path is the best found so far, it's saved as the global best. Each ant 
contributes to updating the pheromone matrix based on the quality (cost) of its path. 
After every iteration, pheromone evaporation occurs, and the pheromone matrix is 
updated. The process continues until the algorithm converges or reaches the maximum 
number of iterations.

![image](https://github.com/user-attachments/assets/79252177-ba5f-4461-a4ae-2db20f7dd5eb)

![image](https://github.com/user-attachments/assets/b69d5547-6724-4c7e-88e4-def1fc0e6044)

![image](https://github.com/user-attachments/assets/4931637d-4f36-4199-b0ba-4f67eab23fe3)





