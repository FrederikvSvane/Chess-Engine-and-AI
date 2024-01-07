import copy

class ChessAI:
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

    def evalBoard(self, board):
        score = 0
        for row in board.squares:
            for square in row:
                if square.hasPiece():
                    piece = square.piece
                    score += piece.value
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
                startRow = best_move.startSquare.row
                startCol = best_move.startSquare.col
                targetRow = best_move.targetSquare.row
                targetCol = best_move.targetSquare.col
                print(f"AI: I think the best possible move is {piece.name} from {boardCopy.convertToChessCoordinates(startRow,startCol)} to {boardCopy.convertToChessCoordinates(targetRow, targetCol)} with a resulting board evaluation of {max_eval}")
            
            return best_move