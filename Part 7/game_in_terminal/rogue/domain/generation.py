from __future__ import annotations

import random

from rogue.domain.models import (
    MAP_HEIGHT,
    MAP_WIDTH,
    Corridor,
    Enemy,
    EnemyType,
    Item,
    ItemType,
    Level,
    Position,
    Room,
    Tile,
)


ENEMY_ARCHETYPES = {
    EnemyType.ZOMBIE: {"health": 18, "agility": 3, "strength": 5, "hostility_range": 5},
    EnemyType.VAMPIRE: {"health": 16, "agility": 7, "strength": 6, "hostility_range": 7},
    EnemyType.GHOST: {"health": 10, "agility": 8, "strength": 3, "hostility_range": 4},
    EnemyType.OGRE: {"health": 24, "agility": 2, "strength": 9, "hostility_range": 5},
    EnemyType.SNAKE_MAGE: {"health": 12, "agility": 10, "strength": 5, "hostility_range": 8},
}


# Build a full dungeon floor, spawn items and enemies, and return it with next enemy id
def generate_level(level_index: int, next_enemy_id: int, seed: int | None = None) -> tuple[Level, int]:
    """Generate one fully playable floor and return it with the next free enemy id."""
    rng = random.Random(seed if seed is not None else random.randrange(1_000_000_000))
    seed_value = seed if seed is not None else rng.randrange(1_000_000_000)
    rng.seed(seed_value)

    tiles = [[Tile.VOID.value for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
    rooms = _generate_rooms(rng)
    # Paint each room onto the tile grid
    for room in rooms:
        _paint_room(tiles, room)

    corridors = _connect_rooms(rng, tiles, rooms)

    start_room_id = rng.randrange(len(rooms))
    exit_room_id = rng.choice([room.room_id for room in rooms if room.room_id != start_room_id])
    exit_room = rooms[exit_room_id]
    exit_position = rng.choice(exit_room.interior_positions())
    tiles[exit_position.y][exit_position.x] = Tile.EXIT.value

    items = _spawn_items(rng, level_index, rooms, start_room_id, exit_position)
    enemies, next_enemy_id = _spawn_enemies(rng, level_index, rooms, start_room_id, next_enemy_id)

    level = Level(
        index=level_index,
        width=MAP_WIDTH,
        height=MAP_HEIGHT,
        tiles=tiles,
        rooms=rooms,
        corridors=corridors,
        start_room_id=start_room_id,
        exit_room_id=exit_room_id,
        exit_position=exit_position,
        items=items,
        enemies=enemies,
        seed=seed_value,
    )
    level.sync_room_contents()
    return level, next_enemy_id


# Pick an empty start position for the player
def spawn_position_in_start(level: Level, rng: random.Random) -> Position:
    start_room = level.rooms[level.start_room_id]
    options = [position for position in start_room.interior_positions() if level.item_at(position) is None]
    return rng.choice(options)


# Create a 3x3 layout of randomly sized rooms
def _generate_rooms(rng: random.Random) -> list[Room]:
    rooms: list[Room] = []
    section_width = MAP_WIDTH // 3
    section_height = MAP_HEIGHT // 3
    room_id = 0
    for row in range(3):
        for col in range(3):
            # Each room stays inside its own section of the 3x3 layout.
            left = col * section_width
            top = row * section_height
            room_width = rng.randint(max(6, section_width // 2), section_width - 2)
            room_height = rng.randint(max(4, section_height // 2), section_height - 2)
            x1 = left + rng.randint(1, max(1, section_width - room_width - 1))
            y1 = top + rng.randint(1, max(1, section_height - room_height - 1))
            x2 = min(MAP_WIDTH - 2, x1 + room_width)
            y2 = min(MAP_HEIGHT - 2, y1 + room_height)
            rooms.append(Room(room_id=room_id, x1=x1, y1=y1, x2=x2, y2=y2))
            room_id += 1
    return rooms


# Draw room walls and floor tiles on the map
def _paint_room(tiles: list[list[str]], room: Room) -> None:
    for y in range(room.y1, room.y2 + 1):
        for x in range(room.x1, room.x2 + 1):
            is_wall = x in {room.x1, room.x2} or y in {room.y1, room.y2}
            tiles[y][x] = Tile.WALL.value if is_wall else Tile.FLOOR.value


# Choose which room pairs to connect and carve corridors
def _connect_rooms(rng: random.Random, tiles: list[list[str]], rooms: list[Room]) -> list[Corridor]:
    corridors: list[Corridor] = []
    edges = {(0, 1), (1, 2), (3, 4), (4, 5), (6, 7), (7, 8), (0, 3), (3, 6), (1, 4), (4, 7), (2, 5), (5, 8)}
    mandatory = {(0, 1), (1, 2), (0, 3), (3, 6), (1, 4), (4, 5), (4, 7), (7, 8)}
    # Mandatory edges guarantee a connected graph; optional ones add variation.
    chosen_edges = set(mandatory)
    # Randomly add optional corridors between sections
    for edge in edges - mandatory:
        if rng.random() < 0.45:
            chosen_edges.add(edge)
    # Carve corridors between connected rooms
    for room_a, room_b in sorted(chosen_edges):
        corridor_points = _carve_corridor(rng, tiles, rooms[room_a].center(), rooms[room_b].center())
        corridors.append(Corridor(points=corridor_points))
    return corridors


# Make an L-shaped corridor between two points
def _carve_corridor(
    rng: random.Random,
    tiles: list[list[str]],
    start: Position,
    finish: Position,
) -> list[Position]:
    points: list[Position] = []
    current = Position(start.x, start.y)
    # Corridors are carved as L-shapes to keep generation simple and robust.
    horizontal_first = rng.random() < 0.5
    # Choose whether to go horizontal first
    if horizontal_first:
        points.extend(_carve_line(tiles, current, Position(finish.x, current.y)))
        current = Position(finish.x, current.y)
        points.extend(_carve_line(tiles, current, finish))
    else:
        points.extend(_carve_line(tiles, current, Position(current.x, finish.y)))
        current = Position(current.x, finish.y)
        points.extend(_carve_line(tiles, current, finish))
    return points


# Draw straight corridor segment between two points
def _carve_line(tiles: list[list[str]], start: Position, finish: Position) -> list[Position]:
    points: list[Position] = []
    x_step = 0 if start.x == finish.x else (1 if finish.x > start.x else -1)
    y_step = 0 if start.y == finish.y else (1 if finish.y > start.y else -1)
    x, y = start.x, start.y
    # Step along the line until reaching the end
    while (x, y) != (finish.x, finish.y):
        _set_corridor_tile(tiles, x, y)
        points.append(Position(x, y))
        x += x_step
        y += y_step
    _set_corridor_tile(tiles, finish.x, finish.y)
    points.append(Position(finish.x, finish.y))
    return points


# Convert a tile to corridor if appropriate
def _set_corridor_tile(tiles: list[list[str]], x: int, y: int) -> None:
    # Only set corridor on empty tiles
    if tiles[y][x] == Tile.VOID.value:
        tiles[y][x] = Tile.CORRIDOR.value
        return
    # Replace wall with corridor when carving
    if tiles[y][x] == Tile.WALL.value:
        tiles[y][x] = Tile.CORRIDOR.value


# Place items in rooms with rarity adjusted by depth
def _spawn_items(
    rng: random.Random,
    level_index: int,
    rooms: list[Room],
    start_room_id: int,
    exit_position: Position,
) -> list[Item]:
    items: list[Item] = []
    occupied = {(exit_position.x, exit_position.y)}
    item_budget = max(3, 12 - level_index // 2)
    # Useful consumables become rarer on deeper floors.
    useful_bias = max(0.12, 0.55 - level_index * 0.015)
    # Try to place each item within the budget
    for _ in range(item_budget):
        room = rng.choice([room for room in rooms if room.room_id != start_room_id])
        candidates = [
            point
            # Iterate interior positions
            for point in room.interior_positions()
            # Skip occupied positions
            if (point.x, point.y) not in occupied
        ]
        # Skip if no free position in room
        if not candidates:
            continue
        position = rng.choice(candidates)
        occupied.add((position.x, position.y))
        roll = rng.random()
        # Small chance to spawn food for healing
        if roll < useful_bias * 0.45:
            item = Item(ItemType.FOOD, "Ration", position=position, health=rng.randint(5, 10))
        # Chance to spawn an elixir with temporary boost
        elif roll < useful_bias * 0.75:
            stat = rng.choice(["strength", "agility", "max_health"])
            item = Item(
                ItemType.ELIXIR,
                f"Elixir of {stat}",
                position=position,
                strength=2 if stat == "strength" else 0,
                agility=2 if stat == "agility" else 0,
                max_health=4 if stat == "max_health" else 0,
                duration=20,
            )
        # Chance to spawn a scroll that gives small permanent stats
        elif roll < useful_bias:
            stat = rng.choice(["strength", "agility", "max_health"])
            item = Item(
                ItemType.SCROLL,
                f"Scroll of {stat}",
                position=position,
                strength=1 if stat == "strength" else 0,
                agility=1 if stat == "agility" else 0,
                max_health=2 if stat == "max_health" else 0,
            )
        # Otherwise spawn a weapon scaled to level
        else:
            item = Item(
                ItemType.WEAPON,
                rng.choice(["Dagger", "Mace", "Spear", "Sword"]),
                position=position,
                strength=rng.randint(2, 4) + level_index // 4,
            )
        items.append(item)
    return items


# Spawn enemies with stats chosen from archetypes and scaled by level
def _spawn_enemies(
    rng: random.Random,
    level_index: int,
    rooms: list[Room],
    start_room_id: int,
    next_enemy_id: int,
) -> tuple[list[Enemy], int]:
    enemies: list[Enemy] = []
    occupied: set[tuple[int, int]] = set()
    # Enemy count is one of the main difficulty levers for floor depth.
    count = min(4 + level_index + level_index // 4, 20)
    room_choices = [room for room in rooms if room.room_id != start_room_id]
    # Spawn each enemy and place them inside rooms
    for _ in range(count):
        enemy_type = rng.choice(list(EnemyType))
        archetype = ENEMY_ARCHETYPES[enemy_type]
        room = rng.choice(room_choices)
        candidates = [
            point
            # Iterate free positions inside the room
            for point in room.interior_positions()
            # Skip occupied positions
            if (point.x, point.y) not in occupied
        ]
        # Skip if no free spawn positions
        if not candidates:
            continue
        position = rng.choice(candidates)
        occupied.add((position.x, position.y))
        bonus = level_index // 3
        enemy = Enemy(
            enemy_id=next_enemy_id,
            enemy_type=enemy_type,
            position=position,
            max_health=archetype["health"] + bonus * 2,
            health=archetype["health"] + bonus * 2,
            agility=archetype["agility"] + bonus // 2,
            strength=archetype["strength"] + bonus,
            hostility_range=archetype["hostility_range"] + bonus // 2,
            invisible=enemy_type is EnemyType.GHOST,
        )
        enemies.append(enemy)
        next_enemy_id += 1
    return enemies, next_enemy_id
