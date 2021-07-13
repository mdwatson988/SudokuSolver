from Sudoku import Sudoku
from SudokuUserInput import SudokuUserInput
from files import *

test_list = [(SudokuUserInput(1, 1, 5)), (SudokuUserInput(2, 1, 3)), (SudokuUserInput(5, 1, 7)), (
    SudokuUserInput(1, 2, 6)), (SudokuUserInput(4, 2, 1)), (SudokuUserInput(5, 2, 9)), (
                 SudokuUserInput(6, 2, 5)), (SudokuUserInput(2, 3, 9)), (SudokuUserInput(3, 3, 8)), (
                 SudokuUserInput(8, 3, 6)), (SudokuUserInput(1, 4, 8)), (SudokuUserInput(5, 4, 6)), (
                 SudokuUserInput(9, 4, 3)), (SudokuUserInput(1, 5, 4)), (SudokuUserInput(4, 5, 8)), (
                 SudokuUserInput(6, 5, 3)), (SudokuUserInput(9, 5, 1)), (SudokuUserInput(1, 6, 7)), (
                 SudokuUserInput(5, 6, 2)), (SudokuUserInput(9, 6, 6)), (SudokuUserInput(2, 7, 6)), (
                 SudokuUserInput(7, 7, 2)), (SudokuUserInput(8, 7, 8)), (SudokuUserInput(9, 8, 5)), (
                 SudokuUserInput(5, 9, 8)), (SudokuUserInput(8, 9, 7)), (SudokuUserInput(9, 9, 9)), (
                 SudokuUserInput(4, 8, 4)), (SudokuUserInput(5, 8, 1)), (SudokuUserInput(6, 8, 9))]


def set_starting_board(sudoku_object, previous_board):
    while True:
        starting_board_input = input(
            "\nWould you like to see the solution to a new starting board, the previous starting board, or the test board?\n"
            "Press 'N' for a new board, 'P' for the previous board, or 'T' for the test board: ")

        if starting_board_input.upper() == "N":
            while True:
                user_input_method = input(
                    "\nWould you like to input an entire row, an entire column, or a single location?\n"
                    "Press 'R' for row, 'C' for column, or 'S' for single location.\n"
                    "Press 'V' to view the current state of the board. Press 'X' to stop adding values: ")
                if user_input_method.upper() == "R":
                    add_row_user_starting_input(sudoku_object)
                elif user_input_method.upper() == "C":
                    add_column_user_starting_input(sudoku_object)
                elif user_input_method.upper() == "S":
                    add_single_user_starting_input(sudoku_object)
                elif user_input_method.upper() == "V":
                    print(sudoku_object)
                elif user_input_method.upper() == "X":
                    break
                else:
                    print("\nInvalid input")
            break

        elif starting_board_input.upper() == "P":
            if previous_board and previous_board[1] == sudoku_object.max_size:
                for starting_value in previous_board[0]:
                    sudoku_object.add_user_value(starting_value)
                break
            elif previous_board:
                print(
                    "\nCurrent board size doesn't match previous board size. Please press 'N' to input your own starting board.")
            else:
                print(
                    "\nThere is not yet a saved starting board. Please press 'N' to input your own starting board.")

        elif starting_board_input.upper() == "T":
            if sudoku_object.max_size == 9:
                for test_input in test_list:
                    sudoku_object.add_user_value(test_input)
                break
            else:
                print("\nTest board requires a 9x9 grid. Please press 'N' to input your own starting board.")

        else:
            print("Please press 'N', 'P', or 'T'\n")


def add_row_user_starting_input(sudoku_object):
    max_size = sudoku_object.max_size
    while True:
        row_input = input("\nPlease input the row number you want to fill in, counting from top down: ")
        try:
            row_number = int(row_input)
            if 0 < row_number <= max_size:  # check for valid row number
                print("\n")
                for column in range(1, max_size + 1):  # start adding a value for each column in that row
                    if (column, row_number) in sudoku_object.unavailable_coords:  # skip locations with values
                        print(f"There is already a value in row {row_number}, column {column}.")
                    else:
                        while True:
                            value_input = input(
                                f"Input the value for row {row_number}, column {column} or press 'X' to skip this location: ")
                            if value_input.upper() == "X":
                                break
                            else:
                                try:
                                    value = int(value_input)
                                    if 0 < value <= max_size:
                                        new_user_value = SudokuUserInput(column, row_number, value, sudoku_object)
                                        # ensure value entered is a valid entry
                                        check_value_results = sudoku_object.check_user_value(new_user_value)
                                        if check_value_results:  # if valid entry, add value to sudoku object
                                            sudoku_object.add_user_value(new_user_value)
                                            break
                                        else:
                                            print(
                                                f"\nYou input a non-valid value at column {column}. Please try again.")
                                    else:
                                        print(f"\nPlease input a value no lower than 1 and no greater than {max_size}.")
                                except ValueError:
                                    print(
                                        f"\nPlease input a whole number no lower than 1 and no greater than {max_size}.")
                break
            else:
                print(f"\nPlease input a row number no lower than 1 and no greater than {max_size}.")
        except ValueError:
            print(f"\nPlease input a whole number no lower than 1 and no greater than {max_size}.")


