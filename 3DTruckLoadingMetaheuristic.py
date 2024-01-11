import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import mcolors module
import numpy as np

# The container has a depth, a width and a height. The container is partially loaded with cargo (box shaped items).
# The cargo is loaded in the container in a matrix of cells. Each cell has a height.

# In debug mode, the process of loading is documented with print statements on the console
debug_load=False
class PartiallyLoadedContainer:
    def __init__(self, columns, rows, depth_coordinates, width_coordinates, container_depth=70, container_width=100, container_height=2600,):
        # Initialize the container's dimensions
        self.height = container_height
        self.depth = depth_coordinates[-1]
        self.width = width_coordinates[-1]
        # Initialize the matrix for heights
        self.height_matrix = [[0 for _ in range(columns)] for _ in range(rows)]

        # Initialize arrays for width and depth coordinates
        self.width_coordinates = [0] * rows
        self.depth_coordinates = [0] * columns
        # Check the depth of the width coordinates array
        if len(width_coordinates) != rows:
            raise ValueError("Invalid number of width coordinates.")
        # Check the depth of the depth coordinates array
        if len(depth_coordinates) != columns:
            raise ValueError("Invalid number of depth coordinates.")
        # Set the width and depth coordinates
        for i in range(rows):
            self.width_coordinates[i] = width_coordinates[i]
        for j in range(columns):
            self.depth_coordinates[j] = depth_coordinates[j]

        # Add a list of all boxes that are  loaded in the container, their index and their lower and upper corner
        self.boxes = []
        self.boxes_index = []
        self.boxes_lower_corner = []
        self.boxes_upper_corner = []


    def get_height(self, row, column):
        """Get the height of the cargo at a specific cell."""
        return self.height_matrix[row][column]

    def set_height(self, row, column, height):
        """Set the height of the cargo at a specific cell."""
        self.height_matrix[row][column] = height

    def add_width_coordinate(self, position, real_width=0.0):
        """Add a new width coordinate level (row) to the container."""
        if position < 0 or position > len(self.width_coordinates):
            raise ValueError("Invalid position for adding a width coordinate.")

        # Insert a new row in the height matrix with default heights
        self.height_matrix.insert(position, [0] * len(self.depth_coordinates))

        # Add the new row height to the width coordinates array
        self.width_coordinates.insert(position, real_width)
        # replicate all height values in the new row
        for i in range(len(self.depth_coordinates)):
            self.height_matrix[position][i] = self.height_matrix[position-1][i]


    def delete_width_coordinate(self, position):
        """Delete a width coordinate level (row) from the container."""
        if position < 0 or position >= len(self.width_coordinates):
            raise ValueError("Invalid position for deleting a width coordinate.")

        # Delete the corresponding row from the height matrix
        del self.height_matrix[position]

        # Delete the width coordinate from the array
        del self.width_coordinates[position]

    def add_depth_coordinate(self, position, width_of_column=0.0):
        """Add a new depth coordinate level (column) to the container."""
        if position < 0 or position > len(self.depth_coordinates):
            raise ValueError("Invalid position for adding a depth coordinate.")

        # Insert a new column in the height matrix with default heights
        for row in self.height_matrix:
            row.insert(position, 0)

        # Add the new column width to the depth coordinates array
        self.depth_coordinates.insert(position, width_of_column)
        # replicate all height values in the new column
        for i in range(len(self.width_coordinates)):
            self.height_matrix[i][position] = self.height_matrix[i][position-1]

    def delete_depth_coordinate(self, position):
        """Delete a depth coordinate level (column) from the container."""
        if position < 0 or position >= len(self.depth_coordinates):
            raise ValueError("Invalid position for deleting a depth coordinate.")

        # Delete the corresponding column from the height matrix
        for row in self.height_matrix:
            del row[position]

        # Delete the depth coordinate from the array
        del self.depth_coordinates[position]

    def display_container(self):
        """Display the container's current state, including heights."""
        for i in range(len(self.width_coordinates)):
            for j in range(len(self.depth_coordinates)):
                print(f"({self.width_coordinates[i]}, {self.depth_coordinates[j]}): {self.height_matrix[i][j]}")

    def display_matplotlib(self):
        """Display the container graphically using Matplotlib with grayscale heights and a legend."""
        rows = len(self.width_coordinates)
        columns = len(self.depth_coordinates)

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Define colormap for grayscale heights from white to black not using get_cmap
        #cmap = plt.cm.get_cmap('gray', lut=256)
        cmap = plt.colormaps['viridis']
        max_color=self.height

        # Create a grid to represent the container with grayscale heights
        for i in range(rows-1):
            for j in range(columns-1):
                height = self.height_matrix[i][j]
                if height > 0:
                    color = cmap(height / max_color)  # Scale heights to the [0, 1] range for grayscale
                    ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, facecolor=color, edgecolor='black'))

        # Set axis: choose the limits and tic label  according to the depth and width coordinate values
        ax.set_xlim(0, columns)
        ax.set_ylim(-rows, 0)
        ax.set_aspect('equal', adjustable='box')

        ax.set_xticks(range(columns))
        ax.set_xticklabels(self.depth_coordinates)
        ax.set_yticks(range(-rows, 0))
        # Flip array width_coordinates to display the width coordinates in the right orderand remove first element
        invertedCoordinates=self.width_coordinates[::-1]
        # plot yticks in the right order and to one level above
        ax.set_yticks(range(-rows+1, 1))
        ax.set_yticklabels(invertedCoordinates)

        # move the yticks one step to the bottom
        ax.tick_params(axis='y', which='major', pad=15)

        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel('depth Coordinate')
        ax.set_ylabel('width Coordinate')

        # Create a legend for height levels
        norm = mcolors.Normalize(vmin=0, vmax=max_color)  # Assuming heights are in the range [0, 100]
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Height Level')
        # add height levels in to the grid cells
        for i in range(rows-1):
            for j in range(columns-1):
                height = self.height_matrix[i][j]
                if height > 0:
                    # set textcolor to white if the height is less than 50
                    if (height < 50  and height > 0):
                        ax.text(j + 0.5, -i - 0.5, str(height), ha='center', va='center', color='white')
                    else:
                        ax.text(j + 0.5, -i - 0.5, str(height), ha='center', va='center', color='black')
                if height == 0:
                    # Make a string from coordinate pair i, j

                    # plot i,j in the cell coordinates
                    ax.text(j + 0.5, -i - 0.5, str(i) + ',' + str(j), ha='center', va='center', color='black')



        # Show the plot
        plt.gca().invert_yaxis()  # Invert the y-axis to match grid coordinates
        plt.grid(True)
        plt.show()

# Define a function that loads a single box into the container and updates the container's state and coordinates
def load_box(container, row, column, depth, width, height):
    """Load a box into the container at a specific position with a specific depth and height."""
    # Check the real coordinates of row and column, using the container's coordinates
    width_of_row = container.width_coordinates[row]
    width_of_column = container.depth_coordinates[column]
    # compute the coordinates after the box is loaded
    width_of_row_after = width_of_row + width
    width_of_column_after = width_of_column + depth
    # compute the real height at column and row
    real_height = container.get_height(row, column)
    # compute the real height after the box is loaded
    real_height_after = real_height + height
    # check if the box fits in the container
    if width_of_row_after > container.width_coordinates[-1] or width_of_column_after > container.depth_coordinates[-1]:
        # do not load the box if it does not fit
        print('box does not fit')
        return False
    else:
        # add box to the container and update coordinates and heights
        # First find the column and row where the upper real coordinate corner of the box is located
        # Find the column where the upper real coordinate corner of the box is located
        for i in range(len(container.depth_coordinates)):
            if ((width_of_column_after >= container.depth_coordinates[i])
                    and (width_of_column_after <= container.depth_coordinates[i+1])):
                new_column = i
                break
        # Find in the same way the row where the upper real coordinate corner of the box is located
        for i in range(len(container.width_coordinates)):
            if ((width_of_row_after >= container.width_coordinates[i])
                    and (width_of_row_after <= container.width_coordinates[i+1])):
                new_row = i
                break
        # Add a coordinate level (new_row) if necessary
        if width_of_row_after < container.width_coordinates[new_row+1]:
            container.add_width_coordinate(new_row + 1, width_of_row_after)
        # Add a coordinate level (new_column) if necessary
        if width_of_column_after < container.depth_coordinates[new_column+1]:
            container.add_depth_coordinate(new_column+1, width_of_column_after)
    # Update heights from in the box from row, colum to new_row and new_column
    for i in range(row, new_row+1):
        for j in range(column, new_column+1):
            container.set_height(i, j, real_height_after)
    # Add the real coordinate of the box to the list of lower corners
    container.boxes_lower_corner.append((width_of_row, width_of_column,real_height))
    # Add the real coordinate of the box to the list of upper corners
    container.boxes_upper_corner.append((width_of_row_after, width_of_column_after,real_height_after))
    # Add the index of the box to the list of boxes
    container.boxes_index.append(len(container.boxes_index))
    # Add the box to the list of boxes
    container.boxes.append((depth, width, height))
    return True

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

