class SudokuUserInput:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.box = self.determine_box()
        self.coords = (x, y)

    def __repr__(self):
        return f"Value object with value of {self.value} at {self.coords}"

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