def add_column_user_starting_input(sudoku_object):
    max_size = sudoku_object.max_size
    while True:
        column_input = input("\nPlease input the column number you want to fill in, counting from left to right: ")
        try:
            column_number = int(column_input)
            if 0 < column_number <= max_size:  # check for valid column number
                print("\n")
                for row in range(1, max_size + 1):  # start adding a value for each row in that column
                    if (column_number, row) in sudoku_object.unavailable_coords:  # skip locations with values
                        print(f"There is already a value in column {column_number}, row {row}.")
                    else:
                        while True:
                            value_input = input(
                                f"Input the value for column {column_number}, row {row} or press 'X' to skip this location: ")
                            if value_input.upper() == "X":
                                break
                            else:
                                try:
                                    value = int(value_input)
                                    if 0 < value <= max_size:
                                        new_user_value = SudokuUserInput(column_number, row, value, sudoku_object)
                                        # ensure value entered is a valid entry
                                        check_value_results = sudoku_object.check_user_value(new_user_value)
                                        if check_value_results:  # if valid entry, add value to sudoku object
                                            sudoku_object.add_user_value(new_user_value)
                                            break
                                        else:
                                            print(f"\nYou input a non-valid value at row {row}. Please try again.")
                                    else:
                                        print(f"\nPlease input a value no lower than 1 and no greater than {max_size}.")
                                except ValueError:
                                    print(
                                        f"\nPlease input a whole number no lower than 1 and no greater than {max_size}.")
                break
            else:
                print(f"\nPlease input a column number no lower than 1 and no greater than {max_size}.")
        except ValueError:
            print(f"\nPlease input a whole number no lower than 1 and no greater than {max_size}.")


def add_single_user_starting_input(sudoku_object):
    max_size = sudoku_object.max_size
    while True:
        x_input = input("\nX coordinate (counting across from left): ")
        y_input = input("Y coordinate (counting down from top): ")
        if (x_input, y_input) in sudoku_object.unavailable_coords:
            print(f"\nThere's already a value at ({x_input},{y_input}).")
        else:
            value_input = input("Value: ")
            try:
                # convert inputs to int type
                x, y, value = int(x_input), int(y_input), int(value_input)
                # if inputs are appropriate, check values and then add value if no conflicts
                if 0 < x <= max_size and 0 < y <= max_size and 0 < value <= max_size:
                    new_user_value = SudokuUserInput(x, y, value, sudoku_object)
                    # check if value has any conflicts with existing values
                    if sudoku_object.check_user_value(new_user_value):
                        return sudoku_object.add_user_value(new_user_value)
                else:
                    print(f"\nPlease input coordinates and values no lower than 1 and no greater than {max_size}.")
            except ValueError:
                print(
                    f"\nPlease input whole numbers no lower than 1 and no greater than {max_size} for coordinates and "
                    f"values.")


def set_start_size():
    while True:
        start_size_input = input(
            "\nWould you like a 4x4, 9x9, or 16x16 sudoku puzzle solved? Please press '9' to use the test board."
            "\nPress '4', '9', or '16': ")
        try:
            start_size = int(start_size_input)
            if start_size == 4 or start_size == 9 or start_size == 16:
                return start_size
            else:
                print("\nPlease enter '4' for a 4x4 grid, '9' for a 9x9 grid, or '16' for a 16x16 grid.")
        except ValueError:
            print("\nPlease enter only the whole numbers '4', '9', or '16'.")


def save_starting_board(sudoku_object, save_file_path):
    while True:
        save_current_sudoku_object_input = input(
            "\nWould you like to save the starting board to a .txt file for later access?"
            " Press 'Y' for Yes or 'N' for No: ")
        # if user wants to save the results
        if save_current_sudoku_object_input.upper() == "Y":
            # open existing txt file using path from files.py
            text_file = open(save_file_path, 'a')
            # write the results string to a new line on the file
            start_board_save_string = f"\nStarting board: {sudoku_object}\n"
            text_file.write(start_board_save_string)
            # close the file then break out of loop
            text_file.close()
            break
        elif save_current_sudoku_object_input.upper() == "N":
            break
        else:
            print('Press "Y" to save your starting board or "N" to skip.\n')


def save_solved_board(sudoku_object, save_file_path):
    while True:
        save_current_sudoku_object_input = input(
            "\nWould you like to save the solved board to a .txt file for later access?"
            " Press 'Y' for Yes or 'N' for No: ")
        # if user wants to save the results
        if save_current_sudoku_object_input.upper() == "Y":
            # open existing txt file using path from files.py
            text_file = open(save_file_path, 'a')
            # write the results string to a new line on the file
            solved_board_save_string = f"\nSolved board: {sudoku_object}\n"
            text_file.write(solved_board_save_string)
            # close the file then break out of loop
            text_file.close()
            break
        elif save_current_sudoku_object_input.upper() == "N":
            break
        else:
            print('Press "Y" to save your starting board or "N" to skip.\n')


# Begin the program
print("\n\n******************************")
print("**************  **************")
print("**********  SUDOKU  **********")
print("**********  PUZZLE  **********")
print("**********  SOLVER  **********")
print("**************  **************")
print("******************************")
print("\nWelcome to the Sudoku Puzzle Solver! This tool allows you to input a starting Sudoku board and view the "
      "solved puzzle.\n")
print("Time to get started with your first puzzle!")

previous_starting_board = None

# outer loop that keeps program running
while True:
    sudoku = Sudoku(set_start_size())  # instantiate a new Sudoku object
    while True:  # this loops ensures values have been added before solver starts
        set_starting_board(sudoku, previous_starting_board)  # add beginning sudoku values
        if sudoku.values_added:
            previous_starting_board = sudoku.starting_board  # save most recent starting board
            print("\nHere's your starting board:")
            print(sudoku)  # show starting board to user
            save_starting_board(sudoku, save_file_path)
            sudoku.dfs_sudoku_solver()  # solve the puzzle
            print("\nHere's your solved puzzle:")
            print(sudoku)  # show solved puzzle
            save_solved_board(sudoku, save_file_path)
            break
        else:
            print("\nPlease add at least one value to the sudoku puzzle.")

    go_again_input = input(
        "\nWould you like to use the program again? Press 'N' to stop the program or any other key to continue: ")
    if go_again_input.upper() == "N":
        break
