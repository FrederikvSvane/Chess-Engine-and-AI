from GlobalConstants import *


class BoardSquare:

    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def hasPiece(self):
        return self.piece != None

    def isEmpty(self):
        return not self.hasPiece()

    def hasFriendlyPiece(self, color):
        return self.hasPiece() and self.piece.color == color

    def hasEnemyPiece(self, color):
        return self.hasPiece() and self.piece.color != color

    def isEmptyOrEnemy(self, color):
        return self.isEmpty() or self.hasEnemyPiece(color)

    @staticmethod
    def isOnBoard(*args):
        for arg in args:
            if arg < 0 or arg >= boardSize:
                return False
        return True