def evaluate_space_feasibility(container, row, column, depth, width, height):
# This function evaluates if a box shaped item can be placed at the integer corner (row, column) as its lower corner
# and it is (1) well supported by the container floor or previously loaded boxes (even height level).
# (2) it does not exceed the container height and (3) it does not exceed the container depth and width.
# The function returns True if the box can be placed at the corner (row, column) and False otherwise.
# The score reflects for a feasible place how well the box fits on previously loaded boxes.
    score = 0.0;
    feasibility = True
    error_message = 'No Problems Encountered'
    # Check the real coordinates of row and column, using the container's coordinates
    width_of_row = container.width_coordinates[row]
    width_of_column = container.depth_coordinates[column]
    # compute the coordinates after the box is loaded
    width_of_row_after = width_of_row + width
    width_of_column_after = width_of_column + depth
    # compute the real height at column and row
    real_height = container.get_height(row, column)
    # compute the real height after the box is loaded
    real_height_after = real_height + height
    # check if the box fits in the container
    if width_of_row_after > container.width_coordinates[-1] or width_of_column_after > container.depth_coordinates[-1]:
        feasibility = False
        error_message = 'box does not fit'
        return feasibility, score, error_message
    else:
        height_lower_left_corner = container.get_height(row, column)
        # check if the box is well supported by the container floor or previously loaded boxes (even height level).
        # compute the width in the integer grid coordinates, using the width coordinates and the width of the corner and the width of the corner after the box is loaded
        row_after = 0
        for i in range(len(container.width_coordinates)):
            if ((width_of_row_after > container.width_coordinates[i])
                    and (width_of_row_after <= container.width_coordinates[i+1])):
                row_after = i
                break
        # compute the depth in the integer grid coordinates, using the depth coordinates and the depth of the corner and the depth of the corner after the box is loaded
        column_after = 0
        for i in range(len(container.depth_coordinates)):
            if ((width_of_column_after > container.depth_coordinates[i])
                    and (width_of_column_after <= container.depth_coordinates[i+1])):
                column_after = i
                break
        # Go through all cells right below the box to be loaded and check if their height is the same
        for i in range(row, row_after+1):
            for j in range(column, column_after+1):
                if container.get_height(i, j) != height_lower_left_corner:
                    feasibility = False
                    error_message = 'box is not well supported by the container floor or previously loaded boxes (even height level)'
                    return feasibility, score,  error_message
        # check if the box exceeds the container height
        if real_height_after > container.height:
            feasibility = False
            error_message = 'box exceeds the container height'
            return feasibility, score, error_message
        # check if the box exceeds the container depth
        if width_of_column_after > container.depth_coordinates[-1]:
            feasibility = False
            error_message = 'box exceeds the container depth'
            return feasibility, score, error_message
        # check if the box exceeds the container width
        if width_of_row_after > container.width_coordinates[-1]:
            feasibility = False
            error_message = 'box exceeds the container width'
            return feasibility, score,  error_message
        # compute the score: loading meters to be held small, prefer the middle of the container.
        #score = width_of_column_after + 0.001 * abs((width_of_row_after - width_of_row)/2 - container.width)
        score = width_of_column_after + 0.00001 * abs((width_of_row_after - width_of_row)/2 - container.width/2)
        return feasibility, score, error_message

# write a test script that evaluates if a box shaped item can be placed at the integer corner (row, column) as its lower corner
# and it is (1) well supported by the container floor or previously loaded boxes (even height level).
# (2) it does not exceed the container height and (3) it does not exceed the container depth and width.
# The function returns True if the box can be placed at the corner (row, column) and False otherwise.
# The score reflects for a feasible place how well the box fits on previously loaded boxes. A blend of loading meters, and axle balance
# Example usage:

#test_load_box()

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


