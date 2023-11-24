import pygame
import os

from GlobalConstants import *
from BoardSquare import BoardSquare
from Move import Move


class Piece:
    def __init__(self, name, color, value: float, image=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'White' else -1
        self.value = value_sign * value
        self.moves = []
        self.moved = False
        self.set_image()
        self.texture_rect = texture_rect

    def set_image(self):
        imageString = os.path.join(
            f'assets/Images/Pieces/{self.color}{self.name}PNG.png'
        )
        image = pygame.image.load(imageString)

        self.image = pygame.transform.smoothscale(image, (squareSize, squareSize))
    
    def addMove(self, moves):
        self.moves.append(moves)

    def clearMoves(self):
        self.moves.clear()

class Pawn(Piece):

    def __init__(self, color: str):
        self.direction = -1 if color == 'White' else 1

    #TODO potential optimization here. Float could be replaced with int, potentially making MinMax faster
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
        super().__init__(name='King', color=color, value=10000.0)