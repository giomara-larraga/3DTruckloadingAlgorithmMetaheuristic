import numpy as np


# Define a data structure for each package
class Package:
    def __init__(self, width, height, depth, non_stackable):
        self.width = width
        self.height = height
        self.depth = depth
        self.non_stackable = non_stackable
        self.x = 0  # Initialize x position
        self.y = 0  # Initialize y position
        self.z = 0  # Initialize z position


# Genetic Algorithm Parameters
POPULATION_SIZE = 50
NUM_GENERATIONS = 100
MUTATION_RATE = 0.2

# Problem-specific parameters
CONTAINER_WIDTH = 10
CONTAINER_HEIGHT = 10
CONTAINER_DEPTH = 10

# Create a list of packages (for example)
packages = [
    Package(2, 3, 1, False),
    Package(4, 2, 1, True),
    Package(3, 3, 1, False),
    Package(1, 4, 1, False),
    Package(5, 2, 1, True),
    # Add more packages as needed
]


# Initialize population with random permutations
def initialize_population(population_size, num_packages):
    return np.array(
        [np.random.permutation(num_packages) for _ in range(population_size)]
    )


# Calculate fitness of each chromosome
def calculate_fitness(population, packages):
    fitness_scores = []

    for chromosome in population:
        # Reset package positions
        for package in packages:
            package.x = 0
            package.y = 0
            package.z = 0

        total_wasted_space = 0
        non_stackable_stacked_penalty = 0

        for i, package_idx in enumerate(chromosome):
            package = packages[package_idx]

            # Calculate position in container
            if i == 0:
                package.x, package.y, package.z = 0, 0, 0
            else:
                package.x = (
                    packages[chromosome[i - 1]].x + packages[chromosome[i - 1]].width
                )
                package.y = packages[chromosome[i - 1]].y
                package.z = packages[chromosome[i - 1]].z

                # Check if package fits in container
                if package.x + package.width > CONTAINER_WIDTH:
                    package.x = 0
                    package.y += max([packages[chromosome[j]].height for j in range(i)])

                if package.y + package.height > CONTAINER_HEIGHT:
                    package.y = 0
                    package.z += max([packages[chromosome[j]].depth for j in range(i)])

                if package.z + package.depth > CONTAINER_DEPTH:
                    total_wasted_space += 1  # Penalize for not fitting in container

                # Check if non-stackable item is stacked
                if package.non_stackable and any(
                    packages[j].z + packages[j].depth > package.z for j in range(i)
                ):
                    non_stackable_stacked_penalty += 1

        # Apply penalty for non-stackable items being stacked
        fitness_scores.append(
            1 / (1 + total_wasted_space + non_stackable_stacked_penalty)
        )
    print(fitness_scores)
    return np.array(fitness_scores)


# Perform single-point crossover
def crossover(parent1, parent2):
    crossover_point = np.random.randint(len(parent1))
    child1 = np.hstack(
        (
            parent1[:crossover_point],
            [i for i in parent2 if i not in parent1[:crossover_point]],
        )
    )
    child2 = np.hstack(
        (
            parent2[:crossover_point],
            [i for i in parent1 if i not in parent2[:crossover_point]],
        )
    )
    return child1, child2


# Perform mutation (swap two random elements)
def mutate(chromosome):
    idx1, idx2 = np.random.choice(len(chromosome), size=2, replace=False)
    chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome


# Genetic Algorithm
def genetic_algorithm(packages, population_size, num_generations, mutation_rate):
    num_packages = len(packages)
    population = initialize_population(population_size, num_packages)

    for generation in range(num_generations):
        fitness_scores = calculate_fitness(population, packages)

        # Select parents for reproduction using roulette wheel selection
        probabilities = fitness_scores / np.sum(fitness_scores)
        parent_indices = np.random.choice(
            range(population_size), size=population_size, p=probabilities
        )
        parents = population[parent_indices]
        # Create new generation
        new_population = []

        for i in range(0, population_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]

            # Perform crossover
            child1, child2 = crossover(parent1, parent2)

            # Perform mutation
            if np.random.rand() < mutation_rate:
                child1 = mutate(child1)
            if np.random.rand() < mutation_rate:
                child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = np.array(new_population)

    # Find the best solution from the final generation
    fitness_scores = calculate_fitness(population, packages)
    best_solution_idx = np.argmax(fitness_scores)
    best_chromosome = population[best_solution_idx]
    best_fitness = fitness_scores[best_solution_idx]

    return best_chromosome, best_fitness


# Run the genetic algorithm
best_chromosome, best_fitness = genetic_algorithm(
    packages, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE
)

# Print the best loading order
print("Best Loading Order:", best_chromosome, "Fitness:", best_fitness)
