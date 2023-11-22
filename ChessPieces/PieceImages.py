import os
import sys
import contextlib

with open(os.devnull, 'w') as f, contextlib.redirect_stdout(f):
    import pygame
    pygame.init()

# Load in images
white_pawn_png = pygame.image.load('Images/Pieces/WhitePawnPNG.png')
black_pawn_png = pygame.image.load('Images/Pieces/BlackPawnPNG.png')
white_knight_png = pygame.image.load('Images/Pieces/WhiteKnightPNG.png')
black_knight_png = pygame.image.load('Images/Pieces/BlackKnightPNG.png')
white_rook_png = pygame.image.load('Images/Pieces/WhiteRookPNG.png')
black_rook_png = pygame.image.load('Images/Pieces/BlackRookPNG.png')
white_bishop_png = pygame.image.load('Images/Pieces/WhiteBishopPNG.png')
black_bishop_png = pygame.image.load('Images/Pieces/BlackBishopPNG.png')
white_queen_png = pygame.image.load('Images/Pieces/WhiteQueenPNG.png')
black_queen_png = pygame.image.load('Images/Pieces/BlackQueenPNG.png')
white_king_png = pygame.image.load('Images/Pieces/WhiteKingPNG.png')
black_king_png = pygame.image.load('Images/Pieces/BlackKingPNG.png')

piece_images = {
    "Pb": black_pawn_png,
    "Pw": white_pawn_png,
    "Nb": black_knight_png,
    "Nw": white_knight_png,
    "Rb": black_rook_png,
    "Rw": white_rook_png,
    "Bb": black_bishop_png,
    "Bw": white_bishop_png,
    "Qb": black_queen_png,
    "Qw": white_queen_png,
    "Kb": black_king_png,
    "Kw": white_king_png
}


# Scale images here, to avoid scaling them every time they are drawn
squareSize = 100  
for piece_code, img in piece_images.items():
    piece_images[piece_code] = pygame.transform.smoothscale(img, (squareSize, squareSize))
