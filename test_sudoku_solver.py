"""
Author: Luke Marshall
Description: Test cases for Sudoku_solver.py
"""

import unittest
import sudoku_solver


class test_solver(unittest.TestCase):

    def setUp(self):
        self.rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.puzzle = [[4, 0, 0, 0, 0, 0, 8, 0, 5], [0, 3, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 8, 0, 4, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0, 0],
                       [0, 0, 0, 6, 0, 3, 0, 7, 0], [5, 0, 0, 2, 0, 0, 0, 0, 0], [1, 0, 4, 0, 0, 0, 0, 0, 0]]
        self.null_puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.solved_puzzle = [[4, 8, 3, 9, 2, 1, 6, 5, 7], [9, 6, 7, 3, 4, 5, 8, 2, 1], [2, 5, 1, 8, 7, 6, 4, 9, 3],
                              [5, 4, 8, 1, 3, 2, 9, 7, 6], [7, 2, 9, 5, 6, 4, 1, 3, 8], [1, 3, 6, 7, 9, 8, 2, 4, 5],
                              [3, 7, 2, 6, 8, 9, 5, 1, 4], [8, 1, 4, 2, 5, 3, 7, 6, 9], [6, 9, 5, 4, 1, 7, 3, 8, 2]]
        
        self.units = sudoku_solver.create_units()

    def test_translate_puzzle(self):
        for row in self.rows:
            for col in self.columns:
                self.assertIn(
                    ('').join([row, col]), sudoku_solver.translate_puzzle(self.puzzle))

        translated = sudoku_solver.translate_puzzle(self.puzzle)
        self.assertEqual(translated['A1'], 4)
        self.assertEqual(translated['A7'], 8)
        self.assertEqual(translated['A9'], 5)
        self.assertEqual(translated['E5'], 8)
        self.assertEqual(translated['I1'], 1)
        self.assertEqual(translated['I3'], 4)
        self.assertEqual(translated['A2'], '123456789')
        self.assertEqual(translated['I9'], '123456789')

    def test_create_units(self):
        translated = sudoku_solver.translate_puzzle(self.null_puzzle)
        for unit in self.units:
            for square in unit:
                if translated[square] == '123456789':
                    translated[square] = 1
                else:
                    translated[square] += 1
        
        for key in translated:
            self.assertEqual(translated[key], 3)

    def test_valid_puzzle(self):
        self.assertTrue(sudoku_solver.valid_puzzle(self.units, sudoku_solver.translate_puzzle(self.puzzle)))
        self.assertFalse(sudoku_solver.valid_puzzle(self.units, sudoku_solver.translate_puzzle(self.null_puzzle)))
        
        invalid_puzzle_row = [[1, 0, 0, 0, 0, 0, 0, 0, 0], [4, 0, 0, 0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 3, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 8, 0, 9]]
        invalid_puzzle_col = [[0, 1, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 8, 0, 0, 0],
                       [0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 7, 0, 0, 0, 0], [0, 6, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 9, 0, 0, 0, 0]]
        self.assertFalse(sudoku_solver.valid_puzzle(self.units, sudoku_solver.translate_puzzle(invalid_puzzle_row)))
        self.assertFalse(sudoku_solver.valid_puzzle(self.units, sudoku_solver.translate_puzzle(invalid_puzzle_col)))

    def test_solved_puzzle(self):
        translated = sudoku_solver.translate_puzzle(self.solved_puzzle)
        self.assertTrue(sudoku_solver.solved_puzzle(self.units, translated))

        translated_2 = sudoku_solver.translate_puzzle(self.null_puzzle)
        self.assertFalse(sudoku_solver.solved_puzzle(self.units, translated_2))

        translated_3 = sudoku_solver.translate_puzzle(self.puzzle)
        self.assertFalse(sudoku_solver.solved_puzzle(self.units, translated_3))
    
    def test_constraint_propogation(self):
        solvable_by_cp = [[0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0],
                          [0, 0, 8, 1, 0, 2, 9, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0],
                          [0, 0, 2, 6, 0, 9, 5, 0, 0], [8, 0, 0, 2, 0, 3, 0, 0, 9], [0, 0, 5, 0, 1, 0, 3, 0, 0]]
        translated = sudoku_solver.translate_puzzle(solvable_by_cp)
        check_dict = translated.copy()
        while True:
            solved = sudoku_solver.constraint_propogation(check_dict, self.units)
            if solved == check_dict:
                break
            else:
                check_dict = solved.copy()
        print(solved)
        self.assertTrue(sudoku_solver.solved_puzzle(self.units, solved))



if __name__ == '__main__':
    unittest.main()
