class SudokuTreeNode:
    def __init__(self, row, column, value=None):
        self.value = value  # data
        self.children = []  # references to other nodes
        self.row = row
        self.column = column

    def __repr__(self):
        return f"{self.value} in Row {self.row} and Column {self.column}"

    def add_child(self, child_node):
        # creates parent-child relationship
        self.children.append(child_node)


    def print_path(path):
        # If path is None, no path was found
        if not path:
            print("No paths found!")

        # If a path was found, print path
        else:
            print("Path found:")
            for node in path:
                print(node.value)
