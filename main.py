# Runnin
from genetic_algorithm import *
from visualization import *
from container import *
from package import *


def main():
    # Genetic Algorithm Parameters
    POPULATION_SIZE = 50
    NUM_GENERATIONS = 100
    MUTATION_RATE = 0.2

    # Problem-specific parameters
    CONTAINER_WIDTH = 10
    CONTAINER_HEIGHT = 10
    CONTAINER_DEPTH = 10

    # List of box dimensions
    deli1_boxes = [(660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203),
                   (660, 940, 1203),
                   (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190),
                   (660, 940, 1398), (660, 940, 1398), (660, 940, 1398), (660, 940, 1398),
                   (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248),
                   (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248)]

    # Create packages from the list of box dimensions
    packages = []
    for box in deli1_boxes:
        depth, width, height = box
        packages.append(Package(depth, width, height, False))

    # Run the genetic algorithm
    best_chromosome, best_fitness = genetic_algorithm(packages, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE, '3D')

    # Print the best loading order
    print("Best Loading Order:", best_chromosome, "Fitness:", best_fitness)

    # Color mapping for visualization
    tieto_deli_colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'green',
                         'green', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
                         'yellow', 'yellow', 'yellow', 'orange', 'orange']

    # Translate the best chromosome into a list of items to be loaded in the container
    items_to_be_loaded = []
    color_package = []
    for i, package_idx in enumerate(best_chromosome):
        package = packages[package_idx]
        color_package.append(tieto_deli_colors[package_idx])
        items_to_be_loaded.append((package.width, package.height, package.depth))

    # Initialize the container
    container = PartiallyLoadedContainer(2, 2, [0, 13620], [0, 2480])
    container.height = 2670

    # Load the boxes in the container
    for box in items_to_be_loaded:
        depth, width, height = box
        best_row, best_column, best_score = find_best_position(container, depth, width, height)
        load_box(container, best_row, best_column, depth, width, height)

    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()

    # Output the lower and upper corners and the index of the boxes loaded in the container
    print('Boxes loaded in the container:')
    print('Index, Lower Corner, Upper Corner')
    for i in range(len(container.boxes)):
        print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])
        print(color_package)

    # Make a list of boxes in JSON format
    # Assign same colors to same size boxes
    boxes_json = print_json_for_list_of_boxes(container.boxes_index, color_package, container.boxes,
                                               container.boxes_lower_corner, cdepth=13620 + 1, cwidth=2480 + 1,
                                               cheight=2670 + 1)
    print(boxes_json)

if __name__ == "__main__":
    main()
