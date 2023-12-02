from GlobalConstants import *

class Piece:
    def __init__(self, name, color, value: float, image=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'White' else -1
        self.value = value_sign * value
        self.moves = []
        self.moved = False
        self.imageKey = f"{color}{name}"
        self.texture_rect = texture_rect

    def draw(self, screen, col, row):
        image = Images[self.imageKey]
        imageCenter = col * squareSize + squareSize // 2, row * squareSize + squareSize // 2
        self.texture_rect = image.get_rect(center=imageCenter)
        screen.blit(image, self.texture_rect)
    
    def addMove(self, moves):
        self.moves.append(moves)

    def clearMoves(self):
        self.moves.clear()

class Pawn(Piece):

    def __init__(self, color: str):
        self.direction = -1 if color == 'White' else 1
        self.enPassant = False
        #TODO: potential optimization here. Float could be replaced with int, potentially making MinMax faster
        super().__init__(name='Pawn', color=color, value=1.0)



# Making all the pieces

class Knight(Piece):
    def __init__(self, color: str):
        super().__init__(name='Knight', color=color, value=3.0)

class Bishop(Piece):
    def __init__(self, color: str):
        super().__init__(name='Bishop', color=color, value=3.0)


class Rook(Piece):
    def __init__(self, color: str):
        super().__init__(name='Rook', color=color, value=5.0)


class Queen(Piece):
    def __init__(self, color: str):
        super().__init__(name='Queen', color=color, value=9.0)


class King(Piece):
    def __init__(self, color: str):
        self.leftRook = None
        self.rightRook = None
        super().__init__(name='King', color=color, value=10000.0)
