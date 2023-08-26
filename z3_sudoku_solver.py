"""
Author: Luke Marshall
Description: Sudoku solver in Z3Py.
"""

from z3 import *

'''# create the sudoku board
board = [ Int("x_%s_%s" % (i+1, j+1)) for j in range(9) for i in range(9) ]

#Constrain the values in each square to be an integer between 1 and 9 inclusive
cell_constraint = [ And(0 < board[i][j], board[i][j] < 10) for i in range(9)
                    for j in range(9) ]

row_constraint = [ Distinct(board[i]) for i in range(9) ]
col_constraint = [ Distinct(board[j])]

def translate_puzzle(puzzle: str) -> dict:
    # check the puzzle is not within quotes
    assert puzzle[0] != "'" and puzzle[0] != '"', "Entered puzzle must not be enclosed in quotes or any other character."
    # check puzzle has necessary rows and columns
    assert len(puzzle) == 81, "Puzzles must contain 9 rows of values, 81 values in the string."
    puzzle = puzzle.replace('.', '0')
    
    # translate the puzzle into a dict with coordinates as keys and a number 1-9 or
    # a string of possible numbers as values
    rows = 'ABCDEFGHI'
    all_possible_values = '123456789'
    values = {}
    position = 0
    for i in range(9):
        for j in range(9):
            if int(puzzle[position]):
                values[('').join([rows[i], str(j+1)])] = puzzle[position]
            else:
                values[('').join([rows[i], str(j+1)])] = all_possible_values
            position += 1
    
    return values'''

def build_rows() -> list[list]:
    rows = [[ Int("x_%s_%s" % (i+1, j+1)) 
             for j in range(9)] for i in range(9) ]
    return rows

def build_cols() ->list[list]:
    cols = [[ Int("x_%s_%s" % (j+1, i+1)) 
             for j in range(9)] for i in range(9) ]
    return cols


def main():
    ''''in_put = input("""Please enter a Sudoku puzzle.
                   The puzzle must be in the form of a string of 81 values.
                   The given values must be placed in their original spots
                   with empty squares represented by zero ('0') or ('.').
                   Ex: 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
                   Ex: 400000805030000000000700000020000060000080400000010000000603070500200000104000000
                   Do not place quotes or any other characters around the entered string.
                   If the puzzle does not have one unique solution (e.g. at least 17 squares with given values
                   or at least 8 different given values at the start), it will be considered unsolvable.
                   Please enter your puzzle here: """)'''
    print(build_rows())

if __name__ == '__main__':
    main()