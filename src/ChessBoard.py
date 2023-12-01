from Pieces import *
from Move import Move
import copy
from BoardSquare import *


class ChessBoard:

    def __init__(self):
        # This just creates the 2D array
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(boardSize)]
        self.lastMove = None
        self.isFirstMoveOver = False
        self.whiteMaterial = 0
        self.blackMaterial = 0
        self._create()
        self._addPieces('White')
        self._addPieces('Black')

    def _create(self):
        # This actually fills the 2D array with BoardSquare objects
        for row in range(boardSize):
            for col in range(boardSize):
                self.squares[row][col] = BoardSquare(row, col)

    def _addPieces(self, color):
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

    def movePiece(self, piece, move,playSound=True):
        if self.isFirstMoveOver is False:
            GlobalConstants.gameStarted = True
            self.isFirstMoveOver = True
        startSquare = move.startSquare
        targetSquare = move.targetSquare

        enPassantSquareIsEmpty = self.squares[targetSquare.row][targetSquare.col].isEmpty()

        # Updates the backend board
        print(f"Before capture - White Material: {self.whiteMaterial}, Black Material: {self.blackMaterial}")
        captured_piece = self.squares[targetSquare.row][targetSquare.col].piece
        if captured_piece is not None:
            if captured_piece.color == "White":
                print(f"Capturing white piece of value: {captured_piece.value}")
                self.blackMaterial += captured_piece.value
            else:
                print(f"Capturing black piece of value: {captured_piece.value}")
                self.whiteMaterial -= captured_piece.value
        print(f"After capture - White Material: {self.whiteMaterial}, Black Material: {self.blackMaterial}")

        self.squares[startSquare.row][startSquare.col].piece = None
        self.squares[targetSquare.row][targetSquare.col].piece = piece

        if isinstance(piece, Pawn):
            # En passant capture
            #TODO den her spiller ikke den rigtige capture sound. Skal fikses
            diff = targetSquare.col - startSquare.col
            if diff != 0 and enPassantSquareIsEmpty:
                self.squares[startSquare.row][startSquare.col + diff].piece = None
                self.squares[targetSquare.row][targetSquare.col].piece = piece
            # Pawn promotion (happens inside an else here, beucase en passant and promotion can not happen at the same time)
            else:
                self.checkPromotion(piece, targetSquare)

        # Castling
        if isinstance(piece, King):
            if self.castling(startSquare, targetSquare):
                diff = targetSquare.col - startSquare.col
                rook = piece.leftRook if diff < 0 else piece.rightRook
                if rook.moves:
                    self.movePiece(rook, rook.moves[-1], playSound=False)
                else:
                    pass # The rook has no moves that dont result in a check, so we can't castle

        # Register move and clear moves
        piece.moved = True
        piece.clearMoves()


        # TODO nu kan vi rokere og promote, så den her logik skal lige omtænkes. Den rigtige lyd må kunne blive indlæst og afspillet på en smart måde
        if playSound:
        #Load correct sound
        #TODO lav en global Sound class med et felt for soundfile, sådan at den kan sættes og overskrives rundt omkring i forskellige metoder
        #Og afspil den så inde i main loopet
            if captured_piece is not None:
                sound_file = "assets/Sounds/CaptureMove.wav"
                #sound_file = "assets/Sounds/CheckBoomSound.wav"
            else:
                sound_file = "assets/Sounds/NormalMove.wav" #TODO den her skal stå nederst, når de andre er lavet

            # TODO implement the rest of the sounds using methods for check, checkmate, promotion, castle etc.

            # elif isinstance(move, CastleMove):
            #     sound_file = "assets/Sounds/Castle.wav"

            # elif isinstance(piece, Pawn) and (targetSquare.row == 0 or targetSquare.row == 7):
            #     sound_file = "assets/Sounds/Promotion.wav"

            # elif self.isCheck():
            #     sound_file = "assets/Sounds/Check.wav"
            #     sound_file = "assets/Sounds/CheckBoomSound.wav" :) :) :)

            # elif self.isCheckmate():
            #     sound_file = "assets/Sounds/Checkmate.wav"

            #TODO lav en secret sound for en passant ( ͡° ͜ʖ ͡°)
            #måske hotel room service af pitbull

            # Play sound
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()

            # Update last move for rendering
            self.lastMove = move

    def checkPromotion(self, piece, targetSquare):
        if (targetSquare.row == 0 or targetSquare.row == 7):
            # TODO add a popup window for choosing a piece to promote to
            self.squares[targetSquare.row][targetSquare.col].piece = Queen(piece.color)
            if piece.color == 'White':
                self.whiteMaterial += 10
            else:
                self.blackMaterial += 10

    def validMove(self, piece, move):
        return move in piece.moves

    def getAllPossibleMoves(self, color):
        allMoves = []
        for row in range(boardSize):
            for col in range(boardSize):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.possibleMoves(piece, row, col, normalCall=False)
                    for move in piece.moves:
                        allMoves.append(move)
        return allMoves

    def castling(self, startSquare, targetSquare):
        return abs(startSquare.col - targetSquare.col) == 2

    def setEnPassantTrue(self, piece):
        for row in range(boardSize):
            for col in range(boardSize):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.enPassant = False
        if isinstance(piece, Pawn):
            piece.enPassant = True

    def moveWillResultInCheck(self, piece, move): #Lækker copy logik her som kan bruges til AI!! TODO AI, optimization
        tempPiece = copy.deepcopy(piece)
        tempBoard = copy.deepcopy(self)
        tempBoard.movePiece(tempPiece, move, playSound=False)

        for row in range(boardSize):
            for col in range(boardSize):
                if tempBoard.squares[row][col].hasEnemyPiece(piece.color):
                    enemyPiece = tempBoard.squares[row][col].piece
                    tempBoard.possibleMoves(enemyPiece, row, col, normalCall=False) #NormalCall is set to false to prevent infinite recursion
                    for move in enemyPiece.moves:
                        if isinstance(move.targetSquare.piece, King):
                            return True
        return False

    def isInCheck(self, king:King):
        for row in range(boardSize):
            for col in range(boardSize):
                if self.squares[row][col].hasEnemyPiece(king.color):
                    enemyPiece = self.squares[row][col].piece
                    self.possibleMoves(enemyPiece, row, col, normalCall=False)
                    for move in enemyPiece.moves:
                        if isinstance(move.targetSquare.piece, King):
                            return True
        return False

    def isInCheckmate(self, kingColor):
        #Find the king
        for row in range(boardSize):
            for col in range(boardSize):
                piece = self.squares[row][col].piece
                if isinstance(piece, King) and piece.color == kingColor:
                    king = piece
                    print(f"{kingColor}'s king found at square {row}, {col}")
                    break
        #If the king is not in check, it is not in checkmate
        if not self.isInCheck(king):
            print("King is not in check")
            return False
        else:
            print("King is in check.")

        #Check if any move can take the king out of check
        print("Checking if any moves can take him out of check")
        for row in range(boardSize):
            for col in range(boardSize):
                piece = self.squares[row][col].piece
                if piece is not None and piece.color == kingColor:
                    print(f"{kingColor} {piece} found at {row}, {col}")
                    possibleMoves = self.possibleMoves(piece, row, col, normalCall=False)
                    if possibleMoves is None:
                        print(f"No possible moves for {piece}")
                        continue
                    for move in possibleMoves:
                        tempBoard = copy.deepcopy(self)
                        #This tries every single legal move of every single piece
                        tempBoard.movePiece(piece, move, playSound=False)
                        if not tempBoard.isInCheck(king):
                            print(f"Move found that takes king out of check!")
                            return False
        #If no move can take the king out of check, it is checkmate
        return True




