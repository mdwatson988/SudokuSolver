class SudokuTreeNode:
    def __init__(self, x, y, value=None):
        self.value = value  # data
        self.children = []  # references to other nodes
        self.x = x # column location
        self.y = y # row location
        self.coords = (x, y)
        self.box = self.determine_box() # sub box containing node
        self.attempted_values = set() # values not to try again at particular step in solver function

    def __repr__(self):
        return f"Tree node with a value of {self.value} at {self.coords}"

    def add_child(self, child_node):
        # creates parent-child relationship
        self.children.append(child_node)

    def determine_box(self):
        # determines which box each node falls into for 1 to 9 pattern. Numbered from top-left, right then down
        if 1 <= self.x <= 3:
            if 1 <= self.y <= 3:
                return 1
            if 4 <= self.y <= 6:
                return 4
            if 7 <= self.y <= 9:
                return 7
        if 4 <= self.x <= 6:
            if 1 <= self.y <= 3:
                return 2
            if 4 <= self.y <= 6:
                return 5
            if 7 <= self.y <= 9:
                return 8
        if 7 <= self.x <= 9:
            if 1 <= self.y <= 3:
                return 3
            if 4 <= self.y <= 6:
                return 6
            if 7 <= self.y <= 9:
                return 9