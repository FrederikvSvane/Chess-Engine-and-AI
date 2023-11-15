class Rook:
    def __init__(self, color):
        self.color = color
        self.symbol = "R"

     # "Representation" of the piece. Used when debugging and to print the piece to the terminal.
    def __repr__(self):
        return self.symbol
