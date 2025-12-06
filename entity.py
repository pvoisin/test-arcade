"""
Entity module for the game.

This module defines the Entity class representing living elements in the world.
"""

from typing import Optional, Tuple


class Entity:
    """
    Represents a living element in the game world.
    
    An entity has position, velocity, and can be affected by behaviors.
    """
    
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
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Velocity
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        
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
        return (self.x, self.y)
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set the position of the entity.
        
        Args:
            x (float): New X position
            y (float): New Y position
        """
        self.x = x
        self.y = y
    
    def get_velocity(self) -> Tuple[float, float]:
        """
        Get the current velocity of the entity.
        
        Returns:
            Tuple[float, float]: (velocity_x, velocity_y)
        """
        return (self.velocity_x, self.velocity_y)
    
    def set_velocity(self, velocity_x: float, velocity_y: float) -> None:
        """
        Set the velocity of the entity.
        
        Args:
            velocity_x (float): Velocity in X direction
            velocity_y (float): Velocity in Y direction
        """
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the bounding box of the entity.
        
        Returns:
            Tuple[float, float, float, float]: (x, y, width, height)
        """
        return (self.x, self.y, self.width, self.height)
    
    def update(self, delta_time: float) -> None:
        """
        Update the entity state.
        
        This method applies velocity to position and can be extended
        for entity-specific updates.
        
        Args:
            delta_time (float): Time elapsed since last update
        """
        # Apply velocity to position
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
    
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
        return f"Entity(id={self.id}, pos=({self.x:.2f}, {self.y:.2f}), size=({self.width:.2f}, {self.height:.2f}))"
