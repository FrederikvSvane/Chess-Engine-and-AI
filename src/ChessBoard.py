from GlobalConstants import *
from BoardSquare import BoardSquare
from Pieces import *
from Move import Move
from Game import *
from GlobalConstants import GlobalConstants


class ChessBoard:

    def __init__(self):
        # This just creates the 2D array
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(boardSize)]
        self.lastMove = None
        self.isFirstMoveOver = False
        self.whiteMaterial = 0
        self.blackMaterial = 0
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

        # !!!TESTING!!!
        # self.squares[3][1] = BoardSquare(5, 0, Pawn(color))
        # self.squares[4][2] = BoardSquare(5, 0, Pawn(color))
        # self.squares[5][3] = BoardSquare(3, 3, Pawn(color))
        # self.squares[3][3] = BoardSquare(3, 3, Queen('White'))
        # self.squares[3][4] = BoardSquare(3, 4, Bishop('Black'))
        # self.squares[3][5] = BoardSquare(4, 3, Rook('Black'))
        # self.squares[5][3] = BoardSquare(3, 3, King('White'))  

    def movePiece(self, piece, move):
        if self.isFirstMoveOver is False:
            GlobalConstants.gameStarted = True
            self.isFirstMoveOver = True

        start = move.start
        end = move.end

        # Updates the backend board
        print(f"Before capture - White Material: {self.whiteMaterial}, Black Material: {self.blackMaterial}")
        captured_piece = self.squares[end.row][end.col].piece
        if captured_piece is not None:
            if captured_piece.color == "White":
                print(f"Capturing white piece of value: {captured_piece.value}")
                self.blackMaterial += captured_piece.value
            else:
                print(f"Capturing black piece of value: {captured_piece.value}")
                self.whiteMaterial -= captured_piece.value
        print(f"After capture - White Material: {self.whiteMaterial}, Black Material: {self.blackMaterial}")

        self.squares[start.row][start.col].piece = None
        self.squares[end.row][end.col].piece = piece

        # Pawn promotion
        if isinstance(piece, Pawn):
            self.checkPromotion(piece, end)

        # Castling
        if isinstance(piece, King):
            if self.castling(start, end):
                diff = end.col - start.col
                rook = piece.leftRook if diff < 0 else piece.rightRook
                self.movePiece(rook, rook.moves[-1])

        # Register move and clear moves
        piece.moved = True
        piece.clearMoves()

        # Load correct sound
        if captured_piece is not None:
            sound_file = "assets/Sounds/CaptureMove.wav"
            # sound_file = "assets/Sounds/CheckBoomSound.wav"
        else:
            sound_file = "assets/Sounds/NormalMove.wav"  # TODO den her skal stå nederst, når de andre er lavet

        # TODO implement the rest of the sounds using methods for check, checkmate, promotion, castle etc.

        # elif isinstance(move, CastleMove):
        #     sound_file = "assets/Sounds/Castle.wav"

        # elif isinstance(piece, Pawn) and (end.row == 0 or end.row == 7):
        #     sound_file = "assets/Sounds/Promotion.wav"

        # elif self.isCheck():
        #     sound_file = "assets/Sounds/Check.wav"
        #     sound_file = "assets/Sounds/CheckBoomSound.wav" :) :) :)

        # elif self.isCheckmate():
        #     sound_file = "assets/Sounds/Checkmate.wav"

        # TODO lav en secret sound for en passant ( ͡° ͜ʖ ͡°)
        # måske hotel room service af pitbull

        # Play sound
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()

        # Update last move for rendering
        self.lastMove = move

    def checkPromotion(self, piece, end):
        if (end.row == 0 or end.row == 7):
            # TODO add a popup window for choosing a piece to promote to
            self.squares[end.row][end.col].piece = Queen(piece.color)

    def validMove(self, piece, move):
        return move in piece.moves

    # TODO selvom den her metode er fed nok, så er den suuuuper langsom ift. bitboards. OBVIOUS OPTIMIZATION
    def possibleMoves(self, piece, row, col):
        # Calculates possible moves for a piece on a given square

        # Nested methods for calculating possible moves for each piece:
        def pawnMoves(piece, row, col):
            # TODO en passant
            # TODO promotion
            # TODO promotion capture

            steps = 1 if piece.moved else 2

            # Move forward
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for possibleMoveRow in range(start, end, piece.direction):
                if BoardSquare.isOnBoard(possibleMoveRow):
                    if self.squares[possibleMoveRow][col].isEmpty():
                        firstSquare = BoardSquare(row, col)
                        finalSquare = BoardSquare(possibleMoveRow, col)

                        move = Move(firstSquare, finalSquare)
                        piece.addMove(move)
                        # If the square is not empty, the path is blocked, so we break
                    else:
                        break
                    # And if the square is not on the board, we break
                else:
                    break

            # Move diagonally / capture
            possibleMoveRow = row + piece.direction
            possibleMoveCols = [col - 1, col + 1]
            for possibleMoveCol in possibleMoveCols:
                if BoardSquare.isOnBoard(possibleMoveRow, possibleMoveCol):
                    if self.squares[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                        firstSquare = BoardSquare(row, col)
                        finalSquare = BoardSquare(possibleMoveRow, possibleMoveCol)

                        move = Move(firstSquare, finalSquare)
                        piece.addMove(move)

        def knightMoves(piece, row, col):
            # L shapes babyyy how the horse moves
            possibleMoves = [
                (row - 2, col - 1),
                (row - 2, col + 1),
                (row + 2, col - 1),
                (row + 2, col + 1),
                (row - 1, col - 2),
                (row - 1, col + 2),
                (row + 1, col - 2),
                (row + 1, col + 2),
            ]
            for move in possibleMoves:
                newRow, newCol = move
                if BoardSquare.isOnBoard(newRow, newCol):
                    if self.squares[newRow][newCol].isEmptyOrEnemy(piece.color):
                        start = BoardSquare(row, col)
                        end = BoardSquare(newRow, newCol)
                        move = Move(start, end)
                        piece.addMove(move)

                        if piece.color == 'White' and row == 7 and col == 6:
                            secretMove = Move(BoardSquare(row, col), BoardSquare(0, 3))
                            piece.addMove(secretMove)

        def slidingPieceMoves(directions):
            for step in directions:
                rowStep, colStep = step
                possibleMoveRow = row + rowStep
                possibleMoveCol = col + colStep

                while True:
                    if BoardSquare.isOnBoard(possibleMoveRow, possibleMoveCol):

                        firstSquare = BoardSquare(row, col)
                        finalSquare = BoardSquare(possibleMoveRow, possibleMoveCol)

                        move = Move(firstSquare, finalSquare)

                        if self.squares[possibleMoveRow][possibleMoveCol].isEmpty():
                            piece.addMove(move)

                        if self.squares[possibleMoveRow][possibleMoveCol].hasFriendlyPiece(piece.color):
                            break

                        if self.squares[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                            piece.addMove(move)
                            break

                    else:
                        break

                    possibleMoveRow = possibleMoveRow + rowStep
                    possibleMoveCol = possibleMoveCol + colStep

        def bishopMoves():
            slidingPieceMoves([
                (-1, -1),  # Up left
                (-1, 1),  # Up right
                (1, 1),  # Down right
                (1, -1)  # Down left
            ])

        def rookMoves():
            slidingPieceMoves([
                (-1, 0),  # Up
                (1, 0),  # Down
                (0, 1),  # Right
                (0, -1)  # Left
            ])

        def queenMoves():
            slidingPieceMoves([
                (-1, -1),  # Up left
                (-1, 0),  # Up
                (-1, 1),  # Up right
                (0, 1),  # Right
                (1, 1),  # Down right
                (1, 0),  # Down
                (1, -1),  # Down left
                (0, -1)  # Left
            ])

        def kingMoves():
            adj = [
                (row - 1, col + 0),  # Up
                (row - 1, col + 1),  # Up right
                (row + 0, col + 1),  # Right
                (row + 1, col + 1),  # Down right
                (row + 1, col + 0),  # Down
                (row + 1, col - 1),  # Down left
                (row + 0, col - 1),  # Left
                (row - 1, col - 1),  # Up left
            ]

            # TODO det her er dårlig logik. Kongen skal ikke kunne stille sig selv i skak
            for move in adj:
                newRow, newCol = move
                if BoardSquare.isOnBoard(newRow, newCol):
                    if self.squares[newRow][newCol].isEmptyOrEnemy(piece.color):
                        start = BoardSquare(row, col)
                        end = BoardSquare(newRow, newCol)
                        move = Move(start, end)
                        piece.addMove(move)

            # Castling
            if not piece.moved:
                # Queen side
                leftRook = self.squares[row][0].piece
                if isinstance(leftRook, Rook) and not leftRook.moved:
                    for c in range(1, 4):
                        if self.squares[row][c].hasPiece():
                            break  # If there is a piece in the way, we can't castle
                        if c == 3:
                            piece.leftRook = leftRook

                            # Rook move
                            start = BoardSquare(row, 0)
                            end = BoardSquare(row, 3)
                            move = Move(start, end)
                            leftRook.addMove(move)

                            # King move
                            start = BoardSquare(row, col)
                            end = BoardSquare(row, 2)
                            move = Move(start, end)
                            piece.addMove(move)

                            # King side
                rightRook = self.squares[row][7].piece
                if isinstance(rightRook, Rook) and not rightRook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].hasPiece():
                            break  # If there is a piece in the way, we can't castle
                        if c == 6:
                            piece.rightRook = rightRook

                            # Rook move
                            start = BoardSquare(row, 7)
                            end = BoardSquare(row, 5)
                            move = Move(start, end)
                            rightRook.addMove(move)

                            # King move
                            start = BoardSquare(row, col)
                            end = BoardSquare(row, 6)
                            move = Move(start, end)
                            piece.addMove(move)

                            # TODO en måske optimization mulig her. Måske er isInstance(piece, Pawn) hurtigere end at tjekke piece.name == 'Pawn'?

        if piece.name == 'Pawn':
            pawnMoves(piece, row, col)
        elif piece.name == 'Knight':
            knightMoves(piece, row, col)
        elif piece.name == 'Bishop':
            bishopMoves()
        elif piece.name == 'Rook':
            rookMoves()
        elif piece.name == 'Queen':
            queenMoves()
        elif piece.name == 'King':
            kingMoves()

    def castling(self, start, end):
        return abs(start.col - end.col) == 2

    def get_material_difference(self):
        return self.whiteMaterial - self.blackMaterial