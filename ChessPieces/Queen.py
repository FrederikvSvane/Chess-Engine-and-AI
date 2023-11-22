class Queen:
    def __init__(self, color: str):
        self.color = color
        self.symbol = "Q"
        
    def __repr__(self):
        return f"{self.symbol}{self.color[0]}"
