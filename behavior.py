"""
Behavior module for the game.

This module defines the Behavior base class and behavior system for entities.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    from world import World


class Behavior:
    """
    Base class for entity behaviors.
    
    Behaviors hold the logic responsible for mutating the state of an entity
    based on the game state. Subclass this to create specific behaviors.
    """
    
    def __init__(self):
        """Initialize the behavior."""
        self.enabled = True
    
    def update(self, entity: 'Entity', world: 'World', delta_time: float) -> None:
        """
        Update the entity based on this behavior and the game state.
        
        This method should be overridden in subclasses to implement
        specific behavior logic.
        
        Args:
            entity (Entity): The entity to update
            world (World): The world state
            delta_time (float): Time elapsed since last update
        """
        pass
    
    def on_collision(self, entity: 'Entity', other: 'Entity', world: 'World') -> None:
        """
        Handle collision events.
        
        Called when the entity collides with another entity.
        
        Args:
            entity (Entity): The entity with this behavior
            other (Entity): The other entity in the collision
            world (World): The world state
        """
        pass


class IdleBehavior(Behavior):
    """
    Simple idle behavior that does nothing.
    
    Useful for static entities or as a default behavior.
    """
    
    def update(self, entity: 'Entity', world: 'World', delta_time: float) -> None:
        """Entity remains idle."""
        pass


class RandomMovementBehavior(Behavior):
    """
    Example behavior that moves an entity randomly.
    """
    
    def __init__(self, speed: float = 50.0):
        """
        Initialize random movement behavior.
        
        Args:
            speed (float): Movement speed
        """
        super().__init__()
        self.speed = speed
        self.change_direction_timer = 0.0
        self.change_interval = 2.0  # Change direction every 2 seconds
    
    def update(self, entity: 'Entity', world: 'World', delta_time: float) -> None:
        """
        Update entity with random movement.
        
        Args:
            entity (Entity): The entity to update
            world (World): The world state
            delta_time (float): Time elapsed since last update
        """
        import random
        import math
        
        self.change_direction_timer += delta_time
        
        # Change direction periodically
        if self.change_direction_timer >= self.change_interval:
            self.change_direction_timer = 0.0
            
            # Random direction using angle
            angle = random.uniform(0, 2 * math.pi)
            entity.velocity_x = self.speed * math.cos(angle)
            entity.velocity_y = self.speed * math.sin(angle)


class BehaviorSystem:
    """
    System for managing and applying behaviors to entities.
    """
    
    def __init__(self):
        """Initialize the behavior system."""
        self.behaviors = {}
    
    def register_behavior(self, entity: 'Entity', behavior: Behavior) -> None:
        """
        Register a behavior for an entity.
        
        Args:
            entity (Entity): The entity to register the behavior for
            behavior (Behavior): The behavior to register
        """
        self.behaviors[entity.id] = behavior
        entity.behavior = behavior
    
    def unregister_behavior(self, entity: 'Entity') -> None:
        """
        Unregister a behavior from an entity.
        
        Args:
            entity (Entity): The entity to unregister the behavior from
        """
        if entity.id in self.behaviors:
            del self.behaviors[entity.id]
            entity.behavior = None
    
    def update_all(self, entities: list, world: 'World', delta_time: float) -> None:
        """
        Update all registered behaviors.
        
        Args:
            entities (list): List of entities
            world (World): The world state
            delta_time (float): Time elapsed since last update
        """
        for entity in entities:
            if entity.id in self.behaviors and entity.active:
                behavior = self.behaviors[entity.id]
                if behavior.enabled:
                    behavior.update(entity, world, delta_time)
    
    def clear(self) -> None:
        """
        Clear all registered behaviors.
        
        This method removes all behavior registrations.
        """
        self.behaviors.clear()
