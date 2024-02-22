import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from genetic_algorithm import *
from visualization import *
import matplotlib.colors as mcolors
from package import *

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
        score = width_of_column_after
                 #+ 0.00001 * abs((width_of_row_after - width_of_row)/2 - container.width/2))
        return feasibility, score, error_message


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



# write a test script that evaluates if a box shaped item can be placed at the integer corner (row, column) as its lower corner
# and it is (1) well supported by the container floor or previously loaded boxes (even height level).
# (2) it does not exceed the container height and (3) it does not exceed the container depth and width.
# The function returns True if the box can be placed at the corner (row, column) and False otherwise.
# The score reflects for a feasible place how well the box fits on previously loaded boxes. A blend of loading meters, and axle balance
# Example usage:
