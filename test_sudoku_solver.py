"""
Author: Luke Marshall
Description: Test cases for Sudoku_solver.py
"""

import unittest
import sudoku_solver
import time


class test_solver(unittest.TestCase):

    def setUp(self):
        self.rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        self.columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.puzzle = "4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......"
        self.puzzle_w_zeros = "400000805030000000000700000020000060000080400000010000000603070500200000104000000"
        self.null_puzzle = "000000000000000000000000000000000000000000000000000000000000000000000000000000000"
        self.solved_puzzle = "483921657967345821251876493548132976729564138136798245372689514814253769695417382"
        self.solvable_by_cp = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'

        self.units = sudoku_solver.create_units()

    def test_translate_puzzle(self):
        translated = sudoku_solver.translate_puzzle(self.puzzle)

        # check if all the coordinates are in the dict
        for row in self.rows:
            for col in self.columns:
                self.assertIn(('').join([row, col]), translated)

        # check if the values for squares match the original
        # original has dots for empty squares
        self.assertEqual(translated['A1'], '4')
        self.assertEqual(translated['A7'], '8')
        self.assertEqual(translated['A9'], '5')
        self.assertEqual(translated['E5'], '8')
        self.assertEqual(translated['I1'], '1')
        self.assertEqual(translated['I3'], '4')
        self.assertEqual(translated['A2'], '123456789')
        self.assertEqual(translated['I9'], '123456789')

        # original has zeros for empty squares
        translated = sudoku_solver.translate_puzzle(self.puzzle_w_zeros)
        self.assertEqual(translated['A1'], '4')
        self.assertEqual(translated['A7'], '8')
        self.assertEqual(translated['A9'], '5')
        self.assertEqual(translated['E5'], '8')
        self.assertEqual(translated['I1'], '1')
        self.assertEqual(translated['I3'], '4')
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
        
        invalid_puzzle_row = "100000000400000000700000000020000000600000006000000000003000000500000000000000809"
        invalid_puzzle_col = "010000000000000030000008000000002000004000000005000000000070000060000030000090000"
        self.assertFalse(sudoku_solver.valid_puzzle(self.units, sudoku_solver.translate_puzzle(invalid_puzzle_row)))
        self.assertFalse(sudoku_solver.valid_puzzle(self.units, sudoku_solver.translate_puzzle(invalid_puzzle_col)))

    def test_solved_puzzle(self):
        translated = sudoku_solver.translate_puzzle(self.solved_puzzle)
        self.assertTrue(sudoku_solver.solved_puzzle(self.units, translated))

        translated_2 = sudoku_solver.translate_puzzle(self.null_puzzle)
        self.assertFalse(sudoku_solver.solved_puzzle(self.units, translated_2))

        translated_3 = sudoku_solver.translate_puzzle(self.puzzle)
        self.assertFalse(sudoku_solver.solved_puzzle(self.units, translated_3))
    
    def test_constraint_propagation(self):
        translated = sudoku_solver.translate_puzzle(self.solvable_by_cp)
        check_dict = translated.copy()
        solved = translated.copy()
        while True:
            solved = sudoku_solver.constraint_propagation(solved, self.units)
            if solved == check_dict:
                break
            else:
                check_dict = solved.copy()
                continue
        self.assertTrue(sudoku_solver.valid_puzzle(self.units, solved))
        self.assertTrue(sudoku_solver.solved_puzzle(self.units, solved))
    
    def test_cp_loop(self):
        translated = sudoku_solver.translate_puzzle(self.solvable_by_cp)
        solved = sudoku_solver.cp_loop(translated, self.units)

        self.assertTrue(sudoku_solver.valid_puzzle(self.units, solved))
        self.assertTrue(sudoku_solver.solved_puzzle(self.units, solved))

    def test_search(self):
        hard_puzzle = "6.....8.3.4.7.................5.4.7.3..2.....1.6.......2.....5.....8.6......1...."
        translated = sudoku_solver.translate_puzzle(hard_puzzle)
        solved = sudoku_solver.search(translated, self.units)
        
        self.assertTrue(sudoku_solver.solved_puzzle(self.units, solved))


if __name__ == '__main__':
    unittest.main()
