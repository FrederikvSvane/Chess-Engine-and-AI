from GlobalConstants import *
from BoardSquare import BoardSquare
from Pieces import *
from Move import Move
import copy


class ChessBoard:

    def __init__(self):
        # This just creates the 2D array
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(boardSize)]
        self.allMoves = []

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

    # def movePiece(self, piece, move, playSound=True):
    #     startSquare = move.startSquare
    #     targetSquare = move.targetSquare

    #     move.capturedPiece = self.squares[targetSquare.row][targetSquare.col].piece

    #     # Updates the backend board
    #     self.updateBoard(piece, startSquare, targetSquare)

    #     # Handle special moves
    #     self.handleSpecialMoves(piece, startSquare, targetSquare)

    #     # Register move and clear moves
    #     piece.moved = True
    #     piece.clearMoves()
    #     self.allMoves.append(move)
        
    #     # Play  sound

    #     if playSound:
    #         sound = pygame.mixer.Sound('assets/Sounds/NormalMove.wav')
    #         if move.capturedPiece is not None:
    #             sound = pygame.mixer.Sound('assets/Sounds/CaptureMove.wav')
    #         sound.play()
        
    def movePiece(self, piece, move, playSound=True):
        startSquare = move.startSquare
        targetSquare = move.targetSquare

        move.capturedPiece = self.squares[targetSquare.row][targetSquare.col].piece

        enPassantSquareIsEmpty = self.squares[targetSquare.row][targetSquare.col].isEmpty()

        # Updates the backend board
        captured_piece = self.squares[targetSquare.row][targetSquare.col].piece
        self.squares[startSquare.row][startSquare.col].piece = None
        self.squares[targetSquare.row][targetSquare.col].piece = piece

        if isinstance(piece, Pawn):
            # En passant capture
            diff = targetSquare.col - startSquare.col
            if diff != 0 and enPassantSquareIsEmpty:
                self.squares[startSquare.row][startSquare.col + diff].piece = None
                self.squares[targetSquare.row][targetSquare.col].piece = piece
                move.isEnPassantMove = True
            # Pawn promotion (happens inside an else here, beucase en passant and promotion can not happen at the same time)
            else:    
                if self.checkPromotion(piece, targetSquare):
                    move.isPromotionMove = True

        # Castling
        if isinstance(piece, King):
            if self.castling(startSquare, targetSquare):
                move.isCastlingMove = True
                diff = targetSquare.col - startSquare.col
                rook = piece.leftRook if diff < 0 else piece.rightRook
                if rook.moves:
                    self.movePiece(rook, rook.moves[-1], playSound=False)
                else:
                    pass # The rook has no moves that dont result in a check, so we can't castle

        # Register move and clear moves
        self.allMoves.append(move)
        piece.moved = True
        piece.clearMoves()

        if playSound:
            if captured_piece is not None:
                sound_file = "assets/Sounds/CaptureMove.wav"
            else:
                sound_file = "assets/Sounds/NormalMove.wav"

            # Play sound
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()


            
    def undoMove(self, playSound = False):
        if not self.allMoves:
            return

        # Get the last move
        lastMove = self.allMoves.pop()

        # Get the start and target squares
        startSquare = lastMove.startSquare
        targetSquare = lastMove.targetSquare

        # Get the piece that was moved
        movedPiece = self.squares[targetSquare.row][targetSquare.col].piece

        # Move the piece back to the start square
        self.squares[startSquare.row][startSquare.col].piece = movedPiece
        self.squares[targetSquare.row][targetSquare.col].piece = lastMove.capturedPiece

        # If the piece was a pawn and it was its first move, set its moved attribute to False
        if isinstance(movedPiece, Pawn) and movedPiece.moved:
            movedPiece.moved = False

        if lastMove.isCastlingMove:
            self.undoMove() #Undo move again, to undo the rook move
        
        if lastMove.isEnPassantMove:
            diff = targetSquare.col - startSquare.col
            color = 'Black' if movedPiece.color == 'White' else 'White'
            self.squares[startSquare.row][startSquare.col + diff].piece = Pawn(color)

        if lastMove.isPromotionMove:
            self.squares[startSquare.row][startSquare.col].piece = Pawn(movedPiece.color)

        # Play sound
        if playSound:
            pygame.mixer.Sound('assets/Sounds/PromoteMove.wav').play()
        
    def checkPromotion(self, piece, targetSquare):
        if (targetSquare.row == 0 or targetSquare.row == 7):
            # TODO: add a popup window for choosing a piece to promote to
            self.squares[targetSquare.row][targetSquare.col].piece = Queen(piece.color)
            return True
        return False

    def validMove(self, piece, move):
        return move in piece.moves

    def getAllPossibleMoves(self, color):
        allMoves = []
        for row in range(boardSize):
            for col in range(boardSize):
                piece = self.squares[row][col].piece
                if piece and piece.color == color:
                    self.possibleMoves(piece, row, col, normalCall=True)
                    for move in piece.moves:
                        allMoves.append(move)
                    piece.clearMoves()
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
                            enemyPiece.clearMoves()
                            return True
                    enemyPiece.clearMoves()
        return False

    def isInCheckmate(self, kingColor):

        #Find the king
        for row in range(boardSize):
            for col in range(boardSize):
                friendlyPiece = self.squares[row][col].piece
                if isinstance(friendlyPiece, King) and friendlyPiece.color == kingColor:
                    king = friendlyPiece
                    break

        #If the king is not in check, it is not in checkmate
        if not self.isInCheck(king):
            return False


        #Check if any move can take the king out of check:

        #Finding all friendly pieces
        for row in range(boardSize):
            for col in range(boardSize):
                copyPiece = copy.deepcopy(self.squares[row][col].piece)
                if copyPiece is not None and copyPiece.color == kingColor:
                    # Find all possible moves for a given piece
                    self.possibleMoves(copyPiece, row, col, normalCall=True)
                    if copyPiece.moves is not None:
                        for move in copyPiece.moves:
                            tempBoard = copy.deepcopy(self)
                            #This tries every single legal move of every single piece
                            tempBoard.movePiece(copyPiece, move, playSound=False)
                            if not tempBoard.isInCheck(king):
                                return False
        #If no move can take the king out of check, it is checkmate
        return True

    def convertToChessCoordinates(self, row, col):
        # Convert the column to a letter A-H
        col = chr(col + ord('A'))
        # Convert the row to a number 1-8 (we add 1 because chess rows start at 1, not 0)
        row = 8 - row
        return col + str(row)

