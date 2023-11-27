import pygame
from ChessBoard import ChessBoard
from DragPiece import DragPiece

from GlobalConstants import *
from BoardSquare import BoardSquare


class Game:

    def __init__(self, config) -> None:
        self.board = ChessBoard()
        self.dragPiece = DragPiece()
        self.currentPlayer = 'White'
        self.hoveredSquare = None
        self.player1_time = config.start_time
        self.player2_time = config.start_time
        self.player1_name = config.player1_name
        self.player2_name = config.player2_name
        self.timerUpdate = pygame.time.get_ticks()

    def drawChessBoard(self, surface) -> None:
        for row in range(boardSize):
            for col in range(boardSize):
                if (row + col) % 2 == 0:
                    color = pygame.Color("burlywood1")
                else:
                    color = pygame.Color("sienna4")

                square = (col * squareSize, row * squareSize, squareSize, squareSize)

                pygame.draw.rect(surface, color, square)


                #TODO this code works, but it makes the game lag alot. Maybe find a better way to do this
                #Show coordinates on the board
                # if col == 0:
                #     color = pygame.Color("burlywood1") if row % 2 != 0 else pygame.Color("sienna4")
                #     font = pygame.font.SysFont('monospace', 18, bold=True)
                #     label = font.render(str(abs(row-8)), True, color)
                #     surface.blit(label, (0, row * squareSize))
                # if row == 7:
                #     color = pygame.Color("burlywood1") if col % 2 == 0 else pygame.Color("sienna4")
                #     font = pygame.font.SysFont('monospace', 18, bold=True)
                #     label = font.render(BoardSquare.getColumnLetter((col)), True, color)
                #     surface.blit(label, (col * squareSize + squareSize - 14, windowHeight - 18))

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

    def resetGame(self,config):
        self.__init__(config)

    def update_timer(self):
        if GlobalConstants.gameStarted:
            current_time = pygame.time.get_ticks()
            if self.currentPlayer == 'Black' and current_time - self.timerUpdate >= 1000:
                self.player1_time -= 1
                self.timerUpdate = current_time
            elif self.currentPlayer == 'White' and current_time - self.timerUpdate >= 1000:
                self.player2_time -= 1
                self.timerUpdate = current_time

