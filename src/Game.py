import pygame
from ChessBoard import ChessBoard
from DragPiece import DragPiece

from GlobalConstants import *
from BoardSquare import BoardSquare


class Game:

    def __init__(self) -> None:
        self.board = ChessBoard()
        self.dragPiece = DragPiece()
        self.currentPlayer = 'White'
        self.hoveredSquare = None

    def drawChessBoard(self, surface) -> None:
        for row in range(boardSize):
            for col in range(boardSize):
                if (row + col) % 2 == 0:
                    color = pygame.Color("burlywood1")
                else:
                    color = pygame.Color("sienna4")

                square = (col * squareSize, row * squareSize, squareSize, squareSize)

                pygame.draw.rect(surface, color, square)

    def drawPieces(self, surface):
        for row in range(boardSize):
            for col in range(boardSize):
                if self.board.squares[row][col].hasPiece():
                    piece = self.board.squares[row][col].piece

                    # Draw all pieces except the one being dragged
                    if piece != self.dragPiece.piece:
                        # Pygame stuff to draw the piece
                        image = piece.image
                        imageCenter = col * squareSize + squareSize // 2, row * squareSize + squareSize // 2
                        piece.texture_rect = image.get_rect(center=imageCenter)
                        surface.blit(image, piece.texture_rect)

    def showMoves(self, surface):
        if self.dragPiece.isDragging:
            piece = self.dragPiece.piece

            # The color and size of the circle
            circle_color = (128, 128, 128, 128)  # RGBA for semi-transparent grey
            circle_radius = squareSize // 7  # Adjust the radius as needed

            capture_circle = (128, 128, 128, 128)
            capture_radius = squareSize // 2

            for move in piece.moves:
                # Create a temporary surface with alpha
                temp_surface = pygame.Surface((squareSize, squareSize), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, circle_color, (squareSize // 2, squareSize // 2), circle_radius)

                surface.blit(temp_surface, (move.end.col * squareSize, move.end.row * squareSize))
                #Draw a rectangle around the square if it has an emenyPiece
                if BoardSquare.hasEnemyPiece(self.board.squares[move.end.row][move.end.col], piece.color):
                    temp_surface = pygame.Surface((squareSize, squareSize), pygame.SRCALPHA)
                    #draw a ring around the square
                    pygame.draw.circle(temp_surface, capture_circle, (squareSize // 2, squareSize // 2), capture_radius, width=8)
                    surface.blit(temp_surface, (move.end.col * squareSize, move.end.row * squareSize))


    def showHoveredSquare(self, surface):
        if self.hoveredSquare:
            color = (180, 180, 180)
            square = (self.hoveredSquare.col * squareSize, self.hoveredSquare.row * squareSize, squareSize, squareSize)
            pygame.draw.rect(surface, color, square, width=4)

    def setHoveredSquare(self, row, col):
        if BoardSquare.isOnBoard(row, col):
            self.hoveredSquare = self.board.squares[row][col]

    def showLastMove(self, surface):
        if self.board.lastMove:
            first = self.board.lastMove.start
            last = self.board.lastMove.end
            light_color = (255, 178, 102, 128)
            dark_color = (170, 100, 35, 128)

            for pos in [first, last]:
                color = light_color if (pos.row + pos.col) % 2 == 0 else dark_color
                square = (pos.col * squareSize, pos.row * squareSize, squareSize, squareSize)
                pygame.draw.rect(surface, color, square)


    def nextTurn(self):
        self.currentPlayer = 'White' if self.currentPlayer == 'Black' else 'Black'
