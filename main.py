import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import mcolors module
class PartiallyLoadedContainer:
    def __init__(self, rows, columns, depth_coordinates, horizontal_coordinates):
        # Initialize the matrix for heights
        self.height_matrix = [[0 for _ in range(columns)] for _ in range(rows)]

        # Initialize arrays for depth and horizontal coordinates
        self.depth_coordinates = [0] * rows
        self.horizontal_coordinates = [0] * columns
        # Check the length of the depth coordinates array
        if len(depth_coordinates) != rows:
            raise ValueError("Invalid number of depth coordinates.")
        # Check the length of the horizontal coordinates array
        if len(horizontal_coordinates) != columns:
            raise ValueError("Invalid number of horizontal coordinates.")
        # Set the depth and horizontal coordinates
        for i in range(rows):
            self.depth_coordinates[i] = depth_coordinates[i]
        for j in range(columns):
            self.horizontal_coordinates[j] = horizontal_coordinates[j]

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
        self.height_matrix.insert(position, [0] * len(self.horizontal_coordinates))

        # Add the new row height to the depth coordinates array
        self.depth_coordinates.insert(position, real_depth)
        # replicate all height values in the new row
        for i in range(len(self.horizontal_coordinates)):
            self.height_matrix[position][i] = self.height_matrix[position-1][i]


    def delete_depth_coordinate(self, position):
        """Delete a depth coordinate level (row) from the container."""
        if position < 0 or position >= len(self.depth_coordinates):
            raise ValueError("Invalid position for deleting a depth coordinate.")

        # Delete the corresponding row from the height matrix
        del self.height_matrix[position]

        # Delete the depth coordinate from the array
        del self.depth_coordinates[position]

    def add_horizontal_coordinate(self, position, real_column=0.0):
        """Add a new horizontal coordinate level (column) to the container."""
        if position < 0 or position > len(self.horizontal_coordinates):
            raise ValueError("Invalid position for adding a horizontal coordinate.")

        # Insert a new column in the height matrix with default heights
        for row in self.height_matrix:
            row.insert(position, 0)

        # Add the new column depth to the horizontal coordinates array
        self.horizontal_coordinates.insert(position, real_column)
        # replicate all height values in the new column
        for i in range(len(self.depth_coordinates)):
            self.height_matrix[i][position] = self.height_matrix[i][position-1]

    def delete_horizontal_coordinate(self, position):
        """Delete a horizontal coordinate level (column) from the container."""
        if position < 0 or position >= len(self.horizontal_coordinates):
            raise ValueError("Invalid position for deleting a horizontal coordinate.")

        # Delete the corresponding column from the height matrix
        for row in self.height_matrix:
            del row[position]

        # Delete the horizontal coordinate from the array
        del self.horizontal_coordinates[position]

    def display_container(self):
        """Display the container's current state, including heights."""
        for i in range(len(self.depth_coordinates)):
            for j in range(len(self.horizontal_coordinates)):
                print(f"({self.depth_coordinates[i]}, {self.horizontal_coordinates[j]}): {self.height_matrix[i][j]}")

    def display_matplotlib(self):
        """Display the container graphically using Matplotlib with grayscale heights and a legend."""
        rows = len(self.depth_coordinates)
        columns = len(self.horizontal_coordinates)

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Define colormap for grayscale heights from white to black not using get_cmap
        #cmap = plt.cm.get_cmap('gray', lut=256)
        cmap = plt.colormaps['viridis']

        # Create a grid to represent the container with grayscale heights
        for i in range(rows):
            for j in range(columns):
                height = self.height_matrix[i][j]
                if height > 0:
                    color = cmap(height / 100.0)  # Scale heights to the [0, 1] range for grayscale
                    ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, facecolor=color, edgecolor='black'))

        # Set axis: choose the limits and tic label  according to the horizontal and depth coordinate values
        ax.set_xlim(0, columns)
        ax.set_ylim(-rows, 0)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel('Horizontal Coordinate')
        ax.set_ylabel('Depth Coordinate')

        ax.set_xticks(range(columns))
        ax.set_xticklabels(self.horizontal_coordinates)
        ax.set_yticks(range(-rows, 0))
        # Flip array depth_coordinates to display the depth coordinates in the right orderand remove first element
        invertedCoordinates=self.depth_coordinates[::-1]
        # plot yticks in the right order and to one level above
        ax.set_yticks(range(-rows+1, 1))
        ax.set_yticklabels(invertedCoordinates)

        # move the yticks one step to the bottom
        ax.tick_params(axis='y', which='major', pad=15)


        #ax.set_xlim(0, columns)
        #ax.set_ylim(-rows, 0)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel('Horizontal Coordinate')
        ax.set_ylabel('Depth Coordinate')

        # Create a legend for height levels
        norm = mcolors.Normalize(vmin=0, vmax=100)  # Assuming heights are in the range [0, 100]
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Height Level')
        # add height levels in to the grid cells
        for i in range(rows):
            for j in range(columns):
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
def load_box(container, row, column, width, depth, height):
    """Load a box into the container at a specific position with a specific width and height."""
    # Check the real coordinates of row and column, using the container's coordinates
    real_row = container.depth_coordinates[row]
    real_column = container.horizontal_coordinates[column]
    # compute the coordinates after the box is loaded
    real_row_after = real_row + depth
    real_column_after = real_column + width
    # compute the real height at column and row
    real_height = container.get_height(row, column)
    # compute the real height after the box is loaded
    real_height_after = real_height + height
    # check if the box fits in the container
    if real_row_after > container.depth_coordinates[-1] or real_column_after > container.horizontal_coordinates[-1]:
        # do not load the box if it does not fit
        print('box does not fit')
        return False
    else:
        # add box to the container and update coordinates and heights
        # First find the column and row where the upper real coordinate corner of the box is located
        # Find the column where the upper real coordinate corner of the box is located
        for i in range(len(container.horizontal_coordinates)):
            if ((real_column_after >= container.horizontal_coordinates[i])
                    and (real_column_after <= container.horizontal_coordinates[i+1])):
                new_column = i
                break
        # Find in the same way the row where the upper real coordinate corner of the box is located
        for i in range(len(container.depth_coordinates)):
            if ((real_row_after >= container.depth_coordinates[i])
                    and (real_row_after <= container.depth_coordinates[i+1])):
                new_row = i
                break
        # Add a coordinate level (new_row) if necessary
        if real_row_after < container.depth_coordinates[new_row+1]:
            container.add_depth_coordinate(new_row + 1, real_row_after)
        # Add a coordinate level (new_column) if necessary
        if real_column_after < container.horizontal_coordinates[new_column+1]:
            container.add_horizontal_coordinate(new_column+1, real_column_after)
    # Update heights from in the box from row, colum to new_row and new_column
    for i in range(row, new_row+1):
        for j in range(column, new_column+1):
            container.set_height(i, j, real_height_after)
    return True

