import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import mcolors module
# The container has a length, a depth and a height. The container is partially loaded with cargo (box shaped items).
# The cargo is loaded in the container in a matrix of cells. Each cell has a height.
class PartiallyLoadedContainer:
    def __init__(self, columns, rows, length_coordinates, depth_coordinates, container_length=70, container_depth=100, container_height=100,):
        # Initialize the container's dimensions
        self.height = container_height
        self.length = length_coordinates[-1]
        self.depth = depth_coordinates[-1]
        # Initialize the matrix for heights
        self.height_matrix = [[0 for _ in range(columns)] for _ in range(rows)]

        # Initialize arrays for depth and length coordinates
        self.depth_coordinates = [0] * rows
        self.length_coordinates = [0] * columns
        # Check the length of the depth coordinates array
        if len(depth_coordinates) != rows:
            raise ValueError("Invalid number of depth coordinates.")
        # Check the length of the length coordinates array
        if len(length_coordinates) != columns:
            raise ValueError("Invalid number of length coordinates.")
        # Set the depth and length coordinates
        for i in range(rows):
            self.depth_coordinates[i] = depth_coordinates[i]
        for j in range(columns):
            self.length_coordinates[j] = length_coordinates[j]

    def get_height(self, row, column):
        """Get the height of the cargo at a specific cell."""
        return self.height_matrix[row][column]

    def set_height(self, row, column, height):
        """Set the height of the cargo at a specific cell."""
        self.height_matrix[row][column] = height

    def add_depth_coordinate(self, position, real_depth=0.0):
        """Add a new depth coordinate level (row) to the container."""
        if position < 0 or position > len(self.depth_coordinates):
            raise ValueError("Invalid position for adding a depth coordinate.")

        # Insert a new row in the height matrix with default heights
        self.height_matrix.insert(position, [0] * len(self.length_coordinates))

        # Add the new row height to the depth coordinates array
        self.depth_coordinates.insert(position, real_depth)
        # replicate all height values in the new row
        for i in range(len(self.length_coordinates)):
            self.height_matrix[position][i] = self.height_matrix[position-1][i]


    def delete_depth_coordinate(self, position):
        """Delete a depth coordinate level (row) from the container."""
        if position < 0 or position >= len(self.depth_coordinates):
            raise ValueError("Invalid position for deleting a depth coordinate.")

        # Delete the corresponding row from the height matrix
        del self.height_matrix[position]

        # Delete the depth coordinate from the array
        del self.depth_coordinates[position]

    def add_length_coordinate(self, position, depth_of_column=0.0):
        """Add a new length coordinate level (column) to the container."""
        if position < 0 or position > len(self.length_coordinates):
            raise ValueError("Invalid position for adding a length coordinate.")

        # Insert a new column in the height matrix with default heights
        for row in self.height_matrix:
            row.insert(position, 0)

        # Add the new column depth to the length coordinates array
        self.length_coordinates.insert(position, depth_of_column)
        # replicate all height values in the new column
        for i in range(len(self.depth_coordinates)):
            self.height_matrix[i][position] = self.height_matrix[i][position-1]

    def delete_length_coordinate(self, position):
        """Delete a length coordinate level (column) from the container."""
        if position < 0 or position >= len(self.length_coordinates):
            raise ValueError("Invalid position for deleting a length coordinate.")

        # Delete the corresponding column from the height matrix
        for row in self.height_matrix:
            del row[position]

        # Delete the length coordinate from the array
        del self.length_coordinates[position]

    def display_container(self):
        """Display the container's current state, including heights."""
        for i in range(len(self.depth_coordinates)):
            for j in range(len(self.length_coordinates)):
                print(f"({self.depth_coordinates[i]}, {self.length_coordinates[j]}): {self.height_matrix[i][j]}")

    def display_matplotlib(self):
        """Display the container graphically using Matplotlib with grayscale heights and a legend."""
        rows = len(self.depth_coordinates)
        columns = len(self.length_coordinates)

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Define colormap for grayscale heights from white to black not using get_cmap
        #cmap = plt.cm.get_cmap('gray', lut=256)
        cmap = plt.colormaps['viridis']

        # Create a grid to represent the container with grayscale heights
        for i in range(rows-1):
            for j in range(columns-1):
                height = self.height_matrix[i][j]
                if height > 0:
                    color = cmap(height / 100.0)  # Scale heights to the [0, 1] range for grayscale
                    ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, facecolor=color, edgecolor='black'))

        # Set axis: choose the limits and tic label  according to the length and depth coordinate values
        ax.set_xlim(0, columns)
        ax.set_ylim(-rows, 0)
        ax.set_aspect('equal', adjustable='box')

        ax.set_xticks(range(columns))
        ax.set_xticklabels(self.length_coordinates)
        ax.set_yticks(range(-rows, 0))
        # Flip array depth_coordinates to display the depth coordinates in the right orderand remove first element
        invertedCoordinates=self.depth_coordinates[::-1]
        # plot yticks in the right order and to one level above
        ax.set_yticks(range(-rows+1, 1))
        ax.set_yticklabels(invertedCoordinates)

        # move the yticks one step to the bottom
        ax.tick_params(axis='y', which='major', pad=15)

        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel('Length Coordinate')
        ax.set_ylabel('Depth Coordinate')

        # Create a legend for height levels
        norm = mcolors.Normalize(vmin=0, vmax=100)  # Assuming heights are in the range [0, 100]
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
def load_box(container, row, column, length, depth, height):
    """Load a box into the container at a specific position with a specific length and height."""
    # Check the real coordinates of row and column, using the container's coordinates
    depth_of_row = container.depth_coordinates[row]
    depth_of_column = container.length_coordinates[column]
    # compute the coordinates after the box is loaded
    depth_of_row_after = depth_of_row + depth
    depth_of_column_after = depth_of_column + length
    # compute the real height at column and row
    real_height = container.get_height(row, column)
    # compute the real height after the box is loaded
    real_height_after = real_height + height
    # check if the box fits in the container
    if depth_of_row_after > container.depth_coordinates[-1] or depth_of_column_after > container.length_coordinates[-1]:
        # do not load the box if it does not fit
        print('box does not fit')
        return False
    else:
        # add box to the container and update coordinates and heights
        # First find the column and row where the upper real coordinate corner of the box is located
        # Find the column where the upper real coordinate corner of the box is located
        for i in range(len(container.length_coordinates)):
            if ((depth_of_column_after >= container.length_coordinates[i])
                    and (depth_of_column_after <= container.length_coordinates[i+1])):
                new_column = i
                break
        # Find in the same way the row where the upper real coordinate corner of the box is located
        for i in range(len(container.depth_coordinates)):
            if ((depth_of_row_after >= container.depth_coordinates[i])
                    and (depth_of_row_after <= container.depth_coordinates[i+1])):
                new_row = i
                break
        # Add a coordinate level (new_row) if necessary
        if depth_of_row_after < container.depth_coordinates[new_row+1]:
            container.add_depth_coordinate(new_row + 1, depth_of_row_after)
        # Add a coordinate level (new_column) if necessary
        if depth_of_column_after < container.length_coordinates[new_column+1]:
            container.add_length_coordinate(new_column+1, depth_of_column_after)
    # Update heights from in the box from row, colum to new_row and new_column
    for i in range(row, new_row+1):
        for j in range(column, new_column+1):
            container.set_height(i, j, real_height_after)
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

    # Load a box into the container at a specific position with a specific length and height
    load_box(container, 1, 1, 5, 4, 10)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific length and height
    load_box(container, 0, 1, 6
             , 5, 10)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific length and height
    load_box(container, 0, 0, 10
             , 20, 70)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")

    # Load a box into the container at a specific position with a specific length and height
    load_box(container, 3, 3, 14
         , 5, 17)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")
    # end of the test function for load_box

