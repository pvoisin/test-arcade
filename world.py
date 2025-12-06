"""World module for game world management."""

from typing import Any, Dict, List, Optional

from behavior import Behavior, BehaviorSystem
from entity import Entity
from terrain import Polygon, Terrain


class World:
    """Game world that manages entities and terrains."""

    width: float
    height: float
    entities: List[Entity]
    terrains: List[Terrain]
    behavior_system: BehaviorSystem
    time_elapsed: float
    properties: Dict[str, Any]

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.entities = []
        self.terrains = []
        self.behavior_system = BehaviorSystem()
        self.time_elapsed = 0.0
        self.properties = {}

    def add_entity(self, entity: Entity) -> None:
        if entity not in self.entities:
            self.entities.append(entity)
            if entity.id is None:
                entity.id = f"entity_{len(self.entities)}"

    def remove_entity(self, entity: Entity) -> None:
        if entity in self.entities:
            self.entities.remove(entity)
            self.behavior_system.unregister_behavior(entity)

    def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None

    def get_entities(self) -> List[Entity]:
        return self.entities.copy()

    def add_terrain(self, terrain: Terrain) -> None:
        if terrain not in self.terrains:
            self.terrains.append(terrain)

    def remove_terrain(self, terrain: Terrain) -> None:
        if terrain in self.terrains:
            self.terrains.remove(terrain)

    def get_terrains(self) -> List[Terrain]:
        return self.terrains.copy()

    def register_behavior(self, entity: Entity, behavior: Behavior) -> None:
        self.behavior_system.register_behavior(entity, behavior)

    @staticmethod
    def _check_aabb_collision(entity1: Entity, entity2: Entity) -> bool:
        """Check AABB (Axis-Aligned Bounding Box) collision using bounding boxes."""
        e1x, e1y, e1w, e1h = entity1.get_bounds()
        e2x, e2y, e2w, e2h = entity2.get_bounds()

        return (
            e1x < e2x + e2w and e1x + e1w > e2x and e1y < e2y + e2h and e1y + e1h > e2y
        )

    def check_entity_collisions(self, entity: Entity) -> List[Entity]:
        """Check collisions using AABB collision detection."""
        collisions: List[Entity] = []

        for other in self.entities:
            if other is entity or not other.active:
                continue

            if self._check_aabb_collision(entity, other):
                collisions.append(other)

        return collisions

    def check_terrain_collisions(self, entity: Entity) -> List[Polygon]:
        all_collisions: List[Polygon] = []

        for terrain in self.terrains:
            collisions: List[Polygon] = terrain.check_collision_with_entity(entity)
            all_collisions.extend(collisions)

        return all_collisions

    def get_entities_in_radius(self, x: float, y: float, radius: float) -> List[Entity]:
        """Get entities within radius using distance squared comparison."""
        entities_in_radius: List[Entity] = []
        radius_squared: float = radius * radius

        for entity in self.entities:
            if not entity.active:
                continue

            ex, ey = entity.position.x, entity.position.y
            distance_squared: float = (ex - x) ** 2 + (ey - y) ** 2

            if distance_squared <= radius_squared:
                entities_in_radius.append(entity)

        return entities_in_radius

    def update(self, delta_time: float) -> None:
        """Update behaviors, entities, handle collisions, and mutate terrain."""
        self.time_elapsed += delta_time

        self.behavior_system.update_all(self.entities, self, delta_time)

        for entity in self.entities:
            if entity.active:
                entity.update(delta_time)

        self._handle_collisions()

        for terrain in self.terrains:
            terrain.mutate_structure()

    def _handle_collisions(self) -> None:
        """Check entity-entity collisions and trigger behavior callbacks."""
        for i, entity in enumerate(self.entities):
            if not entity.active:
                continue

            for j in range(i + 1, len(self.entities)):
                other: Entity = self.entities[j]
                if not other.active:
                    continue

                if self._check_aabb_collision(entity, other):
                    if entity.behavior:
                        entity.behavior.on_collision(entity, other, self)
                    if other.behavior:
                        other.behavior.on_collision(other, entity, self)

    def set_property(self, key: str, value: Any) -> None:
        self.properties[key] = value

    def get_property(self, key: str, default: Any = None) -> Any:
        return self.properties.get(key, default)

    def clear(self) -> None:
        self.entities.clear()
        self.terrains.clear()
        self.behavior_system.clear()
        self.time_elapsed = 0.0

    def __repr__(self) -> str:
        return f"World(size=({self.width}, {self.height}), entities={len(self.entities)}, terrains={len(self.terrains)})"
