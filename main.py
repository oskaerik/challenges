"""Main function for the sudoku solver"""
from parser import Parser
from solver import Solver


def main():
    """Main function"""
    parser = Parser("project_euler_96.txt")
    solver = Solver(parser.grids[4])
    solver.paint()

if __name__ == "__main__":
    main()
