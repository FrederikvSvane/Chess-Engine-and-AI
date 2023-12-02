import pygame

from StartMenu import start_menu
from Game import Game
from GameConfig import GameConfig


def EndGameScreen(config):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ultra Mega Chess 9000 - EndGame")

    # Fonts
    font = pygame.font.SysFont(None, 32)
    welcome_font = pygame.font.SysFont(None, 48)

    # Welcome Text
    welcome_text = welcome_font.render("Welcome to Ultra Mega Chess 9000", True, pygame.Color('white'))
    welcome_rect = welcome_text.get_rect(center=(400, 50))

    # Start Button
    start_menu_button = pygame.Rect(screen.get_width() - 500, screen.get_height() - 150, 250, 50)
    start_menu_button_color = pygame.Color('gray15')

    #restart buttom
    play_again_button = pygame.Rect(screen.get_width() - 500, screen.get_height() - 250, 250, 50)
    play_again_button_color = pygame.Color('gray15')

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_menu_button.collidepoint(event.pos):
                    return 'start_new'
                if play_again_button.collidepoint(event.pos):
                    return 'restart'
        screen.fill((30, 30, 30))

        # Welcome Text
        screen.blit(welcome_text, welcome_rect)

        # Draw Start Menu Button and center its text
        pygame.draw.rect(screen, start_menu_button_color, start_menu_button)
        text_surface = font.render("Start New Game", True, pygame.Color('white'))
        # Calculate text position
        text_x = start_menu_button.x + (start_menu_button.width - text_surface.get_width()) // 2
        text_y = start_menu_button.y + (start_menu_button.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))

        # Draw Play Again Button and center its text
        pygame.draw.rect(screen, play_again_button_color, play_again_button)
        restart_text_surface = font.render("Restart Game", True, pygame.Color('white'))
        # Calculate text position
        restart_text_x = play_again_button.x + (play_again_button.width - restart_text_surface.get_width()) // 2
        restart_text_y = play_again_button.y + (play_again_button.height - restart_text_surface.get_height()) // 2
        screen.blit(restart_text_surface, (restart_text_x, restart_text_y))

        pygame.display.flip()

    pygame.quit()
    return 'quit'
