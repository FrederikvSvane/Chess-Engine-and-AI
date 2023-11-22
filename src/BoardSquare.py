from GlobalConstants import *


class BoardSquare:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def hasPiece(self):
        return self.piece != None