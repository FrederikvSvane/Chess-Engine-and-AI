import pygame

pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)

# Size of squares and board
squareSize = 60  # Size of each square
boardSize = 8  # 8x8 board
windowSize = [squareSize * boardSize, squareSize * boardSize]

# Set up the drawing window (size depends on the board size and square size)
screen = pygame.display.set_mode(windowSize, pygame.RESIZABLE)

# Title and Icon
pygame.display.set_caption("Chess")

def draw_chess_board(screen):
    colors = [pygame.Color("burlywood1"), pygame.Color("sienna4")]
    for row in range(boardSize):
        for col in range(boardSize):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, (col * squareSize, row * squareSize, squareSize, squareSize))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    
    screen.fill(pygame.Color("grey24"))

    draw_chess_board(screen)
    pygame.display.flip()




