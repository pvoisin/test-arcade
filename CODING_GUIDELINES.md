# Coding Guidelines

This document outlines the coding standards and practices for the project.

## Type Hints

**All parameters, return types, member variables, and local variables must have explicit type hints.**

- Use proper typing module imports: `List`, `Dict`, `Tuple`, `Optional`, `Any`, etc.
- Use `TYPE_CHECKING` to avoid circular imports when type hints reference classes that would create import cycles.
- Apply type hints consistently throughout the codebase.

## Documentation

**Avoid documenting obvious code with verbose docstrings. Prefer adding docstrings to specific/complex logic only.**

- Only include detailed method docstrings when the logic is non-obvious or algorithmic;
- For simple getters/setters, omit docstrings entirely.

Keep docstrings for:
- Methods with complex algorithms (e.g., ray casting, collision detection etc.);
- Non-obvious behavior;
- Methods that describe specific optimizations or techniques.

Example:
```python
class Vector:
    """2D vector with x and y components."""

    def rotate(self, angle: float) -> "Vector":
        """Rotate by angle in radians using rotation matrix."""
        # Implementation
```

## Code Organization

- One clear responsibility per class;
- Keep methods focused and concise;
- Use meaningful variable names;
- Avoid commented-out code;
- Avoid abbreviations.

## Import Organization

Use TYPE_CHECKING judiciously:
- Use `TYPE_CHECKING` everywhere when possible, particularly where there could be circular import dependencies;
- Regular runtime imports should not be wrapped in `TYPE_CHECKING`;
- Files that only use types for annotations (not runtime instantiation) should use `TYPE_CHECKING`.

Example of when to use TYPE_CHECKING:
```python
# behavior.py - Entity and World are only used for type hints
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity
    from world import World
```

Example of when NOT to use TYPE_CHECKING:
```python
# world.py - Entity is instantiated and used at runtime
from entity import Entity  # No TYPE_CHECKING needed
```

## Vector Class

All position and velocity operations should use the Vector class when appropriate:
- Entity position is stored as a Vector, not separate x/y;
- Entity velocity is stored as a Vector, not separate velocity_x/velocity_y.
