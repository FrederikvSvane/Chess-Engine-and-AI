import pygame


def start_menu(config):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Ultra Mega Chess 9000 - Menu")
    clock = pygame.time.Clock()

    # Fonts
    font = pygame.font.SysFont(None, 32)
    welcome_font = pygame.font.SysFont(None, 48)

    # Welcome Text
    welcome_text = welcome_font.render("Welcome to Ultra Mega Chess 9000", True, pygame.Color('white'))
    welcome_rect = welcome_text.get_rect(center=(400, 50))

    # Input Boxes
    input_box1 = pygame.Rect(300, 150, 200, 32)
    input_box2 = pygame.Rect(300, 200, 200, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    active_box = None
    text1 = ''
    text2 = ''

    # Start Button
    button = pygame.Rect(300, 300, 200, 50)
    button_color = pygame.Color('gray15')

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_box = input_box1
                elif input_box2.collidepoint(event.pos):
                    active_box = input_box2
                else:
                    active_box = None

                if button.collidepoint(event.pos):
                    config.player1_name = text1
                    config.player2_name = text2
                    return True

                color1 = color_active if active_box == input_box1 else color_inactive
                color2 = color_active if active_box == input_box2 else color_inactive

            if event.type == pygame.KEYDOWN:
                if active_box == input_box1:
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif active_box == input_box2:
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        screen.fill((30, 30, 30))

        # Welcome Text
        screen.blit(welcome_text, welcome_rect)

        # Input Labels
        player1_label = font.render("Enter Player 1:", True, pygame.Color('white'))
        player2_label = font.render("Enter Player 2:", True, pygame.Color('white'))
        screen.blit(player1_label, (input_box1.x, input_box1.y - 30))
        screen.blit(player2_label, (input_box2.x, input_box2.y - 30))

        # Input Boxes
        txt_surface1 = font.render(text1, True, color1)
        txt_surface2 = font.render(text2, True, color2)
        width1 = max(200, txt_surface1.get_width() + 10)
        input_box1.w = width1
        width2 = max(200, txt_surface2.get_width() + 10)
        input_box2.w = width2
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
        screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)

        # Start Button
        pygame.draw.rect(screen, button_color, button)
        button_text = font.render("Start Game", True, pygame.Color('white'))
        screen.blit(button_text, (button.x + 50, button.y + 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return False