def evaluate_space_feasibility(container, row, column, length, depth, height):
# This function evaluates if a box shaped item can be placed at the integer corner (row, column) as its lower corner
# and it is (1) well supported by the container floor or previously loaded boxes (even height level).
# (2) it does not exceed the container height and (3) it does not exceed the container length and depth.
# The function returns True if the box can be placed at the corner (row, column) and False otherwise.
# The score reflects for a feasible place how well the box fits on previously loaded boxes.
    score = 0.0;
    feasibility = True
    error_message = 'No Problems Encountered'
    # Check the real coordinates of row and column, using the container's coordinates
    depth_of_row = container.depth_coordinates[row]
    depth_of_column = container.length_coordinates[column]
    # compute the coordinates after the box is loaded
    depth_of_row_after = depth_of_row + depth
    depth_of_column_after = depth_of_column + length
    # compute the real height at column and row
    real_height = container.get_height(row, column)
    # compute the real height after the box is loaded
    real_height_after = real_height + height
    # check if the box fits in the container
    if depth_of_row_after > container.depth_coordinates[-1] or depth_of_column_after > container.length_coordinates[-1]:
        feasibility = False
        error_message = 'box does not fit'
        return feasibility, score, error_message
    else:
        height_lower_left_corner = container.get_height(row, column)
        # check if the box is well supported by the container floor or previously loaded boxes (even height level).
        # compute the depth in the integer grid coordinates, using the depth coordinates and the depth of the corner and the depth of the corner after the box is loaded
        row_after = 0
        for i in range(len(container.depth_coordinates)):
            if ((depth_of_row_after > container.depth_coordinates[i])
                    and (depth_of_row_after <= container.depth_coordinates[i+1])):
                row_after = i
                break
        # compute the length in the integer grid coordinates, using the length coordinates and the length of the corner and the length of the corner after the box is loaded
        column_after = 0
        for i in range(len(container.length_coordinates)):
            if ((depth_of_column_after > container.length_coordinates[i])
                    and (depth_of_column_after <= container.length_coordinates[i+1])):
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
        # check if the box exceeds the container length
        if depth_of_column_after > container.length_coordinates[-1]:
            feasibility = False
            error_message = 'box exceeds the container length'
            return feasibility, score, error_message
        # check if the box exceeds the container depth
        if depth_of_row_after > container.depth_coordinates[-1]:
            feasibility = False
            error_message = 'box exceeds the container depth'
            return feasibility, score,  error_message
        # compute the score: loading meters to be held small, prefer the middle of the container.
        score = depth_of_column_after + 0.1 * abs((depth_of_row_after - depth_of_row)/2 - container.depth)
        return feasibility, score, error_message

