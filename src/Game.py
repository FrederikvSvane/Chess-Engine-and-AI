import pygame
from ChessBoard import ChessBoard
from DragPiece import DragPiece

from GlobalConstants import *

class Game:

    def __init__(self) -> None:
        self.board = ChessBoard()
        self.dragPiece = DragPiece()


    def drawChessBoard(self, surface) -> None:
        for row in range(boardSize):
            for col in range(boardSize):
                if(row + col) % 2 == 0:
                    color = pygame.Color("burlywood1")
                else:
                    color = pygame.Color("sienna4")

                square =  (col * squareSize, row * squareSize, squareSize, squareSize)

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

            for move in piece.moves:
                color = pygame.Color("yellow") if (move.end.row + move.end.col) % 2 == 0 else pygame.Color("orange")
                square = (move.end.col * squareSize, move.end.row * squareSize, squareSize, squareSize)
                pygame.draw.rect(surface, color, square)


                
