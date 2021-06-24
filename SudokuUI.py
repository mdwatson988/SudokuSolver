from Sudoku import Sudoku
from SudokuValue import SudokuValue


def user_input_query(sudoku_object, values_dictionary):
    while True:
        request_input = input("\nWould you like to add a value to the starting Sudoku board?\n"
                              "Press 'Y' to add a value or 'N' to continue: ")
        if request_input.upper() == "Y":
            get_and_add_user_value_input(sudoku_object, values_dictionary)
        elif request_input.upper() == "N":
            print("\nHere's your starting Sudoku board:\n")
            break
        else:
            print("Please press 'Y' to add another value or 'N' to continue.\n")


def get_and_add_user_value_input(sudoku_object, values_dictionary):
    while True:
        x_input = input("\nX coordinate (counting across from left): ")
        y_input = input("Y coordinate (counting down from top): ")
        value_input = input("Value: ")
        try:
            # convert inputs to int type
            x, y, value = int(x_input), int(y_input), int(value_input)
            # if inputs are appropriate, check values and then add value if no conflicts
            if 0 < x < 10 and 0 < y < 10 and 0 < value < 10:
                new_user_value = (SudokuValue(x, y, value))
                # check if value has any conflicts with existing values
                if sudoku_object.check_user_value(new_user_value, values_dictionary):
                    return sudoku_object.add_value(new_user_value, values_dictionary)
            else:
                print("\nPlease input coordinates and values no lower than 1 and no greater than 9.")
        except ValueError:
            print("\nPlease input whole numbers no lower than 1 and no greater than 9 for coordinates and values.")


def create_values_dictionary(sudoku_object):
    # value dictionary contains unused values in column/row/box and used coordinates to not be used again
    # values added to dictionary lists already so solver function can pop them out and use them
    # coords not added to dictionary until used. Coords just used to check if location already has a value
    value_dict = {}
    for x in range(1, sudoku_object.max_size):
        column = "x_" + str(x)
        value_dict[column] = set()
        for i in range(1, sudoku_object.max_size + 1):
            value_dict[column].add(i)
    for y in range(1, sudoku_object.max_size + 1):
        row = "y_" + str(y)
        value_dict[row] = set()
        for i in range(1, sudoku_object.max_size + 1):
            value_dict[row].add(i)
    for box in range(1, sudoku_object.max_size + 1):
        box_name = "box_" + str(box)
        value_dict[box_name] = set()
        for i in range(1, sudoku_object.max_size + 1):
            value_dict[box_name].add(i)
    value_dict["coords"] = set()
    return value_dict


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
    # create dictionary for used values
    current_values_dictionary = create_values_dictionary(sudoku)
    # add beginning sudoku values
    user_input_query(sudoku, current_values_dictionary)
    print(sudoku)
    break
