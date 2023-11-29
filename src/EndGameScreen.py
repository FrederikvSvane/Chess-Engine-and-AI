import pygame

from StartMenu import start_menu
from Game import Game

def EndGameScreen(config):
    pygame.init()
    game = Game(config)
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ultra Mega Chess 9000 - EndGame")

    # Fonts
    font = pygame.font.SysFont(None, 32)
    welcome_font = pygame.font.SysFont(None, 48)

    # Welcome Text
    welcome_text = welcome_font.render("Welcome to Ultra Mega Chess 9000", True, pygame.Color('white'))
    welcome_rect = welcome_text.get_rect(center=(400, 50))

    # Start Button
    button = pygame.Rect(300, 300, 200, 50)
    button_color = pygame.Color('gray15')
    button_text = font.render("Start New Game", True, pygame.Color('white'))

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    return True

        screen.fill((30, 30, 30))

        # Welcome Text
        screen.blit(welcome_text, welcome_rect)

        # Button and Button Text
        pygame.draw.rect(screen, button_color, button)
        screen.blit(button_text, (button.x + 50, button.y + 10))

        pygame.display.flip()

    pygame.quit()
    return False
