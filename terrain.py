"""Terrain module for terrain structure and collision."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

if TYPE_CHECKING:
    from entity import Entity


class Polygon:
    """Polygon shape defined by vertices."""

    vertices: List[Tuple[float, float]]
    solid: bool
    properties: Dict[str, Any]

    def __init__(self, vertices: List[Tuple[float, float]]) -> None:
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices")

        self.vertices = vertices
        self.solid = True
        self.properties = {}

    def get_vertices(self) -> List[Tuple[float, float]]:
        return self.vertices

    def contains_point(self, x: float, y: float) -> bool:
        """Check if point is inside polygon using ray casting algorithm."""
        n: int = len(self.vertices)
        inside: bool = False

        p1x: float
        p1y: float
        p1x, p1y = self.vertices[0]
        for i in range(1, n + 1):
            p2x: float
            p2y: float
            p2x, p2y = self.vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters: float = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    def get_bounds(self) -> Tuple[float, float, float, float]:
        xs: List[float] = [v[0] for v in self.vertices]
        ys: List[float] = [v[1] for v in self.vertices]

        return (min(xs), min(ys), max(xs), max(ys))

    def set_property(self, key: str, value: Any) -> None:
        self.properties[key] = value

    def get_property(self, key: str, default: Any = None) -> Any:
        return self.properties.get(key, default)


class Terrain:
    """
    Represents the terrain structure of the world.

    Terrain holds logic for mutating the structure of the world and
    is composed of polygons. Collision mechanisms consider terrain structure.
    """

    width: float
    height: float
    polygons: List[Polygon]
    grid_cells: Dict[str, Any]

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.polygons = []
        self.grid_cells = {}  # Optional spatial partitioning for optimization

    def add_polygon(self, polygon: Polygon) -> None:
        self.polygons.append(polygon)

    def remove_polygon(self, polygon: Polygon) -> None:
        if polygon in self.polygons:
            self.polygons.remove(polygon)

    def get_polygons(self) -> List[Polygon]:
        return self.polygons

    def check_collision_with_point(self, x: float, y: float) -> Optional[Polygon]:
        for polygon in self.polygons:
            if polygon.solid and polygon.contains_point(x, y):
                return polygon
        return None

    def check_collision_with_entity(self, entity: "Entity") -> List[Polygon]:
        """Check entity corners and center against solid polygons."""
        collisions: List[Polygon] = []
        ex: float
        ey: float
        ew: float
        eh: float
        ex, ey, ew, eh = entity.get_bounds()

        test_points: List[Tuple[float, float]] = [
            (ex, ey),  # Bottom-left
            (ex + ew, ey),  # Bottom-right
            (ex, ey + eh),  # Top-left
            (ex + ew, ey + eh),  # Top-right
            (ex + ew / 2, ey + eh / 2),  # Center
        ]

        for polygon in self.polygons:
            if polygon.solid:
                for px, py in test_points:
                    if polygon.contains_point(px, py):
                        collisions.append(polygon)
                        break

        return collisions

    def create_rectangle(
        self, x: float, y: float, width: float, height: float
    ) -> Polygon:
        vertices: List[Tuple[float, float]] = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        ]
        polygon: Polygon = Polygon(vertices)
        self.add_polygon(polygon)
        return polygon

    def mutate_structure(self) -> None:
        """
        Apply mutations to the terrain structure.

        This method can be used to implement dynamic terrain changes,
        such as erosion, growth, or player-induced modifications.
        Override or extend this method for specific terrain behaviors.
        """
        pass

    def __repr__(self) -> str:
        return f"Terrain(size=({self.width}, {self.height}), polygons={len(self.polygons)})"
