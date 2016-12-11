"""Contains the Solver class"""
import copy


def solved(values):
    """Checks if a sudoku puzzle is solved or unsolvable, returns -1 if unsolvable, 1 if solved and 0 if not solved"""
    for u in values:
        if len(values[u]) < 1:
            return -1
        elif len(values[u]) > 1:
            return 0
    return 1


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

        # Solve the puzzle (if not already solved)
        if self.solve(self.values):
            self.paint(self.values)
        else:
            print("Critical error in solving")
            quit(1)

    def parse(self, lines):
        for r, line in enumerate(lines):
            for c, value in enumerate(line):
                if value != "0":
                    self.assign(self.values, self.letters[c] + self.numbers[r], value)

    def remove(self, values, key, value):
        """Removes a value from the list of possible values for a square"""
        # Do nothing if the value isn't there
        if value not in values[key]:
            return

        # Remove the value from the square
        values[key] = values[key].replace(value, "")

        # If the square only has one possible value, assign it
        if len(values[key]) == 1:
            self.assign(values, key, values[key])

        # Checks if there exists value that only can be in one place in the row, column or box
        for i in range(1, 10):
            self.single(values, self.rows, key, str(i))
            self.single(values, self.columns, key, str(i))
            self.single(values, self.boxes, key, str(i))

    def assign(self, values, key, value):
        """Assigns a value to a square"""
        # Do nothing if the value isn't there
        if value not in values[key]:
            return

        # Remove all other values from possible values
        remove = values[key].replace(value, "")
        for r in remove:
            self.remove(values, key, r)

        # Removes the value from the squares in the square's row, column and box
        for u in self.rows[key]:
            if not u == key:
                self.remove(values, u, value)
        for u in self.columns[key]:
            if not u == key:
                self.remove(values, u, value)
        for u in self.boxes[key]:
            if not u == key:
                self.remove(values, u, value)

    def single(self, values, dictionary, key, value):
        """Checks if there is only a single place a value can fit"""
        candidate = list()
        for u in dictionary[key]:
            if value in values[u]:
                candidate.append(u)
        if len(candidate) == 1 and len(values[candidate[0]]) > 1:
            self.assign(values, candidate[0], value)

    def paint(self, values):
        """Paints the grid in standard out"""
        for r, n in enumerate(self.numbers):
            if r % 3 == 0:
                print("-------------------------")
            print("|", end="")
            for c, l in enumerate(self.letters):
                if c % 3 == 0 and c != 0:
                    print(" |", end="")
                if len(values[l + n]) > 1:
                    print(" ?", end="")
                elif len(values[l + n]) < 1:
                    print(" X", end="")
                else:
                    print(" " + values[l + n], end="")
            print(" |")
        print("-------------------------")

    def solve(self, mother):
        """Solves the puzzle recursively"""
        if solved(mother) == 1:
            # If the puzzle is solved, return true
            return True
        elif solved(mother) == -1:
            # If the puzzle is unsolvable, return false
            return False

        # Find a square and a possible value
        find = self.find(mother)

        # Create a child and assign the possible value to the square
        child = copy.deepcopy(mother)
        self.assign(child, find[0], find[1])

        # Try to solve the child
        if self.solve(child):
            self.values = child
            return True
        else:
            self.remove(mother, find[0], find[1])
            return self.solve(mother)

    def find(self, values):
        """Find a square with more than one possible value and return the first as tuple"""
        for l in self.letters:
            for n in self.numbers:
                if len(values[l + n]) > 1:
                    return l + n, values[l + n][0]

"""
    def solve(self, mother):
        child = copy.deepcopy(mother)

        if solved(child):
            self.paint(child)
            quit(1)

        for l in self.letters:
            for n in self.numbers:
                if len(child[l + n]) > 1:
                    print("SOLVE assigning " + child[l + n][0] + " to " + l+n)
                    # Try assigning a possible value to a square
                    assign = child[l + n][0]
                    self.assign(child, l + n, child[l + n][0])
                    self.paint(child)

                    # If there is a unit with no possible values, reverse
                    for u in child:
                        if len(child[u]) < 1:
                            print("Contradiction on " + u + ", reverting " + assign + " on square " + l+n)
                            child = copy.deepcopy(mother)
                            self.remove(child, l + n, child[l + n][0])

                    # If all squares had possible values, solve the grandchild
                    self.solve(child)
"""
