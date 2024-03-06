import numpy as np
import random
from visualization import *
from container import PartiallyLoadedContainer, find_best_position, load_box
from package import *

# import all local files
# The container has a depth, a width and a height. The container is partially loaded with cargo (box shaped items).
# The cargo is loaded in the container in a matrix of cells. Each cell has a height.
# In debug mode, the process of loading is documented with print statements on the console
# test_load_box()


def print_population(population):
    for solution in population:
        print("solution start")
        for item in solution:
            print(item)
        print("solution of group")


def get_group_ids(group):
    ids = []
    for package in group:
        ids.append(package.id_item)
    return ids


# Initialize population with random permutations
def initialize_population(population_size, packages):
    population = []
    for _ in range(population_size):
        solution = {}
        grouped_packages = {}
        for package in packages:
            if package.group_id not in grouped_packages:
                grouped_packages[package.group_id] = []
            grouped_packages[package.group_id].append(package.item_id)
        for group_id, group_packages in grouped_packages.items():
            random.shuffle(group_packages)
            solution[group_id] = group_packages
        population.append(solution)
    return population


def calculate_fitness_3DContainerLoader(population, packages, cheight, cdepth, cwidth):
    fitness_scores = []

    for chromosome in population:
        # make a list of items to be loaded in the container by putting packages in the order of the chromosome
        items_to_be_loaded = []
        for group_id, package_ids in chromosome.items():
            for package_idx in package_ids:
                package = packages[package_idx]
                items_to_be_loaded.append(
                    (
                        package.width,
                        package.height,
                        package.depth,
                    )
                )

        # initialize the container
        container = PartiallyLoadedContainer(2, 2, [0, cdepth], [0, cwidth])
        container.height = cheight

        # load the boxes in the container
        best_score = 10000000000
        for box in items_to_be_loaded:
            depth, width, height = box
            best_row, best_column, best_score = find_best_position(
                container, depth, width, height
            )
            load_box(container, best_row, best_column, depth, width, height)
        # calculate the fitness score
        fitness_scores.append(container.depth - best_score)
    return np.array(fitness_scores)


def crossover(parent1, parent2):
    child1 = {}
    child2 = {}
    for group_id in parent1.keys():
        if random.random() < 0.5:
            child1[group_id] = parent1[group_id]
            child2[group_id] = parent2[group_id]
        else:
            child1[group_id] = parent2[group_id]
            child2[group_id] = parent1[group_id]
    return child1, child2


# Perform mutation (swap two random elements)
def mutate(solution):
    mutated_solution = solution.copy()
    for group_id, group_packages in mutated_solution.items():
        if random.random() < 0.1:  # Mutation probability
            random.shuffle(group_packages)
            mutated_solution[group_id] = group_packages
    return mutated_solution


# Genetic Algorithm
def genetic_algorithm(
    packages,
    population_size,
    num_generations,
    mutation_rate,
    loading_method,
    cheight=2670,
    cdepth=13620,
    cwidth=2480,
):
    num_packages = len(packages)
    # num_groups = len(packages)
    # for i in range(num_groups):
    #    num_packages += len(packages[i])

    population = initialize_population(population_size, packages)

    for generation in range(num_generations):
        fitness_scores = []

        # set dimensions  of the container
        fitness_scores = calculate_fitness_3DContainerLoader(
            population, packages, cheight, cdepth, cwidth
        )

        # Select parents for reproduction using roulette wheel selection
        probabilities = fitness_scores / np.sum(fitness_scores)
        parent_indices = np.random.choice(
            range(population_size), size=population_size, p=probabilities
        )

        # parents = population[parent_indices]
        parents = [population[index] for index in parent_indices]

        # Create new generation
        new_population = []

        for i in range(0, population_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]

            # Perform crossover
            child1, child2 = crossover(parent1, parent2)
            # print(child1)
            # print(child2)
            # Perform mutation
            # if np.random.rand() < mutation_rate:
            child1 = mutate(child1)
            # if np.random.rand() < mutation_rate:
            child2 = mutate(child2)

            new_population.extend([child1, child2])

        population = np.array(new_population)

    # Find the best solution from the final generation
    fitness_scores = []

    # set dimensions  of the container
    fitness_scores = calculate_fitness_3DContainerLoader(
        population, packages, cheight, cdepth, cwidth
    )
    best_solution_idx = np.argmax(fitness_scores)
    best_chromosome = population[best_solution_idx]

    best_fitness = fitness_scores[best_solution_idx]

    return best_chromosome, best_fitness
