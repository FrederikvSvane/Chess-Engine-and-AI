import os
import sys
import contextlib
from Move import Move
from src.BoardSquare import BoardSquare

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame

from GlobalConstants import *
from Game import Game


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((windowWidth, windowHeight))
        pygame.display.set_caption("Ultra Mega Chess 9000")
        self.game = Game()

    def mainloop(self) -> None:

        game = self.game
        board = game.board
        screen = self.screen
        dragPiece = game.dragPiece

        # Game loop here. Big boy motherfucka
        while True:
            game.drawChessBoard(screen)
            game.showLastMove(screen)
            game.showMoves(screen)
            if dragPiece.isDragging:
                game.showHoveredSquare(screen)
            game.drawPieces(screen)

            # Draw piece on top of other stuff when dragging, to avoid clipping
            if dragPiece.isDragging:
                dragPiece.updateBlit(screen)

            for event in pygame.event.get():

                # Drag logic                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragPiece.updateMouse(event.pos)

                    clickedRow = dragPiece.mouseY // squareSize
                    clickedCol = dragPiece.mouseX // squareSize

                    if board.squares[clickedRow][clickedCol].hasPiece():
                        piece = board.squares[clickedRow][clickedCol].piece

                        #Check if color of piece matches the player turn
                        if piece.color == game.currentPlayer:
                            board.possibleMoves(piece, clickedRow, clickedCol)
                            dragPiece.saveInitialPos(event.pos)
                            dragPiece.startDraggingPiece(piece)

                            game.drawChessBoard(screen)
                            game.showMoves(screen)
                            game.drawPieces(screen) 

                        # dragPiece.updateBlit(screen)

                if event.type == pygame.MOUSEMOTION:
                    row = event.pos[1] // squareSize
                    col = event.pos[0] // squareSize
                    game.setHoveredSquare(row, col)

                    if dragPiece.isDragging:
                        dragPiece.updateMouse(event.pos)
                        game.drawChessBoard(screen)
                        game.showLastMove(screen)
                        game.showMoves(screen)
                        game.drawPieces(screen)
                        game.showHoveredSquare(screen)
                        dragPiece.updateBlit(screen)

                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragPiece.isDragging:
                        dragPiece.updateMouse(event.pos)
                        chosenRow = dragPiece.mouseY // squareSize
                        chosenCol = dragPiece.mouseX // squareSize

                        startSquare = board.squares[dragPiece.initialRow][dragPiece.initialCol]

                        if BoardSquare.isOnBoard(chosenRow, chosenCol):
                            endSquare = board.squares[chosenRow][chosenCol]
                            move = Move(startSquare, endSquare)

                            if board.validMove(dragPiece.piece, move):
                                board.movePiece(dragPiece.piece, move)

                            #After making the move, draw the pieces
                                game.nextTurn()
                            game.drawChessBoard(screen)
                            game.showLastMove(screen)
                            game.drawPieces(screen)

                        dragPiece.piece.clearMoves()
                    
                    dragPiece.stopDraggingPiece()


                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update relevant parts of display (defaults to all/whole display)
            pygame.display.update()


main = Main()
main.mainloop()
