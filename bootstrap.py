"""
Bootstrap file for starting the Arcade-based 2D Grid Game.

This module is the entry point for the game application.
It initializes the game engine and starts the game loop.
"""

from game_engine import GameEngine


# Game configuration constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "2D Grid Game"

# Grid configuration
GRID_ROWS = 10
GRID_COLS = 10
CELL_SIZE = 40


def main():
    """
    Main function to bootstrap and start the game.
    
    This function creates the game engine instance, sets up the game,
    and starts the main game loop.
    """
    # Create the game engine instance
    game = GameEngine(
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
        SCREEN_TITLE,
        GRID_ROWS,
        GRID_COLS,
        CELL_SIZE
    )
    
    # Set up the game
    game.setup()
    
    # Start the game loop
    game.run()


if __name__ == "__main__":
    main()
