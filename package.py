# Define a data structure for each package
class Package:
    def __init__(self, item_id, width, height, depth, non_stackable, group_id):
        self.item_id = item_id
        self.width = width
        self.height = height
        self.depth = depth
        self.non_stackable = non_stackable
        self.x = 0  # Initialize x position
        self.y = 0  # Initialize y position
        self.z = 0  # Initialize z position
        self.group_id = group_id

    def __str__(self):
        return f"Package(package_id={self.id_item}, group_id={self.group_id})"
