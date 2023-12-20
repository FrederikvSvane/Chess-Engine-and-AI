import copy

class ChessAI:
    def __init__(self, board, depth):
        self.board = board
        self.depth = depth

    def evaluate_board(self):
        # TODO: Implement a function that evaluates the board and returns a score
        pass

    def minmax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.isGameOver():
            return self.evaluate_board()

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.board.getAllPossibleMoves('Black'):
                self.board.makeMove(move)
                eval = self.minmax(depth - 1, alpha, beta, False)
                self.board.undoMove(move)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.board.getAllPossibleMoves('White'):
                self.board.makeMove(move)
                eval = self.minmax(depth - 1, alpha, beta, True)
                self.board.undoMove(move) # TODO: implementer undo move funktionen. Det er bedst sådan. EDIT: Second thought så er det overhovedet ikke bedst at bruge undo move her, brug et deep copy board. Men implementer undo move alligevel
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def find_best_move(self):
        boardCopy = copy.deepcopy(self.board)
        max_eval = float('-inf')
        best_move = None
        for move in boardCopy.getAllPossibleMoves('Black'):
            boardCopy.makeMove(move)
            eval = self.minmax(self.depth - 1, float('-inf'), float('inf'), False)
            self.board.undoMove(move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return best_move