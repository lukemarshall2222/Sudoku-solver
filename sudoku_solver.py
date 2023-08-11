"""
Author: Luke Marshall
Description: Sudoku solver in Python using constraint propogation and search.
"""


def translate_puzzle(puzzle: list[list]) -> dict:
    rows = 'ABCDEFGHI'
    all_possible_values = '123456789'
    values = {}
    separator = ''
    for i in range(1, 10):
        for j in range(1, 10):
            if puzzle[i][j]:
                values[separator.join([rows[i], str(j)])] = str(puzzle[i][j])
            else:
                values[separator.join([rows[i], str(j)])] = all_possible_values
    
    return values

def main():
    puzzle = input("""Please enter a Sudoku puzzle.
                   The puzzle must be in the form of a list of 9 rows.
                   The given values must be placed in their original spots
                   with empty squares are represented by zeros.
                   Ex: [[400000805],[030000000],[000700000],
                        [020000060],[000080400],[000010000],
                        [000603070],[500200000],[104000000]]""")
    values = translate_puzzle(puzzle)
