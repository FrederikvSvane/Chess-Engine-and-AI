import os
import random
import sys
import contextlib
from Move import Move
from BoardSquare import BoardSquare
from Pieces import Pawn
from AI import ChessAI

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
        self.AI = ChessAI(self.game.board, 4)

    def mainloop(self) -> None:

        game = self.game
        board = self.game.board
        screen = self.screen
        dragPiece = self.game.dragPiece
        AI = self.AI

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
                            board.possibleMoves(piece, clickedRow, clickedCol, normalCall=True)
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
                            targetSquare = board.squares[chosenRow][chosenCol]
                            move = Move(startSquare, targetSquare)

                            if board.validMove(dragPiece.piece, move):
                                board.movePiece(dragPiece.piece, move)

                                #If an en passant move was just made, set the enPassant flag to true. Otherwise, set it to false
                                board.setEnPassantTrue(dragPiece.piece)
                                
                                #Change the player turn, and check if the other player is in checkmate
                                game.nextTurn()

                                if board.isInCheckmate(game.currentPlayer):
                                    print(f"{game.currentPlayer} is in checkmate")
                                    # End screen kan blive indsat lige her :D

                            #After making the move, draw the pieces
                            game.drawChessBoard(screen)
                            game.showLastMove(screen)
                            game.drawPieces(screen)

                        dragPiece.piece.clearMoves()
                    
                    dragPiece.stopDraggingPiece()

                # Making an AI make a move. Right now, the AI can only play as black
                if game.currentPlayer == 'Black':
                    AImove = AI.findBestMove()

                    if AImove:
                        AIpiece = board.squares[AImove.startSquare.row][AImove.startSquare.col].piece
                        if AIpiece:
                            board.movePiece(AIpiece, AImove)
                            game.nextTurn()

                        game.drawChessBoard(screen)
                        game.showLastMove(screen)
                        game.drawPieces(screen)

                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.resetGame()
                        game = self.game
                        board = self.game.board
                        AI = ChessAI(board, 4)
                        dragPiece = self.game.dragPiece
                    
                    if event.key == pygame.K_z:
                        if board.allMoves:
                            board.undoMove(playSound=True)
                            game.nextTurn()
                            game.drawChessBoard(screen)
                            game.showLastMove(screen)
                            game.drawPieces(screen)

                # Quit game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Update relevant parts of display (defaults to all/whole display)
            pygame.display.update()

main = Main()
main.mainloop()
