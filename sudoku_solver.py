"""
Author: Luke Marshall
Description: Sudoku solver in Python using constraint propogation and search.
"""


def translate_puzzle(puzzle: str) -> dict:
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
    count = 0
    possibilities = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for key in values:
        if len(values[key]) == 1:
            count += 1
            possibilities.discard(values[key])
    if (count < 17) and (len(possibilities) > 1):
        return False

    for i in range(27):
        possible_values = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
        for j in range(9):
            if len(values[units[i][j]]) == 1:
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
            if len(values[key]) == 1:
                continue
            else:
                return False
        return True
    else:
        return False


def constraint_propogation(values: dict, units: list[list]) -> dict:
    # If a square has only one possible value,
    # then eliminate that value from the square's peers
    for unit in units:
        for square in unit:
            if len(values[square]) == 1:
                for sq in unit:
                    if len(values[sq]) > 1:
                        values[sq] = values[sq].replace(values[square], '')
                    else:
                        continue
            else:
                continue

    # If a unit has only one possibe place for a value, 
    # then put that value there
    possible_values = {}
    for unit in units:
        for i in range(9):
            possible_values[str(i+1)] = 0

    for unit in units:
        for square in unit:
            if len(values[square]) > 1:
                for char in values[square]:
                    possible_values[char] += 1
            else:
                continue
        for key in possible_values:
            if possible_values[key] == 1:
                for sq in unit:
                    if len(values[sq]) > 1:
                        for character in values[sq]:
                            if character == key:
                                values[sq] = key
                                break
                            else:
                                continue
                    else:
                        continue
            else:
                continue
    
    return values


def search(values: dict, units: list[list]) -> dict:

    # base case: 
    if solved_puzzle(units, values):
        return values

    # recursive case:

    # find the square with the least number of value options
    values_copy = values.copy()
    least_key = ''
    values_len = 9
    for key in values:
        if 1 < len(values[key]) < values_len:
            least_key = key
            values_len = len(values[key])

    # use the square with the least number of options as a launch
    # point to guess its value and execute more constraint propogation.
    values_copy[least_key] = values_copy[least_key][0]
    check_dict = values_copy.copy()
    while True:
        constraint_propogation(values_copy, units)
        if values_copy == check_dict:
            break
        else:
            values_copy = check_dict.copy()

    if valid_puzzle(units, values_copy):
        return search(values_copy, units)
    else:
        values[least_key] = values[least_key].replace(values[least_key][0], '')
        return search(values, units)
    

def main():
    puzzle = input("""Please enter a Sudoku puzzle.
                   The puzzle must be in the form of a string of 81 values.
                   The given values must be placed in their original spots
                   with empty squares represented by zero ('0') or ('.').
                   Ex: '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'"""
)
    values = translate_puzzle(puzzle)
    units = create_units(puzzle)

    assert valid_puzzle(units, values), "This puzzle is not valid"

    return search(values, units)
    