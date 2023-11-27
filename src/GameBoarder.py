import pygame

from GlobalConstants import *


class GameBoarder:
    def __init__(self, width, height):
        # Create a surface larger than the chessboard to accommodate the border
        self.surface = pygame.Surface((width, height))
        self.surface.fill((48, 46, 43))  # Fill with black or any color for the border
        self.font = pygame.font.SysFont("Arial", 24)
        self.player1_image = pygame.image.load("assets/Images/black_icon.png")
        self.player2_image = pygame.image.load("assets/Images/white_icon.png")
        image_size = (40, 40)  # Width, Height (adjust as needed)# Fill with black or any color for the border
        self.timer_font = pygame.font.SysFont("Arial", 20)

        # Resize the images
        self.player1_image = pygame.transform.scale(self.player1_image, image_size)
        self.player2_image = pygame.transform.scale(self.player2_image, image_size)

    def draw_chessboard(self, chessboard_surface):
        # Calculate the position to center the chessboard
        x = (self.surface.get_width() - chessboard_surface.get_width()) // 2
        y = (self.surface.get_height() - chessboard_surface.get_height()) // 2
        self.surface.blit(chessboard_surface, (x, y))

    def get_surface(self):
        # Return the surface with the chessboard and border
        return self.surface

    def draw_player_info(self, player1, player2, chessboard_surface):
        # Render the text for player1 and player2 names
        player1_text = self.font.render(f"{player1}", True, (255, 255, 255))
        player2_text = self.font.render(f"{player2}", True, (255, 255, 255))

        # Calculate the y positions for the images
        player1_image_y = 10
        player2_image_y = self.surface.get_height() - self.player2_image.get_height() - 10

        # Calculate the y positions for player1 and player2 names to align with the images
        text_height = player1_text.get_height()
        player1_text_y = player1_image_y + (40 - text_height) // 2  # Vertically center the text with the image
        player2_text_y = player2_image_y + (40 - text_height) // 2

        # Calculate the x position for the images and text (aligned with the left edge of the chessboard)
        chessboard_x = (self.surface.get_width() - chessboard_surface.get_width()) // 2
        image_x = chessboard_x

        # Adjust the x position for the player names to be after the images
        text_x = image_x + self.player1_image.get_width() + 10  # Add some padding

        # Blit the images onto the surface
        self.surface.blit(self.player1_image, (image_x, player1_image_y))
        self.surface.blit(self.player2_image, (image_x, player2_image_y))

        # Blit the player names onto the surface, next to their respective images
        self.surface.blit(player1_text, (text_x, player1_text_y))
        self.surface.blit(player2_text, (text_x, player2_text_y))

    def draw_score_bar(self, chessboard_surface):
        # Define the color and dimensions of the bar
        score_bar_color = (255, 255, 255)  # White color for the bar
        score_bar_width = 10  # The width of the bar
        score_bar_height = chessboard_surface.get_height()  # The height of the bar

        # Calculate the position where the chessboard starts (left edge)
        chessboard_x = (self.surface.get_width() - chessboard_surface.get_width()) // 2

        # Position the bar 10 pixels to the left of the chessboard
        score_bar_x = chessboard_x - score_bar_width - 10
        score_bar_y = (self.surface.get_height() - chessboard_surface.get_height()) // 2

        # Draw the bar
        pygame.draw.rect(self.surface, score_bar_color, (score_bar_x, score_bar_y, score_bar_width, score_bar_height))

    def draw_and_update_timer(self, surface, player1_time, player2_time):
        # Font for the timer
        timer_font = pygame.font.SysFont("Arial", 20)

        # Format time as MM:SS
        minutes_black, seconds_black = divmod(player1_time, 60)
        minutes_white, seconds_white = divmod(player2_time, 60)
        player1_timer_text = timer_font.render(f"{minutes_black:02d}:{seconds_black:02d}", True, (255, 255, 255))
        player2_timer_text = timer_font.render(f"{minutes_white:02d}:{seconds_white:02d}", True, (255, 255, 255))

        # Timer rectangle dimensions and colors
        rectangle_color_black = (43, 41, 38)
        rectangle_color_white = (152, 151, 149)
        # Same size for both timers
        rectangle_height = 40
        rectangle_width = 150

        # Calculate the top right corner of the chessboard for the timers
        chessboard_x = ((self.surface.get_width() - surface.get_width()) // 2 + surface.get_width()) - rectangle_width // 2
        rectangle_x = chessboard_x - rectangle_width // 2
        rectangle_y_black = 10
        rectangle_y_white = self.surface.get_height() - rectangle_height - 10

        # Draw the timer rectangles
        pygame.draw.rect(self.surface, rectangle_color_white,(rectangle_x, rectangle_y_white, rectangle_width, rectangle_height))
        pygame.draw.rect(self.surface, rectangle_color_black,(rectangle_x, rectangle_y_black, rectangle_width, rectangle_height))

        # Calculate the position for the timer text
        text_x_black = rectangle_x + (rectangle_width - player1_timer_text.get_width()) // 2
        text_y_black = rectangle_y_black + (rectangle_height - player1_timer_text.get_height()) // 2
        text_x_white = rectangle_x + (rectangle_width - player2_timer_text.get_width()) // 2
        text_y_white = rectangle_y_white + (rectangle_height - player2_timer_text.get_height()) // 2

        # Blit the timer text onto the surface
        self.surface.blit(player1_timer_text, (text_x_black, text_y_black))
        self.surface.blit(player2_timer_text, (text_x_white, text_y_white))




