"""
Author: Luke Marshall
Description: Sudoku solver in Z3Py.
"""

from z3 import *


def translate_puzzle(puzzle: str) -> list[list]:
    # check the puzzle is not within quotes
    assert puzzle[0] != "'" and puzzle[0] != '"', "Entered puzzle must not be enclosed in quotes or any other character."
    # check puzzle has necessary rows and columns
    assert len(puzzle) == 81, "Puzzles must contain 9 rows of values, 81 values in the string."
    puzzle = puzzle.replace('.', '0')
    
    # translate the puzzle into a dict with coordinates as keys and a number 1-9 or
    # a string of possible numbers as values
    values = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(int(puzzle[j]))
        values.append(row)
        puzzle = puzzle[9:]
    return values


def build_rows() -> list[list]:
    rows = [[ Int("x_%s_%s" % (i+1, j+1)) 
             for j in range(9)] for i in range(9) ]
    return rows


def build_cols() ->list[list]:
    columns = [[ Int("x_%s_%s" % (j+1, i+1)) 
             for j in range(9)] for i in range(9) ]
    return columns


def build_boxes() ->list[list]:
    row_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    boxes = []
    for iteration in range(3):
        squares = [[], [], []]
        for row_i in range(3):
            for col_i in range(9):
                if col_i < 3:
                    squares[0].append(Int('x_%s_%s' % (row_nums[row_i], col_i+1)))
                elif 2 < col_i < 6:
                    squares[1].append(Int('x_%s_%s' % (row_nums[row_i], col_i+1)))
                else:
                    squares[2].append(Int('x_%s_%s' % (row_nums[row_i], col_i+1)))
        for box in squares:
            boxes.append(box)
        del row_nums[:3]
    return boxes

def main():
    puzzle = input("""Please enter a Sudoku puzzle.
                   The puzzle must be in the form of a string of 81 values.
                   The given values must be placed in their original spots
                   with empty squares represented by zero ('0') or ('.').
                   Ex: 4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
                   Ex: 400000805030000000000700000020000060000080400000010000000603070500200000104000000
                   Do not place quotes or any other characters around the entered string.
                   If the puzzle does not have one unique solution (e.g. at least 17 squares with given values
                   or at least 8 different given values at the start), it will be considered unsolvable.
                   Please enter your puzzle here: """)
    # Create row, columns, and box unit arrays containing their respective squares
    s = Solver()
    rows = Array('rows', IntSort(), IntSort())
    columns = Array('columns', IntSort(), IntSort())
    boxes = Array('boxes', IntSort(), IntSort())
    rows = build_rows()
    columns = build_cols()
    boxes = build_boxes()

    # create and add constraint to limit the value of any square to 1-9
    range_constraint = [ And(0 < rows[i][j], rows[i][j] < 10) 
                        for j in range(9) for i in range(9) ]
    s.add(range_constraint)
    
    # create and add the constraints that any square is unique to those 
    # in its row, column, and box units
    rows_constraint = [ Distinct(rows[i]) for i in range(9) ]
    s.add(rows_constraint)
    cols_constraint = [ Distinct(columns[i]) for i in range(9) ]
    s.add(cols_constraint)
    boxes_constraint = [ Distinct(boxes[i]) for i in range(9) ]
    s.add(boxes_constraint)

    # create the board of values out of the original puzzle
    board = translate_puzzle(puzzle)

    # create and add constraint that the squares of the board, if known from the 
    # start, must match their starting values
    starting_values_constraint = [ If(board[i][j] != 0, 
                                      rows[i][j] == board[i][j],
                                      True) 
                                      for i in range(9) for j in range(9) ]
    s.add(starting_values_constraint)

    if s.check() == sat:
        m = s.model()
        e = [ [ m.evaluate(rows[i][j]) 
               for j in range(9) ] for i in range(9) ]
        for i in range(9):
            print(e[i])
    else:
        print('failed')


if __name__ == '__main__':
    main()