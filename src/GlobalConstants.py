import pygame

# Set window dimensions
windowWidth = 800
windowHeight = 800

# Set board dimension
boardSize = 8
squareSize = windowWidth // boardSize

letters = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}

Images = {
    'WhitePawn': pygame.image.load('assets/Images/Pieces/WhitePawnPNG.png'),
    'WhiteRook': pygame.image.load('assets/Images/Pieces/WhiteRookPNG.png'),
    'WhiteKnight': pygame.image.load('assets/Images/Pieces/WhiteKnightPNG.png'),
    'WhiteBishop': pygame.image.load('assets/Images/Pieces/WhiteBishopPNG.png'),
    'WhiteQueen': pygame.image.load('assets/Images/Pieces/WhiteQueenPNG.png'),
    'WhiteKing': pygame.image.load('assets/Images/Pieces/WhiteKingPNG.png'),
    'BlackPawn': pygame.image.load('assets/Images/Pieces/BlackPawnPNG.png'),
    'BlackRook': pygame.image.load('assets/Images/Pieces/BlackRookPNG.png'),
    'BlackKnight': pygame.image.load('assets/Images/Pieces/BlackKnightPNG.png'),
    'BlackBishop': pygame.image.load('assets/Images/Pieces/BlackBishopPNG.png'),
    'BlackQueen': pygame.image.load('assets/Images/Pieces/BlackQueenPNG.png'),
    'BlackKing': pygame.image.load('assets/Images/Pieces/BlackKingPNG.png'),
}

# Smoothscale images to fit the squares
for key in Images:
    Images[key] = pygame.transform.smoothscale(Images[key], (squareSize, squareSize))

