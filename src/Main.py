import os
import sys
import contextlib
from Move import Move
from BoardSquare import BoardSquare
from GameBoarder import GameBoarder

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame

from GlobalConstants import *
from Game import Game


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.gameBoarder = GameBoarder(windowWidth + 2 * borderWidth, windowHeight + 2 * borderWidth)
        self.screen = pygame.display.set_mode((windowWidth + 2 * borderWidth, windowHeight + 2 * borderWidth))
        pygame.display.set_caption("Ultra Mega Chess 9000")
        self.game = Game()


    def mainloop(self) -> None:

        game = self.game
        board = game.board
        dragPiece = game.dragPiece

        # Game loop here. Big boy motherfucka
        while True:
            chessboard_surface = pygame.Surface((800, 800))
            game.drawChessBoard(chessboard_surface)
            game.showLastMove(chessboard_surface)
            game.showMoves(chessboard_surface)
            if dragPiece.isDragging:
                game.showHoveredSquare(chessboard_surface)
            game.drawPieces(chessboard_surface)

            # Draw piece on top of other stuff when dragging, to avoid clipping
            if dragPiece.isDragging:
                dragPiece.updateBlit(chessboard_surface)

            # Draw the chessboard surface onto the GameBoarder surface
            self.gameBoarder.draw_chessboard(chessboard_surface)
            self.screen.blit(self.gameBoarder.get_surface(), (0, 0))

            for event in pygame.event.get():

                # Drag logic                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragPiece.updateMouse(event.pos)

                    clickedRow = dragPiece.mouseY // squareSize
                    clickedCol = dragPiece.mouseX // squareSize

                    if BoardSquare.isOnBoard(clickedRow, clickedCol):
                        if board.squares[clickedRow][clickedCol].hasPiece():
                            piece = board.squares[clickedRow][clickedCol].piece

                            #Check if color of piece matches the player turn
                            if piece.color == game.currentPlayer:
                                board.possibleMoves(piece, clickedRow, clickedCol)
                                dragPiece.saveInitialPos(event.pos)
                                dragPiece.startDraggingPiece(piece)

                                game.drawChessBoard(chessboard_surface)
                                game.showMoves(chessboard_surface)
                                game.drawPieces(chessboard_surface)

                        # dragPiece.updateBlit(screen)

                if event.type == pygame.MOUSEMOTION:
                    row = event.pos[1] // squareSize
                    col = event.pos[0] // squareSize
                    game.setHoveredSquare(row, col)

                    if dragPiece.isDragging:
                        dragPiece.updateMouse(event.pos)
                        game.drawChessBoard(chessboard_surface)
                        game.showLastMove(chessboard_surface)
                        game.showMoves(chessboard_surface)
                        game.drawPieces(chessboard_surface)
                        game.showHoveredSquare(chessboard_surface)
                        dragPiece.updateBlit(chessboard_surface)

                if event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragPiece.isDragging:
                        dragPiece.updateMouse(event.pos)
                        chosenRow = dragPiece.mouseY // squareSize
                        chosenCol = dragPiece.mouseX // squareSize



                        if BoardSquare.isOnBoard(chosenRow, chosenCol):
                            startSquare = board.squares[dragPiece.initialRow][dragPiece.initialCol]
                            endSquare = board.squares[chosenRow][chosenCol]
                            move = Move(startSquare, endSquare)

                            if board.validMove(dragPiece.piece, move):
                                board.movePiece(dragPiece.piece, move)

                            #After making the move, draw the pieces
                                game.nextTurn()
                            game.drawChessBoard(chessboard_surface)
                            game.showLastMove(chessboard_surface)
                            game.drawPieces(chessboard_surface)

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
