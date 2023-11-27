chessBoardWidth = 800
chessBoardHeight = 800
boardSize = 8
squareSize = chessBoardWidth // boardSize

BORDER_WIDTH = 200  # The width of the border around the chessboard
BORDER_HEIGHT = 60  # The height of the border around the chessboard

# Checks if first move is done:


# Adjusted window dimensions to include the border
windowWidthWithBorder = chessBoardWidth + (2 * BORDER_WIDTH)
windowHeightWithBorder = chessBoardHeight + (2 * BORDER_HEIGHT)

letters = {1: 'a', 2: 'b', 3: 'c', 4: 'd', 5: 'e', 6: 'f', 7: 'g', 8: 'h'}


class GlobalConstants:
    gameStarted = False
