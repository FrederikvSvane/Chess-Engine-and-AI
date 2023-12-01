import os
import random
import sys
import contextlib

from Move import Move
from BoardSquare import BoardSquare
from Pieces import Pawn
from GameConfig import *
from StartMenu import start_menu

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame

from GlobalConstants import *
from Game import Game
from GameBoarder import GameBoarder
from EndGameScreen import EndGameScreen

# Set the position of the window
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (500, 100)


class Main:
    def __init__(self):
        # Logic for initializing the game after the start menu
        self.offset_y = None
        self.offset_x = None
        self.game = None
        self.gameBoarder = None
        self.screen = None
        self.config = GameConfig()
        self.start_new_game()

    def start_new_game(self):
        if start_menu(self.config):
            pygame.init()
            self.gameBoarder = GameBoarder(windowWidthWithBorder, windowHeightWithBorder)
            self.screen = pygame.display.set_mode(self.gameBoarder.get_surface().get_size())
            pygame.display.set_caption("Ultra Mega Chess 9000")
            self.game = Game(self.config)
            self.offset_x = BORDER_WIDTH
            self.offset_y = BORDER_HEIGHT
            self.mainloop()
        else:
            pygame.quit()

    def mainloop(self) -> None:

        game = self.game
        board = game.board
        dragPiece = self.game.dragPiece
        game.board.isFirstMoveOver = False
        GlobalConstants.gameStarted = False

        # Game loop here. Big boy motherfucka
        while True:
            # Draw the chessboard and pieces
            chessboard_surface = pygame.Surface((chessBoardWidth, chessBoardHeight))
            game.drawChessBoard(chessboard_surface)
            game.showLastMove(chessboard_surface)
            game.showMoves(chessboard_surface)

            # Draw the player names and images
            game.update_timer()
            self.gameBoarder.draw_score_bar(chessboard_surface, board)
            self.gameBoarder.draw_player_info(self.game.player1_name, self.game.player2_name, chessboard_surface)

            # Logic for showing square that is hovered over
            if dragPiece.isDragging:
                game.showHoveredSquare(chessboard_surface)
            game.drawPieces(chessboard_surface)

            # Updating the dragged piece
            if dragPiece.isDragging:
                dragPiece.updateBlit(chessboard_surface)

            # Draws the chessBoard on the background and draws the timer
            self.gameBoarder.draw_chessboard(chessboard_surface)
            self.gameBoarder.draw_and_update_timer(chessboard_surface, game.player1_time, game.player2_time)
            self.screen.blit(self.gameBoarder.get_surface(), (0, 0))

            # Makes sure the mouse position is adjusted for the border offset
            for event in pygame.event.get():
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP):
                    # Adjust the mouse position for the border offset
                    event_pos_with_offset = (event.pos[0] - self.offset_x, event.pos[1] - self.offset_y)

                # Clicking the mouse button and holding it down
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragPiece.updateMouse(event_pos_with_offset)
                    clickedRow, clickedCol = dragPiece.mouseY // squareSize, dragPiece.mouseX // squareSize
                    if BoardSquare.isOnBoard(clickedRow, clickedCol):
                        if board.squares[clickedRow][clickedCol].hasPiece():
                            piece = board.squares[clickedRow][clickedCol].piece
                            if piece.color == game.currentPlayer:
                                board.possibleMoves(piece, clickedRow, clickedCol)
                                dragPiece.saveInitialPos(event_pos_with_offset)
                                dragPiece.startDraggingPiece(piece)

                # Moving the mouse around while holding down the mouse button
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

                # Letting go of the mouse button
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
                                self.gameBoarder.draw_score_bar(chessboard_surface, board)

                                # If an en passant move was just made, set the enPassant flag to true. Otherwise, set it to false
                                board.setEnPassantTrue(dragPiece.piece)

                                # Change the player turn, and check if the other player is in checkmate
                                game.nextTurn()

                                if board.isInCheckmate(game.currentPlayer):
                                    print(f"{game.currentPlayer} is in checkmate")
                                    if EndGameScreen(self.config):
                                        self.start_new_game()

                            # After making the move, draw the pieces
                            game.drawChessBoard(chessboard_surface)
                            game.showLastMove(chessboard_surface)
                            game.drawPieces(chessboard_surface)

                        dragPiece.piece.clearMoves()
                    dragPiece.stopDraggingPiece()

                if self.config.AI:
                    # Making an AI make a move. Right now, the AI can only play as black
                    if game.currentPlayer == 'Black':
                        allMoves = board.getAllPossibleMoves(game.currentPlayer)
                        if allMoves:
                            # move = board.MinMax(allMoves)
                            AImove = random.choice(allMoves)
                            AIpiece = board.squares[AImove.startSquare.row][AImove.startSquare.col].piece
                            if AIpiece:
                                board.movePiece(AIpiece, AImove)
                                game.nextTurn()

                            game.drawChessBoard(chessboard_surface)
                            game.showLastMove(chessboard_surface)
                            game.drawPieces(chessboard_surface)


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.resetGame(self.config)
                        game = self.game
                        board = game.board
                        dragPiece = game.dragPiece
                        self.gameBoarder.draw_score_bar(chessboard_surface, board)

                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update relevant parts of display (defaults to all/whole display)
            pygame.display.update()


if __name__ == "__main__":
    main = Main()
