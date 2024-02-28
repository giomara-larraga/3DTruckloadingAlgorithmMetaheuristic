# Description: This file contains the main function to run the genetic algorithm to solve the 3D truck loading problem
from genetic_algorithm import *
from visualization import *
from container import *
from package import *
from box3dvisualizer import *

import plotly.graph_objects as go

def main():
    # Genetic Algorithm Parameters
    POPULATION_SIZE = 50
    NUM_GENERATIONS = 1000
    MUTATION_RATE = 0.2

    # draw a ASCII Graphics rectangle as a comment with depth, width, height
    # -------------------------  ---
    # |                       |
    # |                       |  width
    # |                       |
    # -------------------------
    # |<----    depth    ---->|  ---

    # Initialize the container
    container_height = 2670
    container_width = 2480
    container_depth = 13620

    # List of box dimensions format (depth, width, height)
    deli1_boxes = [(660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203),
                   (660, 940, 1203),
                   (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190),
                   (660, 940, 1398), (660, 940, 1398), (660, 940, 1398), (660, 940, 1398),
                   (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248),
                   (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248)]
    # Color mapping for visualization
    tieto_deli_colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'green',
                         'green', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
                         'yellow', 'yellow', 'yellow', 'orange', 'orange']

    #Create a dictionary of colors
    colors = {'red': (255, 0, 0), 'blue': (0, 0, 255), 'green': (0, 255, 0), 'yellow': (255, 255, 0), 'orange': (255, 165, 0)}
    # all unmatched colors will be grey'
    colors = {**colors, **{'grey': (128, 128, 128)}}

    # Here ends the specification of the boxes and the colors


    #Translate the colors tieto_deli_colors to a list of RGB tuples using the dictionary
    tieto_deli_colors_tuples = [colors[color] for color in tieto_deli_colors]

    # Create packages from the list of box dimensions
    packages = []
    for box in deli1_boxes:
        depth, width, height = box
        packages.append(Package(depth, width, height, False))

    # Run the genetic algorithm
    best_chromosome, best_fitness = genetic_algorithm(packages, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE, '3D')

    # Print the best loading order
    print("Best Loading Order:", best_chromosome, "Fitness:", best_fitness)



    # Translate the best chromosome into a list of items to be loaded in the container
    items_to_be_loaded = []
    color_package = []
    for i, package_idx in enumerate(best_chromosome):
        package = packages[package_idx]
        color_package.append(tieto_deli_colors[package_idx])
        items_to_be_loaded.append((package.width, package.height, package.depth))


    container = PartiallyLoadedContainer(2, 2, [0, container_depth], [0, container_width])
    container.height = container_height

    # Load the boxes in the container
    for box in items_to_be_loaded:
        depth, width, height = box
        best_row, best_column, best_score = find_best_position(container, depth, width, height)
        load_box(container, best_row, best_column, depth, width, height)

    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()

    # Output the lower and upper corners and the index of the boxes loaded in the container
    #print('Boxes loaded in the container:')
    #print('Index, Lower Corner, Upper Corner')
    #for i in range(len(container.boxes)):
    #    print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])
    #    print(color_package)

    # Make a list of boxes in JSON format
    # Assign same colors to same size boxes
    boxes_json = print_json_for_list_of_boxes(container.boxes_index, color_package, container.boxes,
                                               container.boxes_lower_corner, cdepth=container_depth + 1, cwidth=container_width + 1,
                                               cheight=container_height + 1)
    print(boxes_json)

    #test_draw_box()
    visualize3Dboxes(container.boxes_lower_corner, container.boxes,
                     container.width, container.depth, container.height, tieto_deli_colors_tuples)


if __name__ == "__main__":
    main()
