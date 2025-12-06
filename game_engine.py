"""
Game Engine for Arcade-based 2D Grid Game

This module contains the core game engine that manages the game window,
rendering, and game loop.
"""

import arcade
from world import World
from entity import Entity
from terrain import Terrain


class GameEngine(arcade.Window):
    """
    Main game engine class that extends arcade.Window.
    
    This class manages the game window, rendering of the 2D grid,
    and the main game loop.
    """
    
    def __init__(self, width, height, title, grid_rows, grid_cols, cell_size):
        """
        Initialize the game engine.
        
        Args:
            width (int): Window width in pixels
            height (int): Window height in pixels
            title (str): Window title
            grid_rows (int): Number of rows in the grid
            grid_cols (int): Number of columns in the grid
            cell_size (int): Size of each grid cell in pixels
        """
        super().__init__(width, height, title)
        
        # Grid configuration
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size
        
        # Set background color to white
        arcade.set_background_color(arcade.color.WHITE)
        
        # Grid offset for centering
        self.grid_offset_x = (width - (grid_cols * cell_size)) // 2
        self.grid_offset_y = (height - (grid_rows * cell_size)) // 2
        
        # Initialize the world
        world_width = grid_cols * cell_size
        world_height = grid_rows * cell_size
        self.world = World(world_width, world_height)
        
    def setup(self):
        """
        Set up the game state.
        
        This method is called to initialize or reset the game state.
        """
        # Clear existing world state
        self.world.clear()
        
        # Example: Add a terrain to the world
        terrain = Terrain(self.world.width, self.world.height)
        self.world.add_terrain(terrain)
    
    def on_draw(self):
        """
        Render the screen.
        
        This method is called every frame to render the game graphics.
        """
        # Clear the screen
        self.clear()
        
        # Draw the grid
        self._draw_grid()
        
        # Draw terrain polygons
        self._draw_terrain()
        
        # Draw entities
        self._draw_entities()
    
    def _draw_grid(self):
        """
        Draw the 2D grid on the screen.
        
        This method renders a grid with the specified number of rows and columns.
        """
        # Draw vertical lines
        for col in range(self.grid_cols + 1):
            x = self.grid_offset_x + col * self.cell_size
            y_start = self.grid_offset_y
            y_end = self.grid_offset_y + self.grid_rows * self.cell_size
            arcade.draw_line(x, y_start, x, y_end, arcade.color.BLACK, 2)
        
        # Draw horizontal lines
        for row in range(self.grid_rows + 1):
            y = self.grid_offset_y + row * self.cell_size
            x_start = self.grid_offset_x
            x_end = self.grid_offset_x + self.grid_cols * self.cell_size
            arcade.draw_line(x_start, y, x_end, y, arcade.color.BLACK, 2)
    
    def on_update(self, delta_time):
        """
        Update game state.
        
        This method is called every frame to update game logic.
        
        Args:
            delta_time (float): Time elapsed since the last update
        """
        # Update the world
        self.world.update(delta_time)
    
    def on_key_press(self, key, modifiers):
        """
        Handle key press events.
        
        Args:
            key: The key that was pressed
            modifiers: Modifier keys that were held during the press
        """
        # Close window on ESC key
        if key == arcade.key.ESCAPE:
            self.close()
    
    def on_key_release(self, key, modifiers):
        """
        Handle key release events.
        
        Args:
            key: The key that was released
            modifiers: Modifier keys that were held during the release
        """
        pass
    
    def on_mouse_press(self, x, y, button, modifiers):
        """
        Handle mouse press events.
        
        Args:
            x (float): x coordinate of the mouse
            y (float): y coordinate of the mouse
            button: Mouse button that was pressed
            modifiers: Modifier keys that were held during the press
        """
        pass
    
    def on_mouse_release(self, x, y, button, modifiers):
        """
        Handle mouse release events.
        
        Args:
            x (float): x coordinate of the mouse
            y (float): y coordinate of the mouse
            button: Mouse button that was released
            modifiers: Modifier keys that were held during the release
        """
        pass
    
    def on_mouse_motion(self, x, y, dx, dy):
        """
        Handle mouse motion events.
        
        Args:
            x (float): x coordinate of the mouse
            y (float): y coordinate of the mouse
            dx (float): Change in x since the last call
            dy (float): Change in y since the last call
        """
        pass
    
    def _draw_terrain(self):
        """
        Draw terrain polygons.
        """
        for terrain in self.world.get_terrains():
            for polygon in terrain.get_polygons():
                vertices = polygon.get_vertices()
                if len(vertices) >= 3:
                    # Convert world coordinates to screen coordinates
                    screen_vertices = [
                        (self.grid_offset_x + x, self.grid_offset_y + y)
                        for x, y in vertices
                    ]
                    
                    # Draw filled polygon
                    color = arcade.color.LIGHT_GRAY if polygon.solid else arcade.color.LIGHT_BLUE
                    arcade.draw_polygon_filled(screen_vertices, color)
                    
                    # Draw polygon outline
                    arcade.draw_polygon_outline(screen_vertices, arcade.color.DARK_GRAY, 2)
    
    def _draw_entities(self):
        """
        Draw entities.
        """
        for entity in self.world.get_entities():
            if entity.visible:
                # Convert world coordinates to screen coordinates
                ex, ey, ew, eh = entity.get_bounds()
                screen_x = self.grid_offset_x + ex
                screen_y = self.grid_offset_y + ey
                
                # Draw entity as a rectangle
                arcade.draw_rectangle_filled(
                    screen_x + ew / 2,
                    screen_y + eh / 2,
                    ew,
                    eh,
                    arcade.color.RED
                )
                
                # Draw entity outline
                arcade.draw_rectangle_outline(
                    screen_x + ew / 2,
                    screen_y + eh / 2,
                    ew,
                    eh,
                    arcade.color.DARK_RED,
                    2
                )