# Find the best position for a box shaped item with a specific depth and height.
# The function returns the best position (row, column) and the score.
# The score reflects for a feasible place how well the box fits on previously loaded boxes. A blend of loading meters, and axle balance
def find_best_position(container, depth, width, height):
    best_score = 10000000000
    best_row = 0
    best_column = 0
    # Go through all possible positions for the lower left corner of the box
    for i in range(len(container.width_coordinates)):
        for j in range(len(container.depth_coordinates)):
            # Evaluate the feasibility of the position
            feasibility, score, error_message = evaluate_space_feasibility(container, i, j, depth, width, height)
            # If the position is feasible and the score is better than the best score so far, update the best score and position
            if feasibility and score <= best_score:
                best_score = score
                best_row = i
                best_column = j # Update the best position
    return best_row, best_column, best_score

# write a test script that finds the best position for a box shaped item with a specific depth and height.
# The function returns the best position (row, column) and the score.
# The score reflects for a feasible place how well the box fits on previously loaded boxes. A blend of loading meters, and axle balance
# Example usage:
#test_load_box()

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

# 6 * Pallet. width 660, depth 940, height 1203
#
# 5 * Pallet. width 660, depth 940, height 1190
#
# 4 * Pallet. width 660, depth 940, height 1398
#
# 10 * Pallet. width 660, depth 920, height 1248
#
# 4 * Pallet. width 660, depth 920, height 1320
#
# Loading parameters: no special rules required
#
# Deli 2 (front of trailer)
#
# 6 * Pallet, width 740, depth 1040, height 1263
#
# 4 * Pallet, width 740, depth 1040, height 1185
#
# 4 * Pallet, width 900, depth 650, height 1338
#
# Loading parameters: no special rules required
# Function for testing the loading of a container test case above:
#
# Message by TE about the visualization tool specification:
# We have developed a prototype of a proper 3D load visualization. You can find it here:
# https://prooptthreejsdemostatic.z22.web.core.windows.net/
# The idea is to make a list of boxes in a json format and then
# visualize it
# The json format is as follows:
# { "container": {
# "size": { // Provide here the dimensions of the container itself.
# "width": 2800,
# "height": 3400,
# "depth": 8000
#},
# "items": [ // Provide here an array of items.
#{
#"id": "BOX1", // This value is shown when the item is hovered with cursor.
#        "type": "box", // “box” or “cylinder”
#        "color": "red",
#        "size": {
#          "width": 800, // Box dimensions
#          "height": 1600,
#          "depth": 1200
#        },
#        "position": { // Item coordinates.
#        // The front bottom left corner of the container is at (x=depth=0,y=width=0,height=0).
#          "x": 0,
#          "y": 0,
#          "z": 0
#        }
#      }
#    ]
# print in the json format (see example above) a list of boxes, index, size of boxes, lower corners in container (with height)
# to json format; assign random colors to the boxes according to colors list (default is 'red')
def print_json_for_list_of_boxes(boxes_indexes, colors, boxes_sizes, boxes_lower_corners,cdepth=8000, cwidth=3400, cheight=2800):
# print in the json format (see example above) a list of boxes, index, size of boxes, lower corners in container (with height)
# to json format; assign random colors to the boxes according to colors list (default is 'red')
# transform cdepth, clength, cwidth to strings

    print('{ "container": {')
    print('"size": {')
    print('"width":' + str(cwidth) + ',')
    print('"height":' + str(cheight) + ',')
    print('"depth":' + str(cdepth))
    print('},')
    print('"items": [')
    for i in range(len(boxes_indexes)):
        print('{', end=" ")
        print('"id": "BOX', boxes_indexes[i], '",',  end=" ")
        print('"type": "box",', end=" ")
        # Make a string from the color assignment to avoid spaces around the color name; no line breaks
        color_print = '"color": "' + colors[i].strip() + '",'
        print(color_print, end=" ")
        print('"size": {', end=" ")
        print('"width": ', boxes_sizes[i][1], ',', end=" ")
        print('"height": ', boxes_sizes[i][2], ',', end=" ")
        print('"depth": ', boxes_sizes[i][0], end=" ")
        print('},', end=" ")
        print('"position": {', end=" ")
        print('"x": ', boxes_lower_corners[i][0], ',', end=" ")
        print('"y": ', boxes_lower_corners[i][2], ',', end=" ")
        print('"z": ', boxes_lower_corners[i][1], end=" ")
        print('}', end=" ")
        if (i < len(boxes_indexes)-1):
            print('},')
        else:
            print('}')
    print(']', end=" ")
    print('}'+ '}')

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

