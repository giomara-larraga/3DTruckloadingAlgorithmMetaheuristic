# write a test script that evaluates if a box shaped item can be placed at the integer corner (row, column) as its lower corner
# and it is (1) well supported by the container floor or previously loaded boxes (even height level).
# (2) it does not exceed the container height and (3) it does not exceed the container depth and width.
# The function returns True if the box can be placed at the corner (row, column) and False otherwise.
# The score reflects for a feasible place how well the box fits on previously loaded boxes. A blend of loading meters, and axle balance
# Example usage:

# Running
from genetic_algorithm_grouping import *
from visualization import *
from container import *
from package import *
def test_evaluate_space_feasibility():
    container = PartiallyLoadedContainer(4, 4, [0, 10, 20, 40], [0, 10, 20, 80])

    # Set heights for specific cells (heights in the range [0, 100])
    container.set_height(0, 1, 30)
    container.set_height(1, 0, 30)
    container.set_height(1, 1, 30)
    container.set_height(1, 2, 30)
    container.set_height(0, 0, 30)

    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Print
    column, row, depth, width, height = (2, 2, 13, 19, 10)
    if (debug_load==True):
        print('Attempting to load_box(container, column:', column,' row:', row, ' depth', depth,' width:', width,' height:', height)
    feasibility, score, error_message = evaluate_space_feasibility(container, row,column, depth, width, height)
    if (debug_load==True):
        print('Feasibility: ', feasibility, 'Score: ', score, 'Error message: ', error_message)
    load_box(container, row, column,
         depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

def test_find_best_position():
    # Define a container
    container = PartiallyLoadedContainer(4, 4, [0, 10, 20, 40], [0, 10, 20, 80])
    # Initialize some heights
    container.set_height(0, 1, 30)
    container.set_height(1, 0, 30)
    container.set_height(1, 1, 30)
    container.set_height(1, 2, 30)
    container.set_height(0, 0, 30)

    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")
    # Find the best position for a box shaped item with a specific depth and height.

    depth, width, height = (13, 19, 10)
    print('Attempting to find_best_position(container, depth:', depth,' width:', width,' height:', height)
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    depth, width, height = (13, 19, 70)
    print('Attempting to find_best_position(container, depth:', depth,' width:', width,' height:', height)
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    depth, width, height = (13, 19, 60)
    print('Attempting to find_best_position(container, depth:', depth,' width:', width,' height:', height)
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")


    depth, width, height = (13, 39, 60)
    if (debug_load==True):
        print('Attempting to find_best_position(container, depth:', depth,' width:', width,' height:', height)
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    if  (debug_load==True):
        print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    if (debug_load==True):
        input("Press Enter to continue...")

    depth, width, height = (13, 39, 50)
    if (debug_load==True):
        print('Attempting to find_best_position(container, depth:', depth,' width:', width,' height:', height)
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    if (debug_load==True):
        print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    if (debug_load==True):
        input("Press Enter to continue...")

    depth, width, height = (10, 10, 65)
    if  (debug_load==True):
        print('Attempting to find_best_position(container, depth:', depth,' width:', width,' height:', height)
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    if  (debug_load==True):
       print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, depth, width, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

# output the lower and upper corners and the index of the boxes loaded in the container
    print('Boxes loaded in the container:')
    print('Index, Lower Corner, Upper Corner')
    for i in range(len(container.boxes)):
        print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])

def test_tietoevry1_load_container():
    # Start with an empty container: depth internal: 13620, width internal: 2480, Height:2670
    # initialize the container
    container_depth = 13620
    container_width = 2480
    container = PartiallyLoadedContainer(2, 2, [0, 13620], [0,2480])
    # set maximal height of the container
    container.height = 2670
    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()
    # wait for user input to continue
    input("Press Enter to continue...")
    # Make a list of boxes to be loaded in the container, first Deli
    # 6 * Pallet. width 660, depth 940, height 1203
    # 5 * Pallet. width 660, depth 940, height 1190
    # 4 * Pallet. width 660, depth 940, height 1398
    # 10 * Pallet. width 660, depth 920, height 1248
    deli1_boxes = [(660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203),
                   (660, 940, 1203),
                   (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190),
                   (660, 940, 1398), (660, 940, 1398), (660, 940, 1398), (660, 940, 1398),
                   (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248),
                   (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248)]
    # assign same colors to same size boxes
    tieto_deli_colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'green',
                            'green', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
                            'yellow', 'yellow', 'yellow']
    # load the boxes in the container
    for box in deli1_boxes:
        depth, width, height = box
        if (debug_load==True):
            print('Attempting to find_best_position(container, depth:', depth, ' width:', width, ' height:', height)
        best_row, best_column, best_score = find_best_position(container, depth, width, height)
        if (debug_load==True):
            print('Best position: ', best_row, best_column, 'Best score: ', best_score)
        load_box(container, best_row, best_column, depth, width, height)
        container.display_matplotlib()
        # wait for user input to continue
        if (debug_load == True):
            input("Press Enter to continue...")
    # Make a list of boxes to be loaded in the container, second Deli
    # 6 * Pallet, width 740, depth 1040, height 1263
    # 4 * Pallet, width 740, depth 1040, height 1185
    # 4 * Pallet, width 900, depth 650, height 1338
    deli2_boxes = [(740, 1040, 1263), (740, 1040, 1185), (900, 650, 1338)]
    # assign additional different colors to these boxes
    tieto_deli_colors.extend(['orange', 'orange', 'orange', 'orange', 'orange', 'orange', 'purple', 'purple', 'purple'])

    # load the boxes in the container
    for box in deli2_boxes:
        depth, width, height = box
        if (debug_load==True):
            print('Attempting to find_best_position(container, depth:', depth, ' width:', width, ' height:', height)
        best_row, best_column, best_score = find_best_position(container, depth, width, height)
        if (debug_load==True):
            print('Best position: ', best_row, best_column, 'Best score: ', best_score)
        load_box(container, best_row, best_column, depth, width, height)
        container.display_matplotlib()
        # wait for user input to continue
        if (debug_load == True):
            input("Press Enter to continue...")
    # output the lower and upper corners and the index of the boxes loaded in the container
    if (debug_load== True):
        print('Boxes loaded in the container:')
        print('Index, Lower Corner, Upper Corner')

    if (debug_load== True):
        for i in range(len(container.boxes)):
            print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])
    # make a list of boxes in json format
    boxes_json = print_json_for_list_of_boxes(container.boxes_index, tieto_deli_colors, container.boxes, container.boxes_lower_corner)
    print(boxes_json)
# make the below part a test function for load_box
#container = PartiallyLoadedContainer(4, 4, [0, 10, 20,34], [0, 10, 20, 30])

def test_load_box():
    # Example usage:
    container = PartiallyLoadedContainer(4, 4, [0, 10, 20,34], [0, 10, 20, 30])

    # Set heights for specific cells (heights in the range [0, 100])
    container.set_height(0, 1, 30)
    container.set_height(1, 1, 60)
    # Display the container using Matplotlib with grayscale heights and a legend
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific depth and height
    load_box(container, 1, 1, 5, 4, 10)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific depth and height
    load_box(container, 0, 1, 6
             , 5, 10)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific depth and height
    load_box(container, 0, 0, 10
             , 20, 70)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific depth and height
    load_box(container, 3, 3, 14
         , 5, 17)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")
    # end of the test function for load_box


#test_load_box()
#test_evaluate_space_feasibility()
#test_find_best_position()
#test_tietoevry1_load_container()
# end of the test functions
