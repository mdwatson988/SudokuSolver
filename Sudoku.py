from SudokuTreeNode import SudokuTreeNode


class Sudoku:
    # will pass a list of SudokuValue objects. When creating each node will check to see if coords are correct
    # if correct add the value for that space instead of None. Will also pass a max size for edges/values
    def __init__(self, max_size, sudoku_value_list):
        self.max_size = max_size
        
        # tree envisioned with root at top, root has 9 children as row 1, columns 1-9. Each column (initial child) then
        # has remaining rows built as children straight down
        self.root = SudokuTreeNode(0, 0, "root")  # root tree node will not contain a sudoku grid value
        # add initial column of children
        for column in range(1, 10):
            self.root.add_child(SudokuTreeNode(1, column))  # added row 1, columns 1-9
        # populate the row for each column node just added, creating a 9x9 grid currently without values
        for child in self.root.children:
            row_list = [child]
            while row_list:
                current_child = row_list.pop()
                next_row = current_child.row + 1
                if next_row <= 9: # keep adding children until the child on 9th row created
                    current_child.add_child(SudokuTreeNode(next_row, current_child.column))
                    row_list.append(current_child.children[0])

    def __repr__(self):
        # traverse tree. Create dict with row numbers as keys and node value as value, put results together
        nodes_to_visit = [self.root]
        grid_dictionary = {}
        for row in range(1, 10):
            grid_dictionary[row] = [] # create empty list to hold values across that row
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop(0)  # take first node from visit list to ensure correct order
            if current_node.row != 0:  # don't add root node value
                if current_node.value:
                    grid_dictionary[current_node.row].append(current_node.value)  # add the sudoku value to the list
                else:
                    grid_dictionary[current_node.row].append("X")
            # initially all children of root added to call stack so row 1 is added to dictionary. After each value is
            # added, it's child is put to end of call stack, ensuring values added in correct order
            nodes_to_visit += current_node.children
        grid_string = "\n"
        for i in grid_dictionary.keys():
            grid_string += str(grid_dictionary[i]) + "\n"
        return grid_string

    def dfs(self, root, target, path=()):
        path = path + (root,)

        if root.value == target:
            return path

        for child in root.children:
            path_found = self.dfs(child, target, path)

            if path_found is not None:
                return path_found

        return None

    def add_test_values(self):
        grid_value = 0
        nodes_to_visit = [self.root]
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop(0)
            current_node.value = grid_value
            grid_value += 1
            if grid_value > 9:
                grid_value = 1
            nodes_to_visit += current_node.children


test = Sudoku()
test.add_test_values()
print(test)
