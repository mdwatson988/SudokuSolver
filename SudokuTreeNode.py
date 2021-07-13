class SudokuTreeNode:
    def __init__(self, sudoku_object, x, y, value=None):
        self.value = value  # data
        self.children = []  # references to child nodes
        self.x = x # column location
        self.y = y # row location
        self.coords = (x, y)
        self.box = self.determine_box(sudoku_object) # sudoku box in which the node falls
        self.attempted_values = set() # values not to try again at particular step in solver function

    def __repr__(self):
        return f"Tree node with a value of {self.value} at {self.coords}"

    def add_child(self, child_node):
        # creates parent-child relationship
        self.children.append(child_node)

    def determine_box(self, sudoku_object):
        max_size = sudoku_object.max_size
        # determines which box each node falls into. Numbered from top-left, right then down
        if max_size == 4:
            if 1 <= self.y <= 2:
                if 1 <= self.x <= 2:
                    return 1
                if 3 <= self.x <= 4:
                    return 2
            if 3 <= self.y <= 4:
                if 1 <= self.x <= 2:
                    return 3
                if 3 <= self.x <= 4:
                    return 4

        if max_size == 9:
            if 1 <= self.y <= 3:
                if 1 <= self.x <= 3:
                    return 1
                if 4 <= self.x <= 6:
                    return 2
                if 7 <= self.x <= 9:
                    return 3
            if 4 <= self.y <= 6:
                if 1 <= self.x <= 3:
                    return 4
                if 4 <= self.x <= 6:
                    return 5
                if 7 <= self.x <= 9:
                    return 6
            if 7 <= self.y <= 9:
                if 1 <= self.x <= 3:
                    return 7
                if 4 <= self.x <= 6:
                    return 8
                if 7 <= self.x <= 9:
                    return 9

        if max_size == 16:
            if 1 <= self.y <= 4:
                if 1 <= self.x <= 4:
                    return 1
                if 5 <= self.x <= 8:
                    return 2
                if 9 <= self.x <= 12:
                    return 3
                if 13 <= self.x <=16:
                    return 4
            if 5 <= self.y <= 8:
                if 1 <= self.x <= 4:
                    return 5
                if 5 <= self.x <= 8:
                    return 6
                if 9 <= self.x <= 12:
                    return 7
                if 13 <= self.x <= 16:
                    return 8
            if 9 <= self.y <= 12:
                if 1 <= self.x <= 4:
                    return 9
                if 5 <= self.x <= 8:
                    return 10
                if 9 <= self.x <= 12:
                    return 11
                if 13 <= self.x <= 16:
                    return 12
            if 13 <= self.y <= 16:
                if 1 <= self.x <= 4:
                    return 13
                if 5 <= self.x <= 8:
                    return 14
                if 9 <= self.x <= 12:
                    return 15
                if 13 <= self.x <= 16:
                    return 16