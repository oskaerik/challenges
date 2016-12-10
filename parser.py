"""Contains the Parser class"""


class Parser(object):
    """The Parser class parses a file with sudoku puzzles"""

    def __init__(self, path):
        """Constructor for the Parser class, reads the lines of the file into a list"""
        self.grids = list()

        with open(path) as file:
            lines = file.readlines()

        # Strip every grid of the \n signs and append to list grids
        for i in range(0, len(lines)//10):
            stripped = list()
            for l in lines[i*10+1:i*10+10]:
                stripped.append(l.replace("\n", ""))
            self.grids.append(stripped)