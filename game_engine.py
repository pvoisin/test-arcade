"""
Game Engine for Arcade-based 2D Grid Game

This module contains the core game engine that manages the game window,
rendering, and game loop.
"""

from typing import List, Tuple

import arcade

from terrain import Terrain
from world import World


class GameEngine(arcade.Window):
    """Main game engine class managing game window and loop."""

    grid_rows: int
    grid_cols: int
    cell_size: int
    grid_offset_x: int
    grid_offset_y: int
    world: World

    def __init__(
        self,
        width: int,
        height: int,
        title: str,
        grid_rows: int,
        grid_cols: int,
        cell_size: int,
    ) -> None:
        super().__init__(width, height, title)

        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size

        arcade.set_background_color(arcade.color.WHITE)

        self.grid_offset_x = (width - (grid_cols * cell_size)) // 2
        self.grid_offset_y = (height - (grid_rows * cell_size)) // 2

        world_width: int = grid_cols * cell_size
        world_height: int = grid_rows * cell_size
        self.world = World(float(world_width), float(world_height))

    def setup(self) -> None:
        self.world.clear()
        terrain: Terrain = Terrain(float(self.world.width), float(self.world.height))
        self.world.add_terrain(terrain)

    def on_draw(self) -> None:
        """
        Render the screen.

        This method is called every frame to render the game graphics.
        """
        self.clear()
        self._draw_grid()
        self._draw_terrain()
        self._draw_entities()

    def _draw_grid(self) -> None:
        for col in range(self.grid_cols + 1):
            x: int = self.grid_offset_x + col * self.cell_size
            y_start: int = self.grid_offset_y
            y_end: int = self.grid_offset_y + self.grid_rows * self.cell_size
            arcade.draw_line(x, y_start, x, y_end, arcade.color.BLACK, 2)

        for row in range(self.grid_rows + 1):
            y: int = self.grid_offset_y + row * self.cell_size
            x_start: int = self.grid_offset_x
            x_end: int = self.grid_offset_x + self.grid_cols * self.cell_size
            arcade.draw_line(x_start, y, x_end, y, arcade.color.BLACK, 2)

    def on_update(self, delta_time: float) -> None:
        self.world.update(delta_time)

    def on_key_press(self, key: int, modifiers: int) -> None:
        if key == arcade.key.ESCAPE:
            self.close()

    def on_key_release(self, key: int, modifiers: int) -> None:
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int) -> None:
        pass

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int) -> None:
        pass

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float) -> None:
        pass

    def _draw_terrain(self) -> None:
        for terrain in self.world.get_terrains():
            for polygon in terrain.get_polygons():
                vertices: List[Tuple[float, float]] = polygon.get_vertices()
                if len(vertices) >= 3:
                    screen_vertices: List[Tuple[float, float]] = [
                        (self.grid_offset_x + x, self.grid_offset_y + y)
                        for x, y in vertices
                    ]

                    color: Tuple[int, int, int] = (
                        arcade.color.LIGHT_GRAY
                        if polygon.solid
                        else arcade.color.LIGHT_BLUE
                    )
                    arcade.draw_polygon_filled(screen_vertices, color)
                    arcade.draw_polygon_outline(
                        screen_vertices, arcade.color.DARK_GRAY, 2
                    )

    def _draw_entities(self) -> None:
        for entity in self.world.get_entities():
            if entity.visible:
                ex: float
                ey: float
                ew: float
                eh: float
                ex, ey, ew, eh = entity.get_bounds()
                screen_x: float = self.grid_offset_x + ex
                screen_y: float = self.grid_offset_y + ey

                arcade.draw_rectangle_filled(
                    screen_x + ew / 2,
                    screen_y + eh / 2,
                    ew,
                    eh,
                    arcade.color.RED,
                )

                arcade.draw_rectangle_outline(
                    screen_x + ew / 2,
                    screen_y + eh / 2,
                    ew,
                    eh,
                    arcade.color.DARK_RED,
                    2,
                )
