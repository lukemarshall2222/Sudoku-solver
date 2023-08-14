"""
Author: Luke Marshall
Description: Sudoku solver in Python using constraint propogation and search.
"""


def translate_puzzle(puzzle: list[list]) -> dict:
    # check puzzle has necessary rows and columns
    assert len(puzzle) == 9, "Puzzles must contain 9 rows of values."
    for row in puzzle:
        assert len(row) == 9, """Puzzle rows should contain 9 values, a number
                                 1-9 if given or 0 if empty."""
    
    # translate the puzzle into a dict with coordinates as keys and a number 1-9 or
    # a string of possible numbers as values
    rows = 'ABCDEFGHI'
    all_possible_values = '123456789'
    values = {}
    for i in range(9):
        for j in range(9):
            if puzzle[i][j]:
                values[('').join([rows[i], str(j+1)])] = puzzle[i][j]
            else:
                values[('').join([rows[i], str(j+1)])] = all_possible_values
    
    return values


def create_3x3s_from_3x9(grid_3x9: list[list], start: int) -> list[list]:
    # Creates 3x3 matrices out of the 3x9 matrix. Takes a starting integer in
    # order to differentiate the outputs from the 3 3x9 matrices made from the
    # original puzzle board
    rows = 'ABCDEFGHI'
    grid_3x3s = [[], [], []]
    for i in range(start, start+3):
        for j in range(9):
            if j < 3:
                grid_3x3s[0].append(('').join([rows[i], str(j+1)]))
            elif 3 <= j < 6:
                grid_3x3s[1].append(('').join([rows[i], str(j+1)]))
            else:
                grid_3x3s[2].append(('').join([rows[i], str(j+1)]))
    return grid_3x3s


def create_units() -> list[list]:
    row_order = 'ABCDEFGHI'
    # create the row units
    rows = []
    for i in range(9):
        rows.append([])
        for j in range(9):
            rows[i].append(('').join([row_order[i], str(j+1)]))

    # create the column units
    columns = []
    for i in range(9):
        columns.append([])
    for j in range(9):
        for k in range(9):
            columns[k].append(('').join([row_order[j], str(k+1)]))

    # create box units
    boxes = []
    for i in range(9):
        boxes.append([])

    grid_3x9_1 = [[], [], []]
    for j in range(3):
        for k in range(9):
            grid_3x9_1[j].append(('').join([row_order[j], str(k+1)]))

    grid_3x9_2 = [[], [], []]
    for j in range(3):
        for k in range(9):
            grid_3x9_2[j].append(('').join([row_order[j+3], str(k+1)]))

    grid_3x9_3 = [[], [], []]
    for j in range(3):
        for k in range(9):
            grid_3x9_2[j].append(('').join([row_order[j+6], str(k+1)]))
    
    grid_3x3s_1 = create_3x3s_from_3x9(grid_3x9_1, 0)
    grid_3x3s_2 = create_3x3s_from_3x9(grid_3x9_2, 3)
    grid_3x3s_3 = create_3x3s_from_3x9(grid_3x9_3, 6)

    # Add all units into one large list 
    all_units = []
    
    for i in range(9):
        all_units.append(rows[i])
        all_units.append(columns[i])
    
    for i in range(3):
        all_units.append(grid_3x3s_1[i])
        all_units.append(grid_3x3s_2[i])
        all_units.append(grid_3x3s_3[i])
    
    return all_units


def valid_puzzle(units: list[list], values: dict) -> bool:

    for i in range(27):
        possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for j in range(9):
            if isinstance(values[units[i][j]], int):
                if values[units[i][j]] in possible_values:
                    possible_values.remove(values[units[i][j]])
                else:
                    return False
            else:
                continue
    return True


def solved_puzzle(units: list[list], values: dict) -> bool:

    if valid_puzzle(units, values):
        for key in values:
            if isinstance(values[key], int):
                continue
            else:
                return False
        return True
    else:
        return False


def constraint_propogation(values: dict, units: list[list]) -> dict:

    for unit in units:
        for square in unit:
            if isinstance(values[square], int):
                for sq in unit:
                    if isinstance(values[sq], str):
                        values[sq].replace(values[square], '')
                    else:
                        continue
            else:
                continue

    for unit in units:
        possible_values = '123456789'
        for square in unit:
            if isinstance(values[square], int):
                possible_values.replace(str(values[square]), '')
            else:
                for char in values[square]:
                    possible_values.replace(char, '')
        if len(possible_values) == 1:
            for sq in unit:
                if isinstance(values[sq], str):
                    for char in values[sq]:
                        if char == possible_values:
                            values[sq] = int(char)
                            break
        else:
            continue



def search(values: dict, units: list[list]) -> dict:

    # base case: 
    if solved_puzzle(units, values):
        return values
    
    if valid_puzzle()

    # recursive case: 

    # find the square with the least number of value options 
    least_key = ''
    values_len = 9
    for key in values:
        if isinstance(values[key], str):
            if len(values[key]) < values_len:
                least_key = key
                values_len = len(values[key])
    
    # use the square with the least number of options as a launch
    # point to guess its value and execute more constraint propogation
    values_copy = values.copy()
    for char in values_copy[least_key]:
        values_copy[least_key] = char
        while True:
            resultant_dict = constraint_propogation(values_copy, units)
            if resultant_dict == values_copy:
                break
            else:
                values_copy = resultant_dict


    
    

def main():
    puzzle = input("""Please enter a Sudoku puzzle.
                   The puzzle must be in the form of a list of 9 rows.
                   The given values must be placed in their original spots
                   with empty squares are represented by zeros.
                   Ex: [[4,0,0,0,0,0,8,0,5],[0,3,0,0,0,0,0,0,0],[0,0,0,7,0,0,0,0,0],
                        [0,2,0,0,0,0,0,6,0],[0,0,0,0,8,0,4,0,0],[0,0,0,0,1,0,0,0,0],
                        [0,0,0,6,0,3,0,7,0],[5,0,0,2,0,0,0,0,0],[1,0,4,0,0,0,0,0,0]]""")
    values = translate_puzzle(puzzle)
    all_units = create_units(puzzle)
    if not valid_puzzle(all_units, values):
        return False
    else:
        pass
    