# -------------- POSSIBLE MOVES -------------------



    #TODO selvom den her metode er fed nok, så er den suuuuper langsom ift. bitboards. OBVIOUS OPTIMIZATION
    def possibleMoves(self, piece, row, col, normalCall=True): #The normalCall is used to prevent infinite recursion inside isInCheck
        # Calculates possible moves for a piece on a given square

        def pawnMoves(piece, row, col):
            steps = 1 if piece.moved else 2
            
            # Move forward
            startSquare = row + piece.direction
            targetSquare = row + (piece.direction * (1 + steps))
            for possibleMoveRow in range(startSquare, targetSquare, piece.direction):
                if BoardSquare.isOnBoard(possibleMoveRow):
                    if self.squares[possibleMoveRow][col].isEmpty():
                        startSquare = BoardSquare(row, col)
                        targetSquare = BoardSquare(possibleMoveRow, col)
                        move = Move(startSquare, targetSquare)

                        if normalCall:
                            if not self.moveWillResultInCheck(piece, move):
                                piece.addMove(move)
                        else:
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
                        startSquare = BoardSquare(row, col)
                        targetPiece = self.squares[possibleMoveRow][possibleMoveCol].piece
                        targetSquare = BoardSquare(possibleMoveRow, possibleMoveCol, targetPiece)
                        move = Move(startSquare, targetSquare)

                        if normalCall:
                            if not self.moveWillResultInCheck(piece, move):
                                piece.addMove(move)
                        else:
                            piece.addMove(move)

            # En passant
            startRow = 3 if piece.color == 'White' else 4
            targetRow = 2 if piece.color == 'White' else 5
            # Left en passant
            if BoardSquare.isOnBoard(col-1) and row == startRow:
                if self.squares[row][col-1].hasEnemyPiece(piece.color):
                    enemyPiece = self.squares[row][col-1].piece
                    if isinstance(enemyPiece, Pawn):
                        if enemyPiece.enPassant:
                            startSquare = BoardSquare(row, col)
                            targetSquare = BoardSquare(targetRow, col-1, enemyPiece)
                            move = Move(startSquare, targetSquare)

                            if normalCall:
                                if not self.moveWillResultInCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)

            # Right en passant
            if BoardSquare.isOnBoard(col+1) and row == startRow:
                if self.squares[row][col+1].hasEnemyPiece(piece.color):
                    enemyPiece = self.squares[row][col+1].piece
                    if isinstance(enemyPiece, Pawn):
                        if enemyPiece.enPassant:
                            startSquare = BoardSquare(row, col)
                            targetSquare = BoardSquare(targetRow, col+1, enemyPiece)
                            move = Move(startSquare, targetSquare)

                            if normalCall:
                                if not self.moveWillResultInCheck(piece, move):
                                    piece.addMove(move)
                            else:
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
                possibleMoveRow, possibleMoveCol = move
                if BoardSquare.isOnBoard(possibleMoveRow, possibleMoveCol):
                    if self.squares[possibleMoveRow][possibleMoveCol].isEmptyOrEnemy(piece.color):
                        startSquare = BoardSquare(row, col)
                        targetPiece = self.squares[possibleMoveRow][possibleMoveCol].piece
                        targetSquare = BoardSquare(possibleMoveRow, possibleMoveCol, targetPiece)

                        move = Move(startSquare, targetSquare)

                        if normalCall:
                            if not self.moveWillResultInCheck(piece, move):
                                piece.addMove(move)
                        else:
                            piece.addMove(move)

                        if piece.color == 'White' and row == 7 and col == 6:
                            secretMove = Move(BoardSquare(row, col), BoardSquare(0,3))
                            piece.addMove(secretMove)
        
        def slidingPieceMoves(directions):
            for step in directions:
                rowStep, colStep = step
                possibleMoveRow = row + rowStep
                possibleMoveCol = col + colStep

                while True:
                    if BoardSquare.isOnBoard(possibleMoveRow, possibleMoveCol):
                        
                        startSquare = BoardSquare(row, col)
                        targetPiece = self.squares[possibleMoveRow][possibleMoveCol].piece
                        targetSquare = BoardSquare(possibleMoveRow, possibleMoveCol, targetPiece)

                        move = Move(startSquare, targetSquare)
                        
                        if self.squares[possibleMoveRow][possibleMoveCol].isEmpty():
                            if normalCall:
                                if not self.moveWillResultInCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)

                        elif self.squares[possibleMoveRow][possibleMoveCol].hasFriendlyPiece(piece.color):
                            break

                        elif self.squares[possibleMoveRow][possibleMoveCol].hasEnemyPiece(piece.color):
                            if normalCall:
                                if not self.moveWillResultInCheck(piece, move):
                                    piece.addMove(move)
                            else:
                                piece.addMove(move)
                            break
                    
                    else:
                        break
                        
                    possibleMoveRow = possibleMoveRow + rowStep
                    possibleMoveCol = possibleMoveCol + colStep                   

        def bishopMoves():
            slidingPieceMoves([
                (-1, -1), # Up left
                (-1, 1), # Up right
                (1, 1), # Down right
                (1, -1) # Down left
            ])

        def rookMoves():
            slidingPieceMoves([
                (-1, 0), # Up
                (1, 0), # Down
                (0, 1), # Right
                (0, -1) # Left
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
                        startSquare = BoardSquare(row, col)
                        targetSquare = BoardSquare(newRow, newCol)
                        move = Move(startSquare, targetSquare)

                        if normalCall:
                            if not self.moveWillResultInCheck(piece, move):
                                piece.addMove(move)
                        else:
                            break # Skal der breakes her? Er det en bug? I am not sure. TODO spørg chat
            
            #Castling
            if not piece.moved:
                # Queen side
                leftRook = self.squares[row][0].piece
                if isinstance(leftRook, Rook) and not leftRook.moved:
                    for c in range(1, 4):
                        if self.squares[row][c].hasPiece():
                            break #If there is a piece in the way, we can't castle
                        if c == 3:
                            piece.leftRook = leftRook

                            #Rook move
                            startSquare = BoardSquare(row, 0)
                            targetSquare = BoardSquare(row, 3)
                            rookMove = Move(startSquare, targetSquare)
                            leftRook.addMove(rookMove)

                            #King move
                            startSquare = BoardSquare(row, col)
                            targetSquare = BoardSquare(row, 2)
                            kingMove = Move(startSquare, targetSquare)

                            if normalCall:
                                if not self.moveWillResultInCheck(piece, kingMove) and not self.moveWillResultInCheck(leftRook, rookMove):
                                    leftRook.addMove(rookMove)
                                    piece.addMove(kingMove)
                            else:
                                leftRook.addMove(rookMove)
                                piece.addMove(kingMove)

                            # King side
                rightRook = self.squares[row][7].piece
                if isinstance(rightRook, Rook) and not rightRook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].hasPiece():
                            break  # If there is a piece in the way, we can't castle
                        if c == 6:
                            piece.rightRook = rightRook

                            #Rook move
                            startSquare = BoardSquare(row, 7)
                            targetSquare = BoardSquare(row, 5)
                            rookMove = Move(startSquare, targetSquare)

                            #King move
                            startSquare = BoardSquare(row, col)
                            targetSquare = BoardSquare(row, 6)
                            kingMove = Move(startSquare, targetSquare)

                            if normalCall:
                                if not self.moveWillResultInCheck(piece, kingMove) and not self.moveWillResultInCheck(rightRook, rookMove):
                                    rightRook.addMove(rookMove)
                                    piece.addMove(kingMove)
                            else:
                                rightRook.addMove(rookMove)
                                piece.addMove(kingMove)

        # TODO en måske optimization mulig her. Måske er isInstance(piece, Pawn) hurtigere end at tjekke piece.name == 'Pawn'?
        if piece.name == 'Pawn': pawnMoves(piece, row, col)
        elif piece.name == 'Knight': knightMoves(piece, row, col)
        elif piece.name == 'Bishop': bishopMoves()
        elif piece.name == 'Rook': rookMoves()
        elif piece.name == 'Queen': queenMoves()
        elif piece.name == 'King': kingMoves()




    def castling(self, start, end):
        return abs(start.col - end.col) == 2

    def getMaterialDifference(self):
        return self.whiteMaterial - self.blackMaterial