# write a test script that loads a box into the container and updates the container's state and coordinates
# and displays the container's state before and after loading the box
# Example usage:
container = PartiallyLoadedContainer(4, 4, [0, 10, 20,34], [0, 10, 20, 30])

# Set heights for specific cells (heights in the range [0, 100])
container.set_height(0, 1, 30)
container.set_height(1, 1, 60)
# Display the container using Matplotlib with grayscale heights and a legend
container.display_matplotlib()
#wait for user input to continue
input("Press Enter to continue...")

# Load a box into the container at a specific position with a specific width and height
load_box(container, 1, 1, 5, 4, 10)
container.display_matplotlib()
#wait for user input to continue
input("Press Enter to continue...")

# Load a box into the container at a specific position with a specific width and height
load_box(container, 0, 1, 6
         , 5, 10)
container.display_matplotlib()
#wait for user input to continue
input("Press Enter to continue...")

# Load a box into the container at a specific position with a specific width and height
load_box(container, 0, 0, 10
         , 20, 70)
container.display_matplotlib()
#wait for user input to continue
input("Press Enter to continue...")

# Load a box into the container at a specific position with a specific width and height
load_box(container, 3, 3, 14
         , 5, 17)
container.display_matplotlib()
#wait for user input to continue
input("Press Enter to continue...")
