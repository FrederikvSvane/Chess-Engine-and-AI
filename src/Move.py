class Move:

    def __init__(self, start, end):
        #These are tuples of (row, col)
        self.start = start
        self.end = end

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end