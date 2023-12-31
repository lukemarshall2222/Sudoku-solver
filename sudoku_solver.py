"""
Author: Luke Marshall
Description: Sudoku solver in Python using constraint propogation and search.
"""


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
    
    return values


def create_units() -> list[list]:
    row_order = 'ABCDEFGHI'
    # create the row units
    rows = [[ ('').join([row_order[i], str(j+1)]) 
             for j in range(9)] for i in range(9) ]

    # create the column units
    columns = [[ ('').join([row_order[j], str(i+1)]) 
                for j in range(9)] for i in range(9) ]
    
    # create box units
    row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    boxes = []
    for iteration in range(3):
        squares = [[], [], []]
        for row_i in range(3):
            for col_i in range(9):
                if col_i < 3:
                    squares[0].append(('').join([row_letters[row_i], str(col_i+1)]))
                elif 2 < col_i < 6:
                    squares[1].append(('').join([row_letters[row_i], str(col_i+1)]))
                else:
                    squares[2].append(('').join([row_letters[row_i], str(col_i+1)]))
        for box in squares:
            boxes.append(box)
        del row_letters[:3]

    # Add all units into one large list 
    all_units = []
    for i in range(9):
        all_units.append(rows[i])
        all_units.append(columns[i])
        all_units.append(boxes[i])
        
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


def constraint_propagation(values: dict, units: list[list]) -> dict:
    # If a square has only one possible value,
    # then eliminate that value from the square's peers
    values_cp = values.copy()
    for unit in units:
        for square in unit:
            if len(values_cp[square]) == 1:
                for sq in unit:
                    if len(values_cp[sq]) > 1:
                        values_cp[sq] = values_cp[sq].replace(values_cp[square], '')

    # If a unit has only one possibe place for a value, 
    # then put that value there
    possible_values = {}
    for i in range(9):
        possible_values[str(i+1)] = 0
    reset_possible_values = possible_values.copy()

    for unit in units:
        for square in unit:
            if len(values[square]) > 1:
                for char in values[square]:
                    possible_values[char] += 1
        for key in possible_values:
            if possible_values[key] == 1:
                for sq in unit:
                    if len(values[sq]) > 1:
                        for character in values[sq]:
                            if character == key:
                                values[sq] = key
                                break
        possible_values = reset_possible_values.copy()
    
    return values_cp


def cp_loop(values: dict, units: list[list]) -> dict:
    solved = values.copy()
    check_dict = values.copy()
    while True:
        solved = constraint_propagation(solved, units)
        if solved == check_dict:
            break
        else:
            check_dict = solved.copy()
            continue
    
    return solved


def search(values: dict, units: list[list]) -> bool:
    values = cp_loop(values, units)
    if solved_puzzle(units, values) or not valid_puzzle(units, values):
        return values
    values_copy = values.copy()
    least_key = ''
    values_len = 10
    for key in values:
        if 1 < len(values[key]) < values_len:
            least_key = key
            values_len = len(values[key])
    for value in values[least_key]:
        values[least_key] = value
        values = search(values, units)
        if solved_puzzle(units, values):
            return values
        else:
            values = values_copy.copy()
    return values


def transcribe(solved: dict) -> str:
    return ('').join(solved.values())    


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

    values = translate_puzzle(puzzle)
    units = create_units()

    # check that the puzzle is valid before beginning
    assert valid_puzzle(units, values), "This puzzle is not valid, detected at the start."

    solved = search(values, units)
    
    # check that the puzzle is valid and solvable before returning it
    assert valid_puzzle(units, solved), "This puzzle is not valid, detected while solving."
    assert solved_puzzle(units, solved), "This puzzle is not solvable."

    # turn the values dict back into a string 
    solved_transcription = transcribe(solved)
    print(f"The solved puzzle is: {solved_transcription}")

    return solved_transcription


if __name__ == '__main__':
    main()
