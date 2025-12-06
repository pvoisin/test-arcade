"""Entity module for the game."""

from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

from vector import Vector

if TYPE_CHECKING:
    from behavior import Behavior


class Entity:
    """Living element in the game world."""

    id: Optional[str]
    position: Vector
    width: float
    height: float
    velocity: Vector
    active: bool
    visible: bool
    properties: Dict[str, Any]
    behavior: Optional["Behavior"]

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        width: float = 1.0,
        height: float = 1.0,
        entity_id: Optional[str] = None,
    ) -> None:
        self.id = entity_id
        self.position = Vector(x, y)
        self.width = width
        self.height = height
        self.velocity = Vector(0.0, 0.0)
        self.active = True
        self.visible = True
        self.properties = {}
        self.behavior = None

    def get_position(self) -> "Vector":
        return self.position

    def set_position(self, x: float, y: float) -> None:
        self.position = Vector(x, y)

    def get_velocity(self) -> Vector:
        return self.velocity

    def set_velocity(self, velocity: Vector) -> None:
        self.velocity = velocity

    def get_bounds(self) -> Tuple[float, float, float, float]:
        return (self.position.x, self.position.y, self.width, self.height)

    def update(self, delta_time: float) -> None:
        """Apply velocity to position."""
        self.position.x += self.velocity.x * delta_time
        self.position.y += self.velocity.y * delta_time

    def set_property(self, key: str, value: Any) -> None:
        self.properties[key] = value

    def get_property(self, key: str, default: Any = None) -> Any:
        return self.properties.get(key, default)

    def __repr__(self) -> str:
        return f"Entity(id={self.id}, pos=({self.position.x:.2f}, {self.position.y:.2f}), size=({self.width:.2f}, {self.height:.2f}))"
