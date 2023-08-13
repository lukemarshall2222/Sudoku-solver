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
        translated = sudoku_solver.translate_puzzle(self.puzzle)


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
        units = sudoku_solver.create_units()
        for unit in units:
            for square in unit:
                if translated[square] == '123456789':
                    translated[square] = 1
                else:
                    translated[square] += 1
        
        for key in translated:
            self.assertEqual(translated[key], 3)

    def test_valid_puzzle(self):
        units = sudoku_solver.create_units()
        self.assertTrue(sudoku_solver.valid_puzzle(units, sudoku_solver.translate_puzzle(self.puzzle)))
        self.assertTrue(sudoku_solver.valid_puzzle(units, sudoku_solver.translate_puzzle(self.null_puzzle)))
        
        invalid_puzzle_row = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 0, 0, 0, 0, 0, 0, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        invalid_puzzle_col = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertFalse(sudoku_solver.valid_puzzle(units, sudoku_solver.translate_puzzle(invalid_puzzle_row)))
        self.assertFalse(sudoku_solver.valid_puzzle(units, sudoku_solver.translate_puzzle(invalid_puzzle_col)))


if __name__ == '__main__':
    unittest.main()
