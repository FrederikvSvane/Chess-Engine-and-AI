import os
import sys
import contextlib
import ChessBoard
from ChessPieces.PieceImages import piece_images

# Redirect stdout to null temporarily, such that pygame doesn't print to console
with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame
    pygame.init()


# Size of squares and board
squareSize = 100  # Size of each square
boardSize = 8  # 8x8 board
windowSize = [squareSize * boardSize, squareSize * boardSize]

# Set up the drawing window (size depends on the board size and square size)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)

# Title and Icon
pygame.display.set_caption("Ultra Mega Chess 9000")

# Initialize the board
chessBoard = ChessBoard.ChessBoard()


def draw_chess_board(screen):
    colors = [pygame.Color("burlywood1"), pygame.Color("sienna4")]
    for row in range(boardSize):
        for col in range(boardSize):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * squareSize, row * squareSize, squareSize, squareSize))
            piece = chessBoard.board[row][col]
            if piece is not None:
                piece_code = repr(piece)
                if piece_code in piece_images:
                    piece_image = piece_images[piece_code]
                    screen.blit(piece_image, (col * squareSize, row * squareSize))
                else:
                    print(f"Error: No image found for piece code '{piece_code}'")
    pygame.display.flip()


def draw_square(row, col):
    # Determine the color of the square
    if (row + col) % 2 == 0:
        color = pygame.Color("burlywood1")
    else:
        color = pygame.Color("sienna4")

    # Draw the square
    pygame.draw.rect(screen, color, pygame.Rect(col * squareSize, row * squareSize, squareSize, squareSize))

    # Draw the piece on the square, if there is one
    piece = chessBoard.board[row][col]
    if piece is not None:
        piece_code = repr(piece)
        if piece_code in piece_images:
            piece_image = piece_images[piece_code]
            # Resize image to fit the square
            piece_image = pygame.transform.smoothscale(piece_image, (squareSize, squareSize))
            screen.blit(piece_image, (col * squareSize, row * squareSize))




running: bool = True
selected_piece = None
selected_piece_position = None
screen.fill(pygame.Color("grey24"))
draw_chess_board(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            draw_chess_board(screen)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // squareSize
            row = y // squareSize
            clicked_square = chessBoard.board[row][col]
            if clicked_square is not None and selected_piece is None:
                # Pick up the piece
                selected_piece = clicked_square
                selected_piece_position = (row, col)
                chessBoard.board[row][col] = None
            elif clicked_square is None and selected_piece is not None:
                # Put down the piece
                chessBoard.board[row][col] = selected_piece
                selected_piece = None
                selected_piece_position = None

    if selected_piece is not None:
        # Draw the selected piece at the cursor position
        x, y = pygame.mouse.get_pos()
        piece_code = repr(selected_piece)
        if piece_code in piece_images:
            piece_image = piece_images[piece_code]
            piece_image = pygame.transform.smoothscale(piece_image, (squareSize, squareSize))
            draw_chess_board(screen)
            screen.blit(piece_image, (x - squareSize // 2, y - squareSize // 2))

    pygame.display.flip()

pygame.quit()











# ------------------ TESTING GAME IN TERMINAL ------------------

# board = ChessBoard.ChessBoard()

# running: bool = True
# turn: int = 1
# currentPlayer: str = "White"
# board.printBoard()

# while running:
#     if(turn % 2 == 1):
#         print("\n \n > White's turn!")
#         currentPlayer = "White"
#     else:
#         print("\n \n > Black's turn!")
#         currentPlayer = "Black"
#     print(f"\n \n > {currentPlayer}, please enter the position of the piece you want to move (e2 for example)")
#     start = input()
#     print(f"\n \n > {currentPlayer}, please enter the position of the square you want to move to (e4 for example)")
#     end = input()
#     board.makeMove(start, end)
#     board.printBoard()
#     turn += 1
#     if(turn > 4):
#         running = False
#         print("Game over!")

# --------------------------------------------------------------