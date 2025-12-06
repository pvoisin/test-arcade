"""
Terrain module for the game.

This module defines the Terrain class representing the world structure
composed of polygons.
"""

from typing import TYPE_CHECKING, List, Tuple, Optional

if TYPE_CHECKING:
    from entity import Entity


class Polygon:
    """
    Represents a polygon shape in the terrain.
    
    A polygon is defined by a list of vertices.
    """
    
    def __init__(self, vertices: List[Tuple[float, float]]):
        """
        Initialize a polygon.
        
        Args:
            vertices (List[Tuple[float, float]]): List of (x, y) coordinates
                defining the polygon vertices
        """
        if len(vertices) < 3:
            raise ValueError("A polygon must have at least 3 vertices")
        
        self.vertices = vertices
        self.solid = True  # Whether entities can pass through
        self.properties = {}
    
    def get_vertices(self) -> List[Tuple[float, float]]:
        """
        Get the vertices of the polygon.
        
        Returns:
            List[Tuple[float, float]]: List of vertex coordinates
        """
        return self.vertices
    
    def contains_point(self, x: float, y: float) -> bool:
        """
        Check if a point is inside the polygon using ray casting algorithm.
        
        Args:
            x (float): X coordinate of the point
            y (float): Y coordinate of the point
            
        Returns:
            bool: True if point is inside polygon, False otherwise
        """
        n = len(self.vertices)
        inside = False
        
        p1x, p1y = self.vertices[0]
        for i in range(1, n + 1):
            p2x, p2y = self.vertices[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get the bounding box of the polygon.
        
        Returns:
            Tuple[float, float, float, float]: (min_x, min_y, max_x, max_y)
        """
        xs = [v[0] for v in self.vertices]
        ys = [v[1] for v in self.vertices]
        return (min(xs), min(ys), max(xs), max(ys))
    
    def set_property(self, key: str, value) -> None:
        """Set a custom property on the polygon."""
        self.properties[key] = value
    
    def get_property(self, key: str, default=None):
        """Get a custom property from the polygon."""
        return self.properties.get(key, default)


class Terrain:
    """
    Represents the terrain structure of the world.
    
    Terrain holds logic for mutating the structure of the world and
    is composed of polygons. Collision mechanisms consider terrain structure.
    """
    
    def __init__(self, width: float, height: float):
        """
        Initialize the terrain.
        
        Args:
            width (float): Width of the terrain
            height (float): Height of the terrain
        """
        self.width = width
        self.height = height
        self.polygons = []
        self.grid_cells = {}  # Optional spatial partitioning for optimization
    
    def add_polygon(self, polygon: Polygon) -> None:
        """
        Add a polygon to the terrain.
        
        Args:
            polygon (Polygon): The polygon to add
        """
        self.polygons.append(polygon)
    
    def remove_polygon(self, polygon: Polygon) -> None:
        """
        Remove a polygon from the terrain.
        
        Args:
            polygon (Polygon): The polygon to remove
        """
        if polygon in self.polygons:
            self.polygons.remove(polygon)
    
    def get_polygons(self) -> List[Polygon]:
        """
        Get all polygons in the terrain.
        
        Returns:
            List[Polygon]: List of all polygons
        """
        return self.polygons
    
    def check_collision_with_point(self, x: float, y: float) -> Optional[Polygon]:
        """
        Check if a point collides with any solid polygon.
        
        Args:
            x (float): X coordinate
            y (float): Y coordinate
            
        Returns:
            Optional[Polygon]: The first colliding polygon, or None
        """
        for polygon in self.polygons:
            if polygon.solid and polygon.contains_point(x, y):
                return polygon
        return None
    
    def check_collision_with_entity(self, entity: 'Entity') -> List[Polygon]:
        """
        Check if an entity collides with any terrain polygons.
        
        Args:
            entity (Entity): The entity to check (must have get_bounds() method)
            
        Returns:
            List[Polygon]: List of colliding polygons
        """
        collisions = []
        ex, ey, ew, eh = entity.get_bounds()
        
        # Check entity corners and center
        test_points = [
            (ex, ey),  # Bottom-left
            (ex + ew, ey),  # Bottom-right
            (ex, ey + eh),  # Top-left
            (ex + ew, ey + eh),  # Top-right
            (ex + ew / 2, ey + eh / 2)  # Center
        ]
        
        for polygon in self.polygons:
            if polygon.solid:
                for px, py in test_points:
                    if polygon.contains_point(px, py):
                        collisions.append(polygon)
                        break
        
        return collisions
    
    def create_rectangle(self, x: float, y: float, width: float, height: float) -> Polygon:
        """
        Create a rectangular polygon and add it to the terrain.
        
        Args:
            x (float): X coordinate of bottom-left corner
            y (float): Y coordinate of bottom-left corner
            width (float): Width of the rectangle
            height (float): Height of the rectangle
            
        Returns:
            Polygon: The created polygon
        """
        vertices = [
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height)
        ]
        polygon = Polygon(vertices)
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
        """String representation of the terrain."""
        return f"Terrain(size=({self.width}, {self.height}), polygons={len(self.polygons)})"
