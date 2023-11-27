import os
import sys
import contextlib
from Move import Move
from BoardSquare import BoardSquare

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame

from GlobalConstants import *
from Game import Game
from GameBoarder import GameBoarder


class Main:
    def __init__(self) -> None:
        pygame.init()
        self.gameBoarder = GameBoarder(windowWidthWithBorder, windowHeightWithBorder)
        self.screen = pygame.display.set_mode(self.gameBoarder.get_surface().get_size())
        pygame.display.set_caption("Ultra Mega Chess 9000")
        self.game = Game()
        self.offset_x = BORDER_WIDTH
        self.offset_y = BORDER_HEIGHT

    def mainloop(self) -> None:
        game = self.game
        board = game.board
        dragPiece = self.game.dragPiece

        while True:
            chessboard_surface = pygame.Surface((chessBoardWidth, chessBoardHeight))
            game.drawChessBoard(chessboard_surface)
            game.showLastMove(chessboard_surface)
            game.showMoves(chessboard_surface)
            self.gameBoarder.draw_player_info("Player 1", "Player 2", chessboard_surface)
            if dragPiece.isDragging:
                game.showHoveredSquare(chessboard_surface)
            game.drawPieces(chessboard_surface)

            if dragPiece.isDragging:
                dragPiece.updateBlit(chessboard_surface)

            self.gameBoarder.draw_chessboard(chessboard_surface)
            self.screen.blit(self.gameBoarder.get_surface(), (0, 0))

            for event in pygame.event.get():
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
                    # Adjust the mouse position for the border offset
                    event_pos_with_offset = (event.pos[0] - self.offset_x, event.pos[1] - self.offset_y)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragPiece.updateMouse(event_pos_with_offset)
                    clickedRow, clickedCol = dragPiece.mouseY // squareSize, dragPiece.mouseX // squareSize

                    if board.squares[clickedRow][clickedCol].hasPiece():
                        piece = board.squares[clickedRow][clickedCol].piece
                        if piece.color == game.currentPlayer:
                            board.possibleMoves(piece, clickedRow, clickedCol)
                            dragPiece.saveInitialPos(event_pos_with_offset)
                            dragPiece.startDraggingPiece(piece)

                if event.type == pygame.MOUSEMOTION:
                    dragPiece.updateMouse(event_pos_with_offset)
                    hoveredRow, hoveredCol = dragPiece.mouseY // squareSize, dragPiece.mouseX // squareSize

                     # Call setHoveredSquare with the hovered row and column
                    game.setHoveredSquare(hoveredRow, hoveredCol)
                    if dragPiece.isDragging:
                        game.drawChessBoard(chessboard_surface)
                        game.showMoves(chessboard_surface)
                        game.drawPieces(chessboard_surface)
                        game.showHoveredSquare(chessboard_surface)
                        dragPiece.updateBlit(chessboard_surface)

                if event.type == pygame.MOUSEBUTTONUP:
                    if dragPiece.isDragging:
                        dragPiece.updateMouse(event_pos_with_offset)
                        chosenRow, chosenCol = dragPiece.mouseY // squareSize, dragPiece.mouseX // squareSize
                        startSquare = board.squares[dragPiece.initialRow][dragPiece.initialCol]
                        

                        if BoardSquare.isOnBoard(chosenRow, chosenCol):
                            endSquare = board.squares[chosenRow][chosenCol]
                            move = Move(startSquare, endSquare)
                            if board.validMove(dragPiece.piece, move):
                                board.movePiece(dragPiece.piece, move)
                                game.nextTurn()

                        dragPiece.piece.clearMoves()
                    dragPiece.stopDraggingPiece()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.resetGame()
                        game = self.game
                        board = game.board
                        dragPiece = game.dragPiece

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

main = Main()
main.mainloop()