"""
Entity module for the game.

This module defines the Entity class representing living elements in the world.
"""

from typing import Optional, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from behavior import Behavior

from vector import Vector


class Entity:
    """
    Represents a living element in the game world.

    An entity has position, velocity, and can be affected by behaviors.
    """

    id: Optional[str]
    position: Vector
    width: float
    height: float
    velocity: Vector
    active: bool
    visible: bool
    properties: dict
    behavior: Optional['Behavior']

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        width: float = 1.0,
        height: float = 1.0,
        entity_id: Optional[str] = None
    ):
        """
        Initialize an entity.

        Args:
            x (float): X position in world coordinates
            y (float): Y position in world coordinates
            width (float): Width of the entity
            height (float): Height of the entity
            entity_id (str, optional): Unique identifier for the entity
        """
        self.id = entity_id
        self.position = Vector(x, y)
        self.width = width
        self.height = height

        # Velocity
        self.velocity = Vector(0.0, 0.0)

        # State
        self.active = True
        self.visible = True

        # Custom properties dictionary
        self.properties = {}

        # Behavior reference (will be set by behavior system)
        self.behavior = None

    def get_position(self) -> Tuple[float, float]:
        """
        Get the current position of the entity.

        Returns:
            Tuple[float, float]: (x, y) coordinates
        """
        return (self.position.x, self.position.y)

    def set_position(self, x: float, y: float) -> None:
        self.position = Vector(x, y)

    def get_velocity(self) -> Vector:
        return self.velocity

    def set_velocity(self, velocity: Vector) -> None:
        self.velocity = velocity

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the bounding box of the entity.

        Returns:
            Tuple[float, float, float, float]: (x, y, width, height)
        """
        return (self.position.x, self.position.y, self.width, self.height)

    def update(self, delta_time: float) -> None:
        """
        Update the entity state.

        This method applies velocity to position and can be extended
        for entity-specific updates.

        Args:
            delta_time (float): Time elapsed since last update
        """
        # Apply velocity to position
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time

    def set_property(self, key: str, value) -> None:
        """
        Set a custom property on the entity.

        Args:
            key (str): Property name
            value: Property value
        """
        self.properties[key] = value

    def get_property(self, key: str, default=None):
        """
        Get a custom property from the entity.

        Args:
            key (str): Property name
            default: Default value if property doesn't exist

        Returns:
            The property value or default
        """
        return self.properties.get(key, default)

    def __repr__(self) -> str:
        """String representation of the entity."""
        return f"Entity(id={self.id}, pos=({self.position.x:.2f}, {self.position.y:.2f}), size=({self.width:.2f}, {self.height:.2f}))"
