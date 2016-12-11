"""Main function for the sudoku solver"""
from parser import Parser
from solver import Solver


def main():
    """Main function"""
    parser = Parser("project_euler_96.txt")

    sum = 0
    for g in parser.grids:
        sum += int(Solver(g).values["A1"]+Solver(g).values["B1"]+Solver(g).values["C1"])
    print(str(sum))

if __name__ == "__main__":
    main()
