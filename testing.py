import unittest
from genetic import *

class TestSolverMethods(unittest.TestCase):
    def test1_piecesFromMatrix(self):
        problem = [[1,2],[3,4]]
        pieces = SBP.piecesFromMatrix(problem)
        self.assertEqual(len(pieces), 4)
        for i in range(len(problem)):
            for j in range(len(problem[i])):
                self.assertTrue(problem[i][j] in pieces)
                self.assertTrue((i,j) in pieces[problem[i][j]].posits)

    def test1_legal(self):
        piece = Piece(1, (1, 0))
        move = Move((0,0), Compass.UP, piece)
        board = Board([[0,2],[1,3]])
        self.assertTrue(SBP.legal(move, board))

    def test2_legal(self):
        piece = Piece(1, (1, 0))
        move = Move((0,0), Compass.UP, piece)
        board = Board([[2,0],[1,3]])
        self.assertFalse(SBP.legal(move, board))

    def test3_legal(self):
        piece = Piece(1, (1, 0))
        move = Move((0,0), Compass.UP, piece)
        board = Board([[0,1],[2,3]])
        self.assertFalse(SBP.legal(move, board))

    def test4_legal(self):
        piece = Piece(1, (0,0))
        move = Move((0,0), Compass.UP, piece)
        board = Board([[1,0],[2,3]])
        self.assertFalse(SBP.legal(move, board))

    def test5_legal(self):
        

if __name__ == '__main__':
    unittest.main()