# write a test script that evaluates if a box shaped item can be placed at the integer corner (row, column) as its lower corner
# and it is (1) well supported by the container floor or previously loaded boxes (even height level).
# (2) it does not exceed the container height and (3) it does not exceed the container length and depth.
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
    column, row, length, depth, height = (2, 2, 13, 19, 10)
    print('Attempting to load_box(container, column:', column,' row:', row, ' length', length,' depth:', depth,' height:', height)
    feasibility, score, error_message = evaluate_space_feasibility(container, row,column, length, depth, height)
    print('Feasibility: ', feasibility, 'Score: ', score, 'Error message: ', error_message)
    load_box(container, row, column,
         length, depth, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")


# Find the best position for a box shaped item with a specific length and height.
# The function returns the best position (row, column) and the score.
# The score reflects for a feasible place how well the box fits on previously loaded boxes. A blend of loading meters, and axle balance
def find_best_position(container, length, depth, height):
    best_score = 1000
    best_row = 0
    best_column = 0
    # Go through all possible positions for the lower left corner of the box
    for i in range(len(container.depth_coordinates)):
        for j in range(len(container.length_coordinates)):
            # Evaluate the feasibility of the position
            feasibility, score, error_message = evaluate_space_feasibility(container, i, j, length, depth, height)
            # If the position is feasible and the score is better than the best score so far, update the best score and position
            if feasibility and score < best_score:
                best_score = score
                best_row = i
                best_column = j # Update the best position
    return best_row, best_column, best_score

# write a test script that finds the best position for a box shaped item with a specific length and height.
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
    # Find the best position for a box shaped item with a specific length and height.

    length, depth, height = (13, 19, 10)
    print('Attempting to find_best_position(container, length:', length,' depth:', depth,' height:', height)
    best_row, best_column, best_score = find_best_position(container, length, depth, height)
    print('Best position: ', best_row, best_column, 'Best score: ', best_score)
    load_box(container, best_row, best_column, length, depth, height)
    container.display_matplotlib()
    #wait for user input to continue
    input("Press Enter to continue...")


# Calling the test functions
#test_load_box()
#test_evaluate_space_feasibility()
test_find_best_position()
