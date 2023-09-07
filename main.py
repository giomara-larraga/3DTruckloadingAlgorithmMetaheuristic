import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import mcolors module
class PartiallyLoadedContainer:
    def __init__(self, rows, columns):
        # Initialize the matrix for heights
        self.height_matrix = [[0 for _ in range(columns)] for _ in range(rows)]

        # Initialize arrays for vertical and horizontal coordinates
        self.vertical_coordinates = [0] * rows
        self.horizontal_coordinates = [0] * columns

    def get_height(self, row, column):
        """Get the height of the cargo at a specific cell."""
        return self.height_matrix[row][column]

    def set_height(self, row, column, height):
        """Set the height of the cargo at a specific cell."""
        self.height_matrix[row][column] = height

    def add_vertical_coordinate(self, position, row_height=0):
        """Add a new vertical coordinate level (row) to the container."""
        if position < 0 or position > len(self.vertical_coordinates):
            raise ValueError("Invalid position for adding a vertical coordinate.")

        # Insert a new row in the height matrix with default heights
        self.height_matrix.insert(position, [0] * len(self.horizontal_coordinates))

        # Add the new row height to the vertical coordinates array
        self.vertical_coordinates.insert(position, row_height)

    def delete_vertical_coordinate(self, position):
        """Delete a vertical coordinate level (row) from the container."""
        if position < 0 or position >= len(self.vertical_coordinates):
            raise ValueError("Invalid position for deleting a vertical coordinate.")

        # Delete the corresponding row from the height matrix
        del self.height_matrix[position]

        # Delete the vertical coordinate from the array
        del self.vertical_coordinates[position]

    def add_horizontal_coordinate(self, position, column_width=0):
        """Add a new horizontal coordinate level (column) to the container."""
        if position < 0 or position > len(self.horizontal_coordinates):
            raise ValueError("Invalid position for adding a horizontal coordinate.")

        # Insert a new column in the height matrix with default heights
        for row in self.height_matrix:
            row.insert(position, 0)

        # Add the new column width to the horizontal coordinates array
        self.horizontal_coordinates.insert(position, column_width)

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
        for i in range(len(self.vertical_coordinates)):
            for j in range(len(self.horizontal_coordinates)):
                print(f"({self.vertical_coordinates[i]}, {self.horizontal_coordinates[j]}): {self.height_matrix[i][j]}")

    def display_matplotlib(self):
        """Display the container graphically using Matplotlib with grayscale heights and a legend."""
        rows = len(self.vertical_coordinates)
        columns = len(self.horizontal_coordinates)

        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Define colormap for grayscale heights
        cmap = plt.cm.get_cmap('gray', lut=256)

        # Create a grid to represent the container with grayscale heights
        for i in range(rows):
            for j in range(columns):
                height = self.height_matrix[i][j]
                if height > 0:
                    color = cmap(height / 100.0)  # Scale heights to the [0, 1] range for grayscale
                    ax.add_patch(plt.Rectangle((j, -i - 1), 1, 1, facecolor=color, edgecolor='black'))

        # Set axis limits and labels
        ax.set_xlim(0, columns)
        ax.set_ylim(-rows, 0)
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel('Horizontal Coordinate')
        ax.set_ylabel('Vertical Coordinate')

        # Create a legend for height levels
        norm = mcolors.Normalize(vmin=0, vmax=100)  # Assuming heights are in the range [0, 100]
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        plt.colorbar(sm, ax=ax, label='Height Level')

        # Show the plot
        plt.gca().invert_yaxis()  # Invert the y-axis to match grid coordinates
        plt.grid(True)
        plt.show()

# Example usage:
container = PartiallyLoadedContainer(3, 4)

# Set heights for specific cells (heights in the range [0, 100])
container.set_height(0, 1, 30)
container.set_height(1, 2, 60)

# Display the container using Matplotlib with grayscale heights and a legend
container.display_matplotlib()

# Add a new vertical coordinate (row) at position 1 with a row height of 15
container.add_vertical_coordinate(1, 15)

# Add a new horizontal coordinate (column) at position 2 with a column width of 25
container.add_horizontal_coordinate(2, 25)

# Display the modified container using Matplotlib with grayscale heights and a legend
container.display_matplotlib()

# Display the modified state
container.display_container()








