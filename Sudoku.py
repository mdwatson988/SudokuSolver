from SudokuTreeNode import SudokuTreeNode
from math import sqrt


class Sudoku:
    def __init__(self, max_size):
        self.max_size = max_size  # pass a max size for edge length/values
        self.starting_board = [[], max_size] # list in index 0 holds sudoku user inputs, index 1 holds starting size
        self.values_added = False # set to True after first user value added - prevents solver from trying blank puzzle
        self.left_to_fill = self.max_size ** 2  # solver function stops when left_to_fill == 0
        self.unavailable_coords = set()  # used to check if location already has a value
        # value dictionary contains unused values in column/row/box and used coordinates to not be used again
        # values initially added to dictionary lists so solver function can compare whats left to be added to graph
        self.available_values_dictionary = {}
        for x in range(1, self.max_size + 1):
            column = "x_" + str(x)
            self.available_values_dictionary[column] = set()
            for i in range(1, self.max_size + 1):
                self.available_values_dictionary[column].add(i)
        for y in range(1, self.max_size + 1):
            row = "y_" + str(y)
            self.available_values_dictionary[row] = set()
            for i in range(1, self.max_size + 1):
                self.available_values_dictionary[row].add(i)
        for box in range(1, self.max_size + 1):
            box_name = "box_" + str(box)
            self.available_values_dictionary[box_name] = set()
            for i in range(1, self.max_size + 1):
                self.available_values_dictionary[box_name].add(i)
        # tree envisioned with root at top, root has 9 children as row 1, columns 1-9. Each column (initial child) then
        # has remaining rows built as children straight down
        # columns are x coordinates across from left, rows are y coordinates down from top
        self.root = SudokuTreeNode(self, 0, 0, "root")  # root tree node will not contain a sudoku grid value
        # add initial column of children
        for column in range(1, self.max_size + 1):
            self.root.add_child(SudokuTreeNode(self, column, 1))  # added row 1, columns 1 through max size
        # populate the row for each column node just added, creating a 9x9 grid currently without values
        for child in self.root.children:
            row_list = [child]
            while row_list:
                current_child = row_list.pop()
                next_row = current_child.y + 1
                if next_row <= self.max_size:  # keep adding children until the child on last row created
                    current_child.add_child(SudokuTreeNode(self, current_child.x, next_row))
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
        grid_string = "\n "
        y_counter = 1
        x_counter = 1
        box_size = int(sqrt(self.max_size))
        horizontal_line = ("-" * 3 * box_size) + (("|" + ("-" * 3 * box_size)) * (box_size - 1))
        for y in grid_dictionary.keys():
            for number in grid_dictionary[y]:
                if y_counter < self.max_size and y_counter % box_size != 0: # add value only
                    grid_string += (str(number) + "  ")
                    y_counter += 1
                # every 3 values that aren't the end of the puzzle, add vertical line for boxes
                elif y_counter < self.max_size and y_counter % box_size == 0:
                    grid_string += (str(number) + " | ")
                    y_counter += 1
                # once row is complete, go to new line.
                elif y_counter == self.max_size and x_counter % box_size != 0:
                    grid_string += (str(number) + f"\n ")
                    x_counter += 1
                    y_counter = 1
                # add a horizontal line for boxes under every 3 rows, except the last row
                elif y_counter == self.max_size and x_counter % box_size == 0 and x_counter < self.max_size:
                    grid_string += (str(number) + f"\n{horizontal_line}\n ")
                    x_counter += 1
                    y_counter = 1
                else:
                    grid_string += (str(number))
        return grid_string

    # function alerts user if manually entered value has conflict
    def check_user_value(self, sudoku_user_input_object):
        x = sudoku_user_input_object.x
        y = sudoku_user_input_object.y
        box = sudoku_user_input_object.box
        coords = sudoku_user_input_object.coords
        value = sudoku_user_input_object.value
        # check to ensure no value at location and value does not match a value already in same row, column, or box
        if coords in self.unavailable_coords:  # check if those coords have already been used
            print(f"\nSorry, there's already at a value at {coords}.")
            return "Location unavailable"
        # check if column, row, or box have been used
        elif value not in self.available_values_dictionary["x_" + str(x)]:
            print(f"\nSorry, there's already a {value} in Column {x}.")
            return False
        elif value not in self.available_values_dictionary["y_" + str(y)]:
            print(f"\nSorry, there's already a {value} in Row {y}.")
            return False
        elif value not in self.available_values_dictionary["box_" + str(box)]:
            print(f"\nSorry, there's already a {value} in Box {box}.")
            return False
        # otherwise return True
        else:
            return True

    # adds user input values to sudoku grid
    def add_user_value(self, sudoku_user_input_object):
        x = sudoku_user_input_object.x
        y = sudoku_user_input_object.y
        box = sudoku_user_input_object.box
        coords = sudoku_user_input_object.coords
        value = sudoku_user_input_object.value
        # start search for correct node at first child node of correct column. subtract 1 from column for index
        current_child_list = [self.root.children[(x - 1)]]
        while current_child_list:
            current_child = current_child_list.pop()
            if current_child.y == y:
                # stop at node in correct row and add value then update all relevant values dictionary lists
                current_child.value = value
                self.left_to_fill -= 1
                self.starting_board[0].append(sudoku_user_input_object)
                self.values_added = True # allows solver function to run when set to True
                self.unavailable_coords.add(coords)
                self.available_values_dictionary["x_" + str(x)].remove(value)
                self.available_values_dictionary["y_" + str(y)].remove(value)
                self.available_values_dictionary["box_" + str(box)].remove(value)
            else:
                # otherwise go on to next child
                current_child_list.append(current_child.children[0])

    def add_solver_value(self, target_node, target_value):
        target_node.value = target_value
        target_node.attempted_values.add(target_value)
        self.left_to_fill -= 1
        self.unavailable_coords.add(target_node.coords)
        self.available_values_dictionary["x_" + str(target_node.x)].remove(target_value)
        self.available_values_dictionary["y_" + str(target_node.y)].remove(target_value)
        self.available_values_dictionary["box_" + str(target_node.box)].remove(target_value)
        ### UNCOMMENT next two lines to see what's being added where and the state of the board at each step
        # print(f"Solver added {target_value} to {target_node.coords}")
        # print(self)

    # removes incorrect values added by solver function
    def remove_solver_value(self, target_node):
        value_removed = target_node.value
        target_node.value = None
        self.left_to_fill += 1
        self.unavailable_coords.remove(target_node.coords)
        self.available_values_dictionary["x_" + str(target_node.x)].add(value_removed)
        self.available_values_dictionary["y_" + str(target_node.y)].add(value_removed)
        self.available_values_dictionary["box_" + str(target_node.box)].add(value_removed)
        ### UNCOMMENT next two lines to see what's being removed where and the state of the board at each step
        # print(f"The solver remove value function removed {value_removed} from {target_node.coords}")
        # print(self)

    # Functions to determine next target for solver function
    # first determine which column/row/box has fewest empty values - nearly finished means few possible values
    def dfs_column_or_row_or_box_target_finder(
            self):  # values dictionary keeps track of spots where there is NOT a value
        current_target_string = None
        current_target_number_to_beat = self.max_size
        available_values_dictionary_items = self.available_values_dictionary.items()
        for item in available_values_dictionary_items:
            number_left_to_fill = len(item[1])  # number of values left in the column/row/box
            if number_left_to_fill == 0:  # if none left to fill, skip this column/box/row
                continue
            else:
                if number_left_to_fill < current_target_number_to_beat:  # find shortest list
                    current_target_string = item[0]
                    current_target_number_to_beat = number_left_to_fill
        if current_target_string:  # dummy check to make sure a target was found
            # print(f"Column/row/box target finder found {current_target_string}")
            return current_target_string
        else:
            print("Column or row or box finder function didn't find a value \n")
            return None

    # target node is first node with empty value in target row/column/box
    def dfs_target_node_finder(self):
        target_column_or_row_or_box_string = self.dfs_column_or_row_or_box_target_finder()
        if target_column_or_row_or_box_string:  # column or row or box target finder returns None if unsuccessful
            # first determine if targeting a column, row, or box
            if target_column_or_row_or_box_string[0] == "x":  # if target is a column
                x = int(target_column_or_row_or_box_string[2])  # get column number
                # print(f"target column number: {x}")
                root_children_copy = self.root.children.copy()
                current_column_child_list = [root_children_copy[x - 1]]  # check for first empty value in correct column
                while current_column_child_list:
                    current_child = current_column_child_list.pop()
                    if not current_child.value:
                        target_node = current_child
                        # print(f"Target node found: {target_node.coords}")
                        return target_node
                    else:
                        if current_child.children:
                            current_column_child_list.append(current_child.children[0])
            elif target_column_or_row_or_box_string[0] == "y":  # if target==row, search whole tree for 1st empty value
                y = int(target_column_or_row_or_box_string[2])  # get row number
                # print(f"target row number: {y}")
                child_list = self.root.children.copy()
                while child_list:
                    current_child = child_list.pop(0)
                    if current_child.y == y and not current_child.value:
                        target_node = current_child
                        # print(f"Target node found: {target_node.coords}")
                        return target_node
                    elif current_child.y == y and current_child.value:
                        continue  # move on to next column once row has been checked
                    else:  # otherwise add next child in that column to front of list
                        if current_child.children:
                            child_list.insert(0, current_child.children[0])
            elif target_column_or_row_or_box_string[0] == "b":  # if target is a box
                box = int(target_column_or_row_or_box_string[4])  # get box number
                # print(f"target box number: {box}")
                child_list = self.root.children.copy()
                while child_list:
                    current_child = child_list.pop(0)
                    if current_child.box == box and not current_child.value:
                        target_node = current_child
                        # print(f"Target node found: {target_node.coords}")
                        return target_node
                    else:  # otherwise add next child in that column to front of list
                        if current_child.children:
                            child_list.insert(0, current_child.children[0])
            else:
                print(
                    f"There was a problem with the target node finder for " + target_column_or_row_or_box_string + "\n")
        # print("No target node found")
        return None

    # possible node values are all values not yet placed in that row, column, or box
    # will use first value in list of possible node values that isn't in the attempted_values list for this iteration
    def dfs_determine_target_node_value(self, target_node):
        # print(f"Target node is: {target_node}")
        possible_column_values = self.available_values_dictionary["x_" + str(target_node.x)]
        possible_row_values = self.available_values_dictionary["y_" + str(target_node.y)]
        possible_box_values = self.available_values_dictionary["box_" + str(target_node.box)]
        # possible node values is the set of values that are all listed in the possible column, row, and box values
        possible_node_values = possible_column_values.intersection(possible_row_values, possible_box_values)
        # print(f"Possible node values are {possible_node_values} and values already attempted are {target_node.attempted_values}")
        if possible_node_values and possible_node_values != target_node.attempted_values:  # if not all possible values have been attempted
            # print("There are possible node values not yet attempted")
            for value in possible_node_values:
                if value not in target_node.attempted_values:  # attempt to use first value not yet attempted
                    # print(f"Will attempt to place a {value} at {target_node.coords}")
                    return value  # return the Sudoku target object
        # if all possible values for target have been attempted, solver f'n must remove the node previous
        elif possible_node_values and possible_node_values == target_node.attempted_values:
            # to target and try new value there. Also must clear the attempted values list for target node
            # print("Possible nodes found but all have been attempted")
            return "All potential values attempted"
        # if unable to find any possible node values, previous node will need to be removed by solver
        else:
            # print("No value possible")
            return "No value possible"

    def dfs_sudoku_solver(self, nodes_with_values_added_by_solver=None):
        if nodes_with_values_added_by_solver is None:  # keep track of values added so incorrect values can be removed
            nodes_with_values_added_by_solver = []

        # base case
        if self.left_to_fill == 0:
            print("\nYour Sudoku puzzle has been solved!")
            return self  # printing the solved sudoku object will display the completed puzzle

        target_node = self.dfs_target_node_finder()  # returns None if no appropriate target node could be found

        if not target_node:  # if no target node found by finder function, placed values need to be removed and replaced
            # print("No target node was found. Will have to remove values and try new ones")
            most_recent_solver_node = nodes_with_values_added_by_solver.pop()
            self.remove_solver_value(most_recent_solver_node)  # clear value from most recent placement
            # check to see if another value can be placed at that location
            node_target_value = self.dfs_determine_target_node_value(most_recent_solver_node)
            # determine target node value returns an int type value if one found, otherwise returns a string detailing what went wrong
            if type(node_target_value) == int:  # if another value can be tried at that location, add it and continue function
                # print(f"found another possible node for {most_recent_solver_node.coords}")
                self.add_solver_value(most_recent_solver_node, node_target_value)
                # update nodes added by solver list
                nodes_with_values_added_by_solver.append(most_recent_solver_node)
                return self.dfs_sudoku_solver(nodes_with_values_added_by_solver)
            else:  # if no more values left to try at current location, clear attempted values list and remove value
                # from next previous node, run function again
                #  print("didn't find possible node values that haven't been attempted")
                most_recent_solver_node.attempted_values.clear()
                # print(f"cleared attempted values for {most_recent_solver_node}, attempted values are now {most_recent_solver_node.attempted_values}")
                previously_placed_node_that_needs_new_value = nodes_with_values_added_by_solver.pop()
                self.remove_solver_value(previously_placed_node_that_needs_new_value)
                # node could have more available values or not, just run function again
                return self.dfs_sudoku_solver(
                    nodes_with_values_added_by_solver)

        # if target node was found by finder function, determine value to try for that node
        target_value = self.dfs_determine_target_node_value(target_node)

        if target_value == "No value possible":  # if no value possible at target node, remove prev node and try new
            # value at that location
            most_recent_solver_node = nodes_with_values_added_by_solver.pop()
            self.remove_solver_value(most_recent_solver_node)
            return self.dfs_sudoku_solver(nodes_with_values_added_by_solver)  # recursively run function

        # if all values have been attempted at the target node, clear attempted values list for target node, then
        # remove node prev to target and try new value there
        elif target_value == "All potential values attempted":
            target_node.attempted_values.clear()
            # print(f"Cleared attempted values list at {target_node.coords}")
            next_solver_node_to_remove = nodes_with_values_added_by_solver.pop()
            self.remove_solver_value(next_solver_node_to_remove)
            return self.dfs_sudoku_solver(nodes_with_values_added_by_solver)

        else:  # if target node & value found, add the value to that node and update nodes added by solver list
            self.add_solver_value(target_node, target_value)
            nodes_with_values_added_by_solver.append(target_node)
            return self.dfs_sudoku_solver(nodes_with_values_added_by_solver)
