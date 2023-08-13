"""
Author: Luke Marshall
Description: Sudoku solver in Python using constraint propogation and search.
"""


def translate_puzzle(puzzle: list[list]) -> dict:
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
    # Creates 3x3 matrices out of the 3x9 matrix, takes a starting integer in order to 
    # differentiate the outputs from the 3 3x9 matrices made from the original puzzle board
    rows = 'ABCDEFGHI'
    grid_3x3s = [[],[],[]]
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

    grid_3x9_1 = [[],[],[]]
    for j in range(3):
        for k in range(9):
            grid_3x9_1[j].append(('').join([row_order[j], str(k+1)]))

    grid_3x9_2 = [[],[],[]]
    for j in range(3):
        for k in range(9):
            grid_3x9_2[j].append(('').join([row_order[j+3], str(k+1)]))

    grid_3x9_3 = [[],[],[]]
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
            if values[units[i][j]].isnumeric():
                if values[units[i][j]] in possible_values:
                    possible_values.remove(values[units[i][j]])
                else:
                    return False
            else:
                continue
    return True


#def constraint_propogation(values: dict) -> dict:


#def search(values: dict) -> dict:
    

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
    