# Calling the test functions

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

def calculate_fitness_3DContainerLoader(population, packages, cheight,cdepth, cwidth):
    fitness_scores = []

    for chromosome in population:
        # make a list of items to be loaded in the container by putting packages in the order of the chromosome
        items_to_be_loaded = []
        for i, package_idx in enumerate(chromosome):
            package = packages[package_idx]
            items_to_be_loaded.append((package.width, package.height, package.depth))
        # initialize the container
        container = PartiallyLoadedContainer(2, 2, [0, cdepth], [0,cwidth])
        container.height = cheight

        # load the boxes in the container
        best_score = 10000000000
        for box in items_to_be_loaded:
            depth, width, height = box
            best_row, best_column, best_score = find_best_position(container, depth, width, height)
            load_box(container, best_row, best_column, depth, width, height)
        # calculate the fitness score
        fitness_scores.append(container.depth-best_score)
    return np.array(fitness_scores)



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
def genetic_algorithm(packages, population_size, num_generations, mutation_rate, loading_method,
                      cheight = 2670,cdepth = 13620, cwidth = 2480):
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
    fitness_scores = []
    if (loading_method == '2D'):
        fitness_scores = calculate_fitness(population, packages, cheight, cdepth, cwidth)
    elif (loading_method == '3D'):
        # set dimensions  of the container
        fitness_scores = calculate_fitness_3DContainerLoader(population, packages, cheight, cdepth, cwidth)
    best_solution_idx = np.argmax(fitness_scores)
    best_chromosome = population[best_solution_idx]


    best_fitness = fitness_scores[best_solution_idx]

    return best_chromosome, best_fitness



deli1_boxes = [(660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203), (660, 940, 1203),
                       (660, 940, 1203),
                       (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190), (660, 940, 1190),
                       (660, 940, 1398), (660, 940, 1398), (660, 940, 1398), (660, 940, 1398),
                       (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248),
                       (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248), (660, 920, 1248)]
# make packages from the list of deli1_boxes. LEN, WID, HEI, NON_STACKABLE
packages = []
for box in deli1_boxes:
    depth, width, height = box
    packages.append(Package(depth, width, height, False))


# Run the genetic algorithm
best_chromosome, best_fitness = genetic_algorithm(
    packages, POPULATION_SIZE, NUM_GENERATIONS, MUTATION_RATE, '3D'
)




# Print the best loading order
print("Best Loading Order:", best_chromosome, "Fitness:", best_fitness)


# translate the best chromosome into a list of items to be loaded in the container
tieto_deli_colors = ['red', 'red', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'green',
                            'green', 'green', 'green', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
                            'yellow', 'yellow', 'yellow','orange','orange']
items_to_be_loaded = []

color_package = []
for i, package_idx in enumerate(best_chromosome):
    package = packages[package_idx]
    color_package.append(tieto_deli_colors[package_idx])
    items_to_be_loaded.append((package.width, package.height, package.depth))

# initialize the container
container = PartiallyLoadedContainer(2, 2, [0, 13620], [0,2480])
container.height = 2670
# load the boxes in the container
best_score = 10000000000
for box in items_to_be_loaded:
    depth, width, height = box
    best_row, best_column, best_score = find_best_position(container, depth, width, height)
    load_box(container, best_row, best_column, depth, width, height)
# Display the container using Matplotlib with grayscale heights and a legend
container.display_matplotlib()

# output the lower and upper corners and the index of the boxes loaded in the container
print('Boxes loaded in the container:')
print('Index, Lower Corner, Upper Corner')
for i in range(len(container.boxes)):
    print(container.boxes_index[i], container.boxes_lower_corner[i], container.boxes_upper_corner[i])
    print(color_package)
# make a list of boxes in json format
# assign same colors to same size boxes
boxes_json = print_json_for_list_of_boxes(container.boxes_index, color_package, container.boxes, container.boxes_lower_corner, cdepth=13620+1, cwidth=2480+1, cheight=2670+1)
print(boxes_json)

#test_load_box()
#test_evaluate_space_feasibility()
#test_find_best_position()
#test_tietoevry1_load_container()
# end of the test functions
