import pygame

class GameBoarder:
    def __init__(self, width, height):
        # Create a surface larger than the chessboard to accommodate the border
        self.surface = pygame.Surface((width, height))
        self.surface.fill((0, 0, 0))  # Fill with black or any color for the border

    def draw_chessboard(self, chessboard_surface):
        # Calculate the position to center the chessboard
        x = (self.surface.get_width() - chessboard_surface.get_width()) // 2
        y = (self.surface.get_height() - chessboard_surface.get_height()) // 2
        self.surface.blit(chessboard_surface, (x, y))

    def get_surface(self):
        # Return the surface with the chessboard and border
        return self.surface
