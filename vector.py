import math


class Vector:
    """2D vector with x and y components."""

    x: float
    y: float

    def __init__(self, x: float = 0.0, y: float = 0.0) -> None:
        self.x = x
        self.y = y

    def add(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    def subtract(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    def rotate(self, angle: float) -> "Vector":
        """Rotate by angle in radians using rotation matrix."""
        cos_angle: float = math.cos(angle)
        sin_angle: float = math.sin(angle)

        return Vector(
            self.x * cos_angle - self.y * sin_angle,
            self.x * sin_angle + self.y * cos_angle,
        )

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