# -------------- POSSIBLE MOVES -------------------



    #TODO: selvom den her metode er fed nok, så er den suuuuper langsom ift. bitboards. OBVIOUS OPTIMIZATION
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
                (-1, -1), # Up left
                (-1, 0), # Up
                (-1, 1), # Up right
                (0, 1), # Right
                (1, 1), # Down right
                (1, 0), # Down
                (1, -1), # Down left
                (0, -1) # Left
            ])

        def kingMoves():
            adj = [
                (row - 1, col + 0), # Up
                (row - 1, col + 1), # Up right
                (row + 0, col + 1), # Right
                (row + 1, col + 1), # Down right
                (row + 1, col + 0), # Down
                (row + 1, col - 1), # Down left
                (row + 0, col - 1), # Left
                (row - 1, col - 1), # Up left
            ]

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
                            piece.addMove(move) # Skal der breakes her? Er det en bug? I am not sure. TODO spørg chat
            
            #Castling
            if not piece.moved:
                #Queen side
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

                #King side
                rightRook = self.squares[row][7].piece
                if isinstance(rightRook, Rook) and not rightRook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].hasPiece():
                            break #If there is a piece in the way, we can't castle
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

        # TODO: en måske optimization mulig her. Måske er isInstance(piece, Pawn) hurtigere end at tjekke piece.name == 'Pawn'?
        if piece.name == 'Pawn': pawnMoves(piece, row, col)
        elif piece.name == 'Knight': knightMoves(piece, row, col)
        elif piece.name == 'Bishop': bishopMoves()
        elif piece.name == 'Rook': rookMoves()
        elif piece.name == 'Queen': queenMoves()
        elif piece.name == 'King': kingMoves()
                    
        

