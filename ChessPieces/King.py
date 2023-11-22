class King:
    def __init__(self, color: str):
        self.color = color
        self.symbol = "K"

    def __repr__(self) -> str:
        return f"{self.symbol}{self.color[0]}"