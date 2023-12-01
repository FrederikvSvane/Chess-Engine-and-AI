import pygame
import re

def validate_time_format(time_str):
    """ Check if the time is in MM:SS format """
    return re.match(r'^\d{2}:\d{2}$', time_str) is not None
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
    input_box1 = pygame.Rect(screen.get_width() - 750, screen.get_height() - 450, 250, 50)
    input_box2 = pygame.Rect(screen.get_width() - 750, screen.get_height() - 350, 250, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color1 = color_inactive
    color2 = color_inactive
    active_box = None
    pvp_active = True  # PVP is active by default
    pva_active = False
    text1 = 'Enter name'
    text2 = 'Enter name'

    timer_box = pygame.Rect(screen.get_width() - 750, screen.get_height() - 250, 250, 50)
    timer_box_color = color_inactive
    text3 = '10:00'  # Default time
    active_box = None

    # Start Button
    start_button = pygame.Rect(screen.get_width() - 500, screen.get_height() - 150, 200, 50)
    start_button_color = pygame.Color('gray15')

    # Pvp button
    pvp_button = pygame.Rect(screen.get_width() - 300, screen.get_height() - 450, 250, 50)
    pvp_button_color = pygame.Color('gray15')

    # Player vs AI button
    pva_button = pygame.Rect(screen.get_width() - 300, screen.get_height() - 350, 250, 50)
    pva_button_color = pygame.Color('gray15')

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_box = input_box1
                    if text1 == 'Enter name':
                        text1 = ''
                    if text2.strip() == '':
                        text2 = 'Enter name'
                elif input_box2.collidepoint(event.pos):
                    active_box = input_box2
                    if text2 == 'Enter name':
                        text2 = ''
                    if text1.strip() == '':
                        text1 = 'Enter name'
                else:
                    active_box = None
                    if text1 == '':
                        text1 = 'Enter name'
                    if text2 == '':
                        text2 = 'Enter name'

                if timer_box.collidepoint(event.pos):
                    active_box = timer_box
                    if text3 == '10:00':  # Default time text
                        text3 = ''
                else:
                    if text3.strip() == '':
                        text3 = '10:00'  # Reset to default time if empt

                if start_button.collidepoint(event.pos):
                    # Validate time format
                    if not validate_time_format(text3):
                        print("Invalid time format. Please enter time in MM:SS format.")
                        continue  # Skip the rest of the loop and do not start the game

                    # If time format is valid, configure the game settings
                    config.player1_name = text1
                    config.player2_name = text2
                    config.start_time = text3  # Assuming your config can store this
                    return True  # Start the game

                color1 = color_active if active_box == input_box1 else color_inactive
                color2 = color_active if active_box == input_box2 else color_inactive

                if pvp_button.collidepoint(event.pos):
                    pvp_active = True
                    pva_active = False
                elif pva_button.collidepoint(event.pos):
                    pvp_active = False
                    pva_active = True
                    config.AI = True

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

                if active_box == timer_box:
                    if event.key == pygame.K_BACKSPACE:
                        text3 = text3[:-1]
                    else:
                        text3 += event.unicode

        screen.fill((30, 30, 30))

        # Welcome Text
        screen.blit(welcome_text, welcome_rect)

        # Input Labels
        player1_label = font.render("Enter black name:", True, pygame.Color('white'))
        player2_label = font.render("Enter white name:", True, pygame.Color('white'))
        screen.blit(player1_label, (input_box1.x, input_box1.y - 30))
        screen.blit(player2_label, (input_box2.x, input_box2.y - 30))

        # Input Boxes
        txt_surface1 = font.render(text1, True, pygame.Color('white'))
        txt_surface2 = font.render(text2, True, pygame.Color('white'))
        width1 = max(250, txt_surface1.get_width() + 10)
        input_box1.w = width1
        width2 = max(250, txt_surface2.get_width() + 10)
        input_box2.w = width2
        screen.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 13))
        screen.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 13))
        pygame.draw.rect(screen, color1, input_box1, 2)
        pygame.draw.rect(screen, color2, input_box2, 2)

        # Start Button
        pygame.draw.rect(screen, start_button_color, start_button)
        start_button_text = font.render("Start Game", True, pygame.Color('white'))
        screen.blit(start_button_text, (start_button.x + 40, start_button.y + 15))

        # Pvp button
        pygame.draw.rect(screen, pvp_button_color, pvp_button)  # Draw background
        border_color = color_active if pvp_active else color_inactive
        pygame.draw.rect(screen, border_color, pvp_button, width=2)  # Draw border
        pvp_button_text = font.render("Player vs Player", True, pygame.Color('white'))
        screen.blit(pvp_button_text, (pvp_button.x + 40, pvp_button.y + 15))

        # Pva
        pygame.draw.rect(screen, pva_button_color, pva_button)  # Draw background
        border_color = color_active if pva_active else color_inactive
        pygame.draw.rect(screen, border_color, pva_button, width=2)  # Draw border
        pva_button_text = font.render("Player vs AI", True, pygame.Color('white'))
        screen.blit(pva_button_text, (pva_button.x + 65, pva_button.y + 15))

        # Timer
        time_label = font.render("Enter Time (mm:ss):", True, pygame.Color('white'))
        screen.blit(time_label, (timer_box.x, timer_box.y - 30))

        txt_surface3 = font.render(text3, True, pygame.Color('white'))
        width3 = max(250, txt_surface3.get_width() + 10)
        timer_box.w = width3
        screen.blit(txt_surface3, (timer_box.x + 5, timer_box.y + 13))
        pygame.draw.rect(screen, timer_box_color, timer_box, 2)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return False
