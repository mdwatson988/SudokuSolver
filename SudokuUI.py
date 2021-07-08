from Sudoku import Sudoku
from SudokuUserInput import SudokuUserInput


def user_input_query(sudoku_object):
    while True:
        request_input = input("\nWould you like to add a value to the starting Sudoku board?\n"
                              "Press 'Y' to add a value or 'N' to continue: ")
        if request_input.upper() == "Y":
            get_and_add_user_value_input(sudoku_object)
        elif request_input.upper() == "N":
            print("\nHere's your starting Sudoku board:\n")
            break
        else:
            print("Please press 'Y' to add another value or 'N' to continue.\n")


def get_and_add_user_value_input(sudoku_object):
    while True:
        x_input = input("\nX coordinate (counting across from left): ")
        y_input = input("Y coordinate (counting down from top): ")
        value_input = input("Value: ")
        try:
            # convert inputs to int type
            x, y, value = int(x_input), int(y_input), int(value_input)
            # if inputs are appropriate, check values and then add value if no conflicts
            if 0 < x < 10 and 0 < y < 10 and 0 < value < 10:
                new_user_value = (SudokuUserInput(x, y, value))
                # check if value has any conflicts with existing values
                if sudoku_object.check_user_value(new_user_value):
                    return sudoku_object.add_user_value(new_user_value)
            else:
                print("\nPlease input coordinates and values no lower than 1 and no greater than 9.")
        except ValueError:
            print("\nPlease input whole numbers no lower than 1 and no greater than 9 for coordinates and values.")


def add_start_values_for_testing(sudoku_object, list_of_user_input_objects):
    print("\nHere's the starting input for the test puzzle:")
    for test_input in list_of_user_input_objects:
        sudoku_object.add_user_value(test_input)
        # print(sudoku_object)


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

# outer loop that keeps program running
while True:
    # instantiate Sudoku grid object
    sudoku = Sudoku(9)
    # add beginning sudoku values
    # user_input_query(sudoku)
    add_start_values_for_testing(sudoku, test_list)
    print(sudoku)
    solved = sudoku.dfs_sudoku_solver()
    print(solved)
    break
