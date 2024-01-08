import copy
from GlobalConstants import *

class ChessAI:
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

    def evalBoard(self, board):
        score = 0
        for row in range(boardSize):
            for col in range(boardSize):
                square = board.squares[row][col]
                if square.hasPiece():
                    piece = square.piece
                    piece_value = piece.value

                    # TODO er ikke sikker på at vi også skal kigge på de hvides placering. Det er jo for at give incitament til at rykke egne brikker frem.
                    if piece.name == 'Pawn':
                        score_table = whitePawnScores if piece.color == 'White' else blackPawnScores
                    elif piece.name == 'Knight':
                        score_table = whiteKnightScores if piece.color == 'White' else blackKnightScores
                    elif piece.name == 'Bishop':
                        score_table = whiteBishopScores if piece.color == 'White' else blackBishopScores
                    elif piece.name == 'Rook':
                        score_table = whiteRookScores if piece.color == 'White' else blackRookScores
                    elif piece.name == 'Queen':
                        score_table = whiteQueenScores if piece.color == 'White' else blackQueenScores
                    elif piece.name == 'King':
                        # Assuming you might switch to king end game scores at some point
                        score_table = whiteKingMiddleGameScores if piece.color == 'White' else blackKingMiddleGameScores

                    # Adjust the score based on the piece's position
                    position_score = score_table[row][col]
                    score += piece_value + position_score

        return score

    def minmax(self, depth, alpha, beta, maximizing_player, board):
        if depth == 0 or board.isInCheckmate('Black') or board.isInCheckmate('White'):
            return self.evalBoard(board)

        if maximizing_player:
            max_eval = float('-inf')
            for move in board.getAllPossibleMoves('White'):
                piece = board.squares[move.startSquare.row][move.startSquare.col].piece
                if piece is not None:
                    board.movePiece(piece, move, playSound=False)
                    eval = self.minmax(depth - 1, alpha, beta, False, board)
                    board.undoMove()
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval
        else:
            min_eval = float('inf')
            for move in board.getAllPossibleMoves('Black'):
                piece = board.squares[move.startSquare.row][move.startSquare.col].piece
                if piece is not None:
                    board.movePiece(piece, move, playSound=False)
                    eval = self.minmax(depth - 1, alpha, beta, True, board)
                    board.undoMove() 
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

    def findBestMove(self):
        boardCopy = copy.deepcopy(self.board)
        max_eval = float('inf')
        best_move = None
        for move in boardCopy.getAllPossibleMoves('Black'):
            piece = boardCopy.squares[move.startSquare.row][move.startSquare.col].piece
            if piece is not None:
                boardCopy.movePiece(piece, move, playSound=False)
                eval = self.minmax(self.depth - 1, float('-inf'), float('inf'), False, boardCopy)
                boardCopy.undoMove()
                if eval < max_eval:
                    max_eval = eval
                    best_move = move


        if best_move is not None:
            targetRow = best_move.targetSquare.row
            targetCol = best_move.targetSquare.col
            piece = boardCopy.squares[best_move.startSquare.row][best_move.startSquare.col].piece
            if piece is not None:   
                print(f"Best move is {piece.name} {boardCopy.convertToChessCoordinates(targetRow, targetCol)}. Board eval: {max_eval}")
            
        return best_move