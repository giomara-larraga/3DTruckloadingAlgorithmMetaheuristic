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
