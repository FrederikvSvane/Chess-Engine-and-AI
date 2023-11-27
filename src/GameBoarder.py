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
    
    def draw_player_info(self, player1_name, player2_name):
        # Render the text for player1 and player2 names and scores
        player1_surf = self.font.render(f"{player1_name}", True, (255, 255, 255))  # White color for the text
        player2_surf = self.font.render(f"{player2_name}", True, (255, 255, 255))  # White color for the text

        # Calculate the y positions for player1 and player2 names and scores
        player1_y = 10  # A small margin from the top edge
        player2_y = self.surface.get_height() - player2_surf.get_height() - 10  # A small margin from the bottom edge

        # Center the text horizontally
        player1_x = (self.surface.get_width() - player1_surf.get_width()) // 2
        player2_x = (self.surface.get_width() - player2_surf.get_width()) // 2

        # Blit the player names and scores onto the surface
        self.surface.blit(player1_surf, (player1_x, player1_y))
        self.surface.blit(player2_surf, (player2_x, player2_y))
