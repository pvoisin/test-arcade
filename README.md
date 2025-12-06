# test-arcade

A Python game project based on the Arcade library featuring a 2D grid game engine with entity-component architecture.

## Features

- **Bootstrap System**: Easy game initialization with `bootstrap.py`
- **Game Engine**: Core rendering and game loop management
- **Entity System**: Living elements in the game world
- **Behavior System**: Logic for mutating entity state based on game state
- **Terrain System**: World structure composed of polygons with collision detection
- **World Management**: Global logic managing all entities and terrains

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

To start the game, run:
```bash
python3 bootstrap.py
```

**In environments without a display (like GitHub Codespaces or containers)**, use xvfb-run:
```bash
xvfb-run -a python3 bootstrap.py
```

Press ESC to exit the game.

## Architecture

### Core Classes

#### Entity
Represents a living element in the game world.
- Has position, velocity, and size
- Can be affected by behaviors
- Supports custom properties

```python
from entity import Entity
from vector import Vector

entity = Entity(x=10, y=20, width=5, height=5, entity_id="player")
entity.velocity = Vector(1.0, 2.0)
entity.update(delta_time)
```

#### Behavior
Holds logic for mutating entity state based on game state.
- Base class for creating custom behaviors
- Update method called each frame
- Collision handling support

```python
from behavior import Behavior, IdleBehavior, RandomMovementBehavior

# Use built-in behaviors
idle = IdleBehavior()
random_move = RandomMovementBehavior(speed=50.0)

# Or create custom behaviors
class CustomBehavior(Behavior):
    def update(self, entity, world, delta_time):
        # Custom logic here
        pass
```

#### Terrain
Represents world structure composed of polygons.
- Polygon-based collision detection
- Support for solid and non-solid polygons
- Dynamic terrain mutations

```python
from terrain import Terrain, Polygon

terrain = Terrain(width=400, height=400)
terrain.create_rectangle(x=50, y=50, width=100, height=100)

# Custom polygons
vertices = [(0, 0), (10, 0), (10, 10), (0, 10)]
polygon = Polygon(vertices)
terrain.add_polygon(polygon)
```

#### World
Manages global game logic and holds references to all entities and terrains.
- Entity and terrain management
- Collision detection (entity-entity and entity-terrain)
- Behavior system integration
- Global update loop

```python
from world import World

world = World(width=800, height=600)

# Add entities
world.add_entity(entity)

# Add terrain
world.add_terrain(terrain)

# Register behaviors
world.register_behavior(entity, behavior)

# Update world
world.update(delta_time)
```

### Game Engine

The `GameEngine` class extends `arcade.Window` and integrates all components:
- Manages the game window and rendering
- Displays a 2D grid overlay
- Renders entities and terrain
- Handles input events
- Runs the main game loop

## Project Structure

```
test-arcade/
├── bootstrap.py        # Entry point for the game
├── game_engine.py      # Core game engine
├── entity.py          # Entity class
├── behavior.py        # Behavior system
├── terrain.py         # Terrain and polygon classes
├── world.py           # World management
├── requirements.txt   # Python dependencies
└── README.md          # This file
```

## Development

### Adding New Entities

```python
# In your game setup
entity = Entity(x=100, y=100, width=20, height=20)
world.add_entity(entity)
```

### Creating Custom Behaviors

```python
from behavior import Behavior

class PlayerControlBehavior(Behavior):
    def update(self, entity, world, delta_time):
        # Handle player input
        if keys_pressed[arcade.key.LEFT]:
            entity.velocity_x = -100
        # ... more logic
```

### Adding Terrain

```python
terrain = Terrain(world.width, world.height)

# Add obstacles
terrain.create_rectangle(x=100, y=100, width=50, height=50)

# Add to world
world.add_terrain(terrain)
```

## License

This project is open source.