"""
World module for the game.

This module defines the World class that holds global logic and manages
all entities and terrains.
"""

from typing import List, Optional, Tuple
from entity import Entity
from terrain import Terrain, Polygon
from behavior import BehaviorSystem, Behavior


class World:
    """
    Represents the game world.
    
    The World holds global logic applying to all entities and terrains.
    It maintains references to every entity and terrain and manages
    their interactions.
    """
    
    def __init__(self, width: float, height: float):
        """
        Initialize the world.
        
        Args:
            width (float): Width of the world
            height (float): Height of the world
        """
        self.width = width
        self.height = height
        
        # Collections
        self.entities = []
        self.terrains = []
        
        # Systems
        self.behavior_system = BehaviorSystem()
        
        # World state
        self.time_elapsed = 0.0
        self.properties = {}
    
    def add_entity(self, entity: Entity) -> None:
        """
        Add an entity to the world.
        
        Args:
            entity (Entity): The entity to add
        """
        if entity not in self.entities:
            self.entities.append(entity)
            
            # Assign ID if not set
            if entity.id is None:
                entity.id = f"entity_{len(self.entities)}"
    
    def remove_entity(self, entity: Entity) -> None:
        """
        Remove an entity from the world.
        
        Args:
            entity (Entity): The entity to remove
        """
        if entity in self.entities:
            self.entities.remove(entity)
            # Clean up behavior
            self.behavior_system.unregister_behavior(entity)
    
    def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """
        Get an entity by its ID.
        
        Args:
            entity_id (str): The entity ID
            
        Returns:
            Optional[Entity]: The entity, or None if not found
        """
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None
    
    def get_entities(self) -> List[Entity]:
        """
        Get all entities in the world.
        
        Returns:
            List[Entity]: List of all entities
        """
        return self.entities.copy()
    
    def add_terrain(self, terrain: Terrain) -> None:
        """
        Add a terrain to the world.
        
        Args:
            terrain (Terrain): The terrain to add
        """
        if terrain not in self.terrains:
            self.terrains.append(terrain)
    
    def remove_terrain(self, terrain: Terrain) -> None:
        """
        Remove a terrain from the world.
        
        Args:
            terrain (Terrain): The terrain to remove
        """
        if terrain in self.terrains:
            self.terrains.remove(terrain)
    
    def get_terrains(self) -> List[Terrain]:
        """
        Get all terrains in the world.
        
        Returns:
            List[Terrain]: List of all terrains
        """
        return self.terrains.copy()
    
    def register_behavior(self, entity: Entity, behavior: Behavior) -> None:
        """
        Register a behavior for an entity.
        
        Args:
            entity (Entity): The entity
            behavior (Behavior): The behavior to register
        """
        self.behavior_system.register_behavior(entity, behavior)
    
    def check_entity_collisions(self, entity: Entity) -> List[Entity]:
        """
        Check if an entity collides with other entities.
        
        Uses simple bounding box collision detection.
        
        Args:
            entity (Entity): The entity to check
            
        Returns:
            List[Entity]: List of entities colliding with the given entity
        """
        collisions = []
        ex, ey, ew, eh = entity.get_bounds()
        
        for other in self.entities:
            if other is entity or not other.active:
                continue
            
            ox, oy, ow, oh = other.get_bounds()
            
            # AABB collision detection
            if (ex < ox + ow and
                ex + ew > ox and
                ey < oy + oh and
                ey + eh > oy):
                collisions.append(other)
        
        return collisions
    
    def check_terrain_collisions(self, entity: Entity) -> List[Polygon]:
        """
        Check if an entity collides with terrain.
        
        Args:
            entity (Entity): The entity to check
            
        Returns:
            List[Polygon]: List of terrain polygons colliding with the entity
        """
        all_collisions = []
        
        for terrain in self.terrains:
            collisions = terrain.check_collision_with_entity(entity)
            all_collisions.extend(collisions)
        
        return all_collisions
    
    def get_entities_in_radius(self, x: float, y: float, radius: float) -> List[Entity]:
        """
        Get all entities within a radius of a point.
        
        Args:
            x (float): X coordinate of the center point
            y (float): Y coordinate of the center point
            radius (float): Search radius
            
        Returns:
            List[Entity]: List of entities within the radius
        """
        entities_in_radius = []
        radius_squared = radius * radius
        
        for entity in self.entities:
            if not entity.active:
                continue
            
            ex, ey = entity.get_position()
            distance_squared = (ex - x) ** 2 + (ey - y) ** 2
            
            if distance_squared <= radius_squared:
                entities_in_radius.append(entity)
        
        return entities_in_radius
    
    def update(self, delta_time: float) -> None:
        """
        Update the world state.
        
        This method updates all entities, applies behaviors, checks collisions,
        and updates terrains.
        
        Args:
            delta_time (float): Time elapsed since last update
        """
        self.time_elapsed += delta_time
        
        # Update behaviors
        self.behavior_system.update_all(self.entities, self, delta_time)
        
        # Update entities
        for entity in self.entities:
            if entity.active:
                entity.update(delta_time)
        
        # Check and handle collisions
        self._handle_collisions()
        
        # Update terrains
        for terrain in self.terrains:
            terrain.mutate_structure()
    
    def _handle_collisions(self) -> None:
        """
        Handle collision detection and response.
        
        This method checks for entity-entity and entity-terrain collisions
        and triggers appropriate behavior callbacks.
        """
        # Entity-entity collisions
        for i, entity in enumerate(self.entities):
            if not entity.active:
                continue
            
            # Check with other entities
            for j in range(i + 1, len(self.entities)):
                other = self.entities[j]
                if not other.active:
                    continue
                
                # Direct AABB collision check between entity pair
                ex, ey, ew, eh = entity.get_bounds()
                ox, oy, ow, oh = other.get_bounds()
                
                if (ex < ox + ow and
                    ex + ew > ox and
                    ey < oy + oh and
                    ey + eh > oy):
                    # Trigger behavior callbacks
                    if entity.behavior:
                        entity.behavior.on_collision(entity, other, self)
                    if other.behavior:
                        other.behavior.on_collision(other, entity, self)
    
    def set_property(self, key: str, value) -> None:
        """
        Set a global world property.
        
        Args:
            key (str): Property name
            value: Property value
        """
        self.properties[key] = value
    
    def get_property(self, key: str, default=None):
        """
        Get a global world property.
        
        Args:
            key (str): Property name
            default: Default value if property doesn't exist
            
        Returns:
            The property value or default
        """
        return self.properties.get(key, default)
    
    def clear(self) -> None:
        """
        Clear all entities and terrains from the world.
        """
        self.entities.clear()
        self.terrains.clear()
        self.behavior_system.behaviors.clear()
        self.time_elapsed = 0.0
    
    def __repr__(self) -> str:
        """String representation of the world."""
        return f"World(size=({self.width}, {self.height}), entities={len(self.entities)}, terrains={len(self.terrains)})"
