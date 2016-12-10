"""Contains the Solver class"""


class Solver(object):
    """The Solver class handles solving of the sudoku puzzle"""

    def __init__(self, lines):
        """Constructor, creates the collection of rows, columns, boxes and the values"""
        self.letters = "ABCDEFGHI"
        self.numbers = "123456789"

        # Create rows
        self.rows = dict()
        for l in self.letters:
            row = list()
            for n in self.numbers:
                row.append(l + n)
            for u in row:
                self.rows[u] = row

        # Create columns
        self.columns = dict()
        for n in self.numbers:
            column = list()
            for l in self.letters:
                column.append(l + n)
            for u in column:
                self.columns[u] = column

        # Create boxes
        self.boxes = dict()
        for r in range(0, 3):
            for c in range(0, 3):
                box = list()
                for l in range(0, 3):
                    for n in range(0, 3):
                        box.append(self.letters[l+3*r] + self.numbers[n+3*c])
                for u in box:
                    self.boxes[u] = box

        # Create values
        self.values = dict()
        for l in self.letters:
            for n in self.numbers:
                self.values[l + n] = "123456789"

        # Parse the input lines
        self.parse(lines)

    def parse(self, lines):
        for r, line in enumerate(lines):
            for c, value in enumerate(line):
                if value != "0":
                    self.assign(self.letters[c] + self.numbers[r], value)


    def remove(self, key, value):
        """Removes a value from the list of possible values for a unit"""
        # Do nothing if the value isn't there
        if value not in self.values[key]:
            return

        # Remove the value from the unit
        self.values[key] = self.values[key].replace(value, "")

        # If the unit only has one possible value, assign it
        if len(self.values[key]) == 1:
            self.assign(key, self.values[key])

        # Checks if there exists value that only can be in one place in the row, column or box
        for i in range(1, 10):
            self.single(self.rows, key, str(i))
            self.single(self.columns, key, str(i))
            self.single(self.boxes, key, str(i))

        # Asserts that every unit in the grid has at least one possible value
        # !This is to be fixed when implementing recursion!
        for u in self.values:
            assert (len(self.values[u]) > 0)

    def assign(self, key, value):
        """Assigns a value to a unit"""
        # Do nothing if the value isn't there
        if value not in self.values[key]:
            return

        # Remove all other values from possible values
        remove = self.values[key].replace(value, "")
        for r in remove:
            self.remove(key, r)

        # Removes the value from the units in the unit's row, column and box
        for u in self.rows[key]:
            if not u == key:
                self.remove(u, value)
        for u in self.columns[key]:
            if not u == key:
                self.remove(u, value)
        for u in self.boxes[key]:
            if not u == key:
                self.remove(u, value)

    def single(self, dictionary, key, value):
        """Checks if there is only a single place a value can fit"""
        candidate = list()
        for u in dictionary[key]:
            if value in self.values[u]:
                candidate.append(u)
        if len(candidate) == 1 and len(self.values[candidate[0]]) > 1:
            self.assign(candidate[0], value)

    def paint(self):
        """Paints the grid in standard out"""
        for r, n in enumerate(self.numbers):
            if r % 3 == 0:
                print("-------------------------")
            print("|", end="")
            for c, l in enumerate(self.letters):
                if c % 3 == 0 and c != 0:
                    print(" |", end="")
                if len(self.values[l + n]) > 1:
                    print(" ?", end="")
                else:
                    print(" " + self.values[l + n], end="")
            print(" |")
        print("-------------------------")