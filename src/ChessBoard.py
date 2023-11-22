from GlobalConstants import *
from BoardSquare import BoardSquare
from Pieces import *
from Move import Move


class ChessBoard:

    def __init__(self):
        # This just creates the 2D array
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(boardSize)]

        self._create()
        self._add_pieces('White')
        self._add_pieces('Black')

    
    def _create(self):
        # This actually fills the 2D array with BoardSquare objects
        for row in range(boardSize):
            for col in range(boardSize):
                self.squares[row][col] = BoardSquare(row, col)

    def _add_pieces(self, color):
        # This adds the piece objects to the BoardSquare objects, drawing all pieces onto the board
        row_pawn, row_other = (6, 7) if color == 'White' else (1, 0)

        # pawns
        for col in range(boardSize):
            self.squares[row_pawn][col] = BoardSquare(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = BoardSquare(row_other, 1, Knight(color))
        self.squares[row_other][6] = BoardSquare(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = BoardSquare(row_other, 2, Bishop(color))
        self.squares[row_other][5] = BoardSquare(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = BoardSquare(row_other, 0, Rook(color))
        self.squares[row_other][7] = BoardSquare(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = BoardSquare(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = BoardSquare(row_other, 4, King(color))


    def possibleMoves(self, piece, row, col):
            # Calculates possible moves for a piece on a given square


            # Nested methods for calculating possible moves for each piece
            def pawnMoves(piece, row, col):
                pass

            def knightMoves(piece, row, col):
                possibleMoves = [
                    (row+2, col+1),
                    (row+1, col+2),
                    (row-1, col+2),
                    (row-2, col+1),
                    (row-2, col-1),
                    (row-1, col-2),
                    (row+1, col-2),
                    (row+2, col-1)
                ]

                for move in possibleMoves:
                    newRow, newCol = move
                    if BoardSquare.isOnBoard(newRow, newCol):
                        if self.squares[newRow][newCol].isEmptyOrEnemy(piece.color):
                            start = BoardSquare(row, col)
                            end = BoardSquare(newRow, newCol)
                            move = Move(start, end)
                            piece.addMove(move)
                            pass
                        

            def bishopMoves(piece, row, col):
                pass

            def rookMoves(piece, row, col):
                pass

            def queenMoves(piece, row, col):
                pass

            def kingMoves(piece, row, col):
                pass


            # TODO en måske optimization mulig her. Måske er isInstance(piece, Pawn) hurtigere end at tjekke piece.name == 'Pawn'?
            if piece.name == 'Pawn':
                pass
            elif piece.name == 'Knight':
                knightMoves(piece, row, col)

            elif piece.name == 'Bishop':
                pass
            elif piece.name == 'Rook':
                pass
            elif piece.name == 'Queen':
                pass
            elif piece.name == 'King':
                pass