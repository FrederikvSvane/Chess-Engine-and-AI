class Rook:
    def __init__(self, color: str):
        self.color = color
        self.symbol = "R"

    def __repr__(self):
        return f"{self.symbol}{self.color[0]}"
