import pygame

class GameBoarder:
    def __init__(self, width, height):
        # Create a surface larger than the chessboard to accommodate the border
        self.surface = pygame.Surface((width, height))
        self.surface.fill((0, 0, 0))  # Fill with black or any color for the border
        self.font = pygame.font.SysFont("Arial", 24)

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
        player1 = self.font.render(f"{player1}", True, (255, 255, 255))  # White color for the text
        player2 = self.font.render(f"{player2}", True, (255, 255, 255))  # White color for the text

        # Calculate the x position where the chessboard starts (left edge)
        chessboard_x = (self.surface.get_width() - chessboard_surface.get_width()) // 2

        # Calculate the y positions for player1 and player2 names
        player1_y = 10  # A small margin from the top edge
        player2_y = self.surface.get_height() - player2.get_height() - 10  # A small margin from the bottom edge

        # Blit the player names onto the surface, aligned with the chessboard's left edge
        self.surface.blit(player1, (chessboard_x, player1_y))
        self.surface.blit(player2, (chessboard_x, player2_y))


