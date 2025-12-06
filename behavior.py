"""Behavior module for entity behaviors."""

import math
import random
from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:
    from entity import Entity
    from world import World


class Behavior:
    enabled: bool

    def __init__(self) -> None:
        self.enabled = True

    def update(self, entity: "Entity", world: "World", delta_time: float) -> None:
        pass

    def on_collision(self, entity: "Entity", other: "Entity", world: "World") -> None:
        pass


class IdleBehavior(Behavior):
    def update(self, entity: "Entity", world: "World", delta_time: float) -> None:
        pass


class RandomMovementBehavior(Behavior):
    speed: float
    change_direction_timer: float
    change_interval: float

    def __init__(self, speed: float = 50.0) -> None:
        super().__init__()
        self.speed = speed
        self.change_direction_timer = 0.0
        self.change_interval = 2.0

    def update(self, entity: "Entity", world: "World", delta_time: float) -> None:
        self.change_direction_timer += delta_time

        if self.change_direction_timer >= self.change_interval:
            self.change_direction_timer = 0.0
            angle: float = random.uniform(0, 2 * math.pi)
            entity.velocity.x = self.speed * math.cos(angle)
            entity.velocity.y = self.speed * math.sin(angle)


class BehaviorSystem:
    """System for managing and applying behaviors to entities."""

    behaviors: Dict[Optional[str], Behavior]

    def __init__(self) -> None:
        self.behaviors = {}

    def register_behavior(self, entity: "Entity", behavior: Behavior) -> None:
        self.behaviors[entity.id] = behavior
        entity.behavior = behavior

    def unregister_behavior(self, entity: "Entity") -> None:
        if entity.id in self.behaviors:
            del self.behaviors[entity.id]
            entity.behavior = None

    def update_all(
        self, entities: List["Entity"], world: "World", delta_time: float
    ) -> None:
        for entity in entities:
            if entity.id in self.behaviors and entity.active:
                behavior: Behavior = self.behaviors[entity.id]
                if behavior.enabled:
                    behavior.update(entity, world, delta_time)

    def clear(self) -> None:
        self.behaviors.clear()
