class Move:

    def __init__(self, startSquare, targetSquare):
        #These are tuples of (row, col)
        self.startSquare = startSquare
        self.targetSquare = targetSquare

    def __eq__(self, other):
        return self.startSquare == other.startSquare and self.targetSquare == other.targetSquare