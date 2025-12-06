"""
Vector module for the game.

This module defines the Vector class for 2D vector operations.
"""

import math


class Vector:
    """
    Represents a 2D vector with x and y components.

    Provides operations for vector arithmetic and transformations.
    """

    x: float
    y: float

    def __init__(self, x: float = 0.0, y: float = 0.0):
        """
        Initialize a vector.

        Args:
            x (float): X component of the vector
            y (float): Y component of the vector
        """
        self.x = x
        self.y = y

    def add(self, other: 'Vector') -> 'Vector':
        """
        Add another vector to this vector and return the result.

        Args:
            other (Vector): The vector to add

        Returns:
            Vector: A new vector representing the sum
        """
        return Vector(self.x + other.x, self.y + other.y)

    def subtract(self, other: 'Vector') -> 'Vector':
        """
        Subtract another vector from this vector and return the result.

        Args:
            other (Vector): The vector to subtract

        Returns:
            Vector: A new vector representing the difference
        """
        return Vector(self.x - other.x, self.y - other.y)

    def rotate(self, angle: float) -> 'Vector':
        """
        Rotate this vector by the given angle (in radians) and return the result.

        Args:
            angle (float): Rotation angle in radians

        Returns:
            Vector: A new vector representing the rotated vector
        """
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        new_x = self.x * cos_angle - self.y * sin_angle
        new_y = self.x * sin_angle + self.y * cos_angle
        return Vector(new_x, new_y)

    def __repr__(self) -> str:
        """Return a string representation of the vector."""
        return f"Vector({self.x}, {self.y})"
