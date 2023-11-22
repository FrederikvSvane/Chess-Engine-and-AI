import os
import sys
import contextlib

# Redirect stdout to null temporarily
with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame

from ChessPieces.Rook import Rook
from ChessPieces.Knight import Knight
from ChessPieces.Bishop import Bishop
from ChessPieces.Queen import Queen
from ChessPieces.King import King
from ChessPieces.Pawn import Pawn

def coordinatesToNotation(x: int, y: int) -> str:
    columns = "abcdefgh"
    columnLetter = columns[x]
    rowNumber = 8 - y
    return columnLetter + str(rowNumber)

def notationToCoordinates(notation: str) -> (int, int):
    columns = "abcdefgh"
    x = columns.index(notation[0])
    y = 8 - int(notation[1])
    return x, y


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initializePieces()

    def initializePieces(self):
        # Pawns
        for i in range(8):
            self.board[1][i] = Pawn("black")
            self.board[6][i] = Pawn("white")

        # Rooks
        self.board[0][0] = Rook("black")
        self.board[0][7] = Rook("black")
        self.board[7][0] = Rook("white")
        self.board[7][7] = Rook("white")

        # # Knights
        self.board[0][1] = Knight("black")
        self.board[0][6] = Knight("black")
        self.board[7][1] = Knight("white")
        self.board[7][6] = Knight("white")

        # Bishops
        self.board[0][2] = Bishop("black")
        self.board[0][5] = Bishop("black")
        self.board[7][2] = Bishop("white")
        self.board[7][5] = Bishop("white")

        # Queens
        self.board[0][3] = Queen("black")
        self.board[7][3] = Queen("white")

        # Kings
        self.board[0][4] = King("black")
        self.board[7][4] = King("white")
    
    def printBoard(self):
        for row in self.board:
            print_row = []
            for piece in row:
                if piece:
                    print_row.append("[" + repr(piece) + "]")
                else:
                    print_row.append('[__]')
            print(''.join(print_row))

    def makeMove(self, start: str, end: str):
        startX, startY = notationToCoordinates(start)
        endX, endY = notationToCoordinates(end)

        self.board[endY][endX] = self.board[startY][startX]
        self.board[startY][startX] = None