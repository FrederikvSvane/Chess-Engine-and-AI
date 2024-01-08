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


# Board heuristics
    
whitePawnScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

whiteKnightScores = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

whiteBishopScores = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

whiteRookScores = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

whiteQueenScores = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

whiteKingMiddleGameScores = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]

whiteKingEndGameScores = [
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]
]

def flip_and_invert_scores(scores):
    flipped_scores = [row[::-1] for row in scores[::-1]]  # Flip the array 180 degrees
    return [[-score for score in row] for row in flipped_scores]  # Invert the sign of each score


blackPawnScores = flip_and_invert_scores(whitePawnScores)
blackKnightScores = flip_and_invert_scores(whiteKnightScores)
blackBishopScores = flip_and_invert_scores(whiteBishopScores)
blackRookScores = flip_and_invert_scores(whiteRookScores)
blackQueenScores = flip_and_invert_scores(whiteQueenScores)
blackKingMiddleGameScores = flip_and_invert_scores(whiteKingMiddleGameScores)
blackKingEndGameScores = flip_and_invert_scores(whiteKingEndGameScores)




