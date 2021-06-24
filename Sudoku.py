from SudokuTreeNode import SudokuTreeNode


class Sudoku:
    # will pass a list of SudokuValue objects. Will also pass a max size for edges/values
    def __init__(self, max_size):
        self.max_size = max_size
        self.left_to_fill = self.max_size ** 2
        # tree envisioned with root at top, root has 9 children as row 1, columns 1-9. Each column (initial child) then
        # has remaining rows built as children straight down
        # columns x coordinates, rows y coordinates
        self.root = SudokuTreeNode(0, 0, "root")  # root tree node will not contain a sudoku grid value
        # add initial column of children
        for column in range(1, self.max_size + 1):
            self.root.add_child(SudokuTreeNode(column, 1))  # added row 1, columns 1 through max size
        # populate the row for each column node just added, creating a 9x9 grid currently without values
        for child in self.root.children:
            row_list = [child]
            while row_list:
                current_child = row_list.pop()
                next_row = current_child.y + 1
                if next_row <= 9:  # keep adding children until the child on 9th row created
                    current_child.add_child(SudokuTreeNode(current_child.x, next_row))
                    row_list.append(current_child.children[0])

    def __repr__(self):
        # traverse tree. Create dict with row numbers as keys and node value as value, put results together
        nodes_to_visit = [self.root]
        grid_dictionary = {}
        for y in range(1, self.max_size + 1):
            grid_dictionary[y] = []  # create empty list to hold values across that row
        while len(nodes_to_visit) > 0:
            current_node = nodes_to_visit.pop(0)  # take first node from visit list to ensure correct order
            current_row = current_node.y
            if current_row != 0:  # don't add root node value
                if current_node.value:
                    grid_dictionary[current_row].append(current_node.value)  # add the sudoku value to the list
                else:
                    grid_dictionary[current_row].append("-")
            # initially all children of root added to call stack so row 1 is added to dictionary. After each value is
            # added, it's child is put to end of call stack, ensuring values added in correct order
            nodes_to_visit += current_node.children
        # create grid of string characters to display the sudoku board
        grid_string = "\n"
        counter = 1
        for y in grid_dictionary.keys():
            for number in grid_dictionary[y]:
                if counter < self.max_size:
                    grid_string += (str(number) + "  ")
                    counter += 1
                else:
                    grid_string += (str(number) + "\n")
                    counter = 1
        return grid_string

    # function alerts user if manually entered value has conflict
    def check_user_value(self, sudoku_value_object, values_dictionary):
        x = sudoku_value_object.x
        y = sudoku_value_object.y
        box = sudoku_value_object.box
        coords = sudoku_value_object.coords
        value = sudoku_value_object.value
        # check to ensure no value at location and value does not match a value already in same row, column, or box
        if coords in values_dictionary["coords"]:  # check if those coords have already been used
            print(f"\nSorry, there's already at a value at {coords}.")
            return False
        # check if column, row, or box have been used
        elif value not in values_dictionary["x_" + str(x)]:
            print(f"\nSorry, there's already a {value} in Column {x}.")
            return False
        elif value not in values_dictionary["y_" + str(y)]:
            print(f"\nSorry, there's already a {value} in Row {y}.")
            return False
        elif value not in values_dictionary["box_" + str(box)]:
            print(f"\nSorry, there's already a {value} in Box {box}.")
            return False
        # otherwise return True
        else:
            return True

    # silently checks value for solver function
    def check_value(self, sudoku_value_object, values_dictionary):
        x = sudoku_value_object.x
        y = sudoku_value_object.y
        box = sudoku_value_object.box
        coords = sudoku_value_object.coords
        value = sudoku_value_object.value
        # check to ensure no value at location and value does not match a value already in same row, column, or box
        if coords in values_dictionary["coords"]:  # check if those coords have already been used
            return False
        # check if column, row, or box have been used
        elif value not in values_dictionary["x_" + str(x)] or value not in values_dictionary[
            "y_" + str(y)] or value not in values_dictionary["box_" + str(box)]:
            return False
        # otherwise return True
        else:
            return True

    # adds values to sudoku grid
    def add_value(self, sudoku_value_object, values_dictionary):
        x = sudoku_value_object.x
        y = sudoku_value_object.y
        box = sudoku_value_object.box
        coords = sudoku_value_object.coords
        value = sudoku_value_object.value
        # start search for correct node at first child node of correct column. subtract 1 from column for index
        current_child_list = [self.root.children[(x - 1)]]
        while current_child_list:
            current_child = current_child_list.pop()
            if current_child.y == y:
                # stop at node in correct row and add value then update all relevant values dictionary lists
                current_child.value = value
                self.left_to_fill -= 1
                values_dictionary["coords"].add(coords)
                values_dictionary["x_" + str(x)].remove(value)
                values_dictionary["y_" + str(y)].remove(value)
                values_dictionary["box_" + str(box)].remove(value)
            else:
                # otherwise go on to next child
                current_child_list.append(current_child.children[0])

    # removes incorrect values added by solver function
    def remove_value(self, sudoku_value_object, values_dictionary):
        x = sudoku_value_object.x
        y = sudoku_value_object.y
        box = sudoku_value_object.box
        coords = sudoku_value_object.coords
        value = sudoku_value_object.value
        # start search for correct node at first child node of correct column. subtract 1 from column for index
        current_child_list = [self.root.children[(x - 1)]]
        while current_child_list:
            current_child = current_child_list.pop()
            if current_child.y == y:
                # stop at node in correct row and add value then update all relevant values dictionary lists
                current_child.value = None
                self.left_to_fill += 1
                values_dictionary["coords"].remove(coords)
                values_dictionary["x_" + str(x)].add(value)
                values_dictionary["y_" + str(y)].add(value)
                values_dictionary["box_" + str(box)].add(value)
            else:
                # otherwise go on to next child
                current_child_list.append(current_child.children[0])

    # begin by going to first node without a value
    # get column, row, box information of node
    # user intersection set method to make set of values available in all 3 dictionary sets
    # append first value in intersection set, add value to list of values added by solver
    # go on to next value
    # if no items in intersection list, remove most recent value in values added list
    # try new values in intersection list
    # stop when left to fill == 0
    # figure it out. This is hard.
    def dfs_sudoku_solver(self, root, values_added=None):
        if values_added is None:
            values_added = []

    def dfs(self, root, target, path=()):
        path = path + (root,)

        if root.value == target:
            return path

        for child in root.children:
            path_found = self.dfs(child, target, path)

            if path_found is not None:
                return path_found

        return None
