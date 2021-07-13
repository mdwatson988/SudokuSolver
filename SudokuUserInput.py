class SudokuUserInput:
    def __init__(self, x, y, value, sudoku_object=None):
        self.x = x
        self.y = y
        self.value = value
        self.box = self.determine_box(sudoku_object)
        self.coords = (x, y)

    def __repr__(self):
        return f"Value object with value of {self.value} at {self.coords}"

    def determine_box(self, sudoku_object):
        if not sudoku_object:  # No sudoku object passed when using test puzzle
            max_size = 9
        else:
            max_size = sudoku_object.max_size

        # determines which box each node falls into for 1 to 9 pattern. Numbered from top-left, right then down
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
                if 13 <= self.x <= 16:
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
