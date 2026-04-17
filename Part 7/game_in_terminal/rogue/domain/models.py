from __future__ import annotations
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


MAP_WIDTH = 60
MAP_HEIGHT = 24
TOTAL_LEVELS = 21


# Tile values used to represent map cells
class Tile(str, Enum):
    VOID = " "
    WALL = "#"
    FLOOR = "."
    CORRIDOR = "+"
    EXIT = ">"


# Types of items the player can find or use
class ItemType(str, Enum):
    FOOD = "food"
    ELIXIR = "elixir"
    SCROLL = "scroll"
    WEAPON = "weapon"
    TREASURE = "treasure"


# Which stat a timed effect modifies (health, strength, agility)
class EffectStat(str, Enum):
    MAX_HEALTH = "max_health"
    STRENGTH = "strength"
    AGILITY = "agility"


# Different enemy archetypes used to pick stats and behavior
class EnemyType(str, Enum):
    ZOMBIE = "zombie"
    VAMPIRE = "vampire"
    GHOST = "ghost"
    OGRE = "ogre"
    SNAKE_MAGE = "snake_mage"


@dataclass
# Simple coordinate pair used throughout the game
class Position:
    x: int
    y: int

    # Return a new Position moved by dx and dy
    def shifted(self, dx: int, dy: int) -> "Position":
        return Position(self.x + dx, self.y + dy)

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y}

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, int]) -> "Position":
        return cls(x=data["x"], y=data["y"])


@dataclass
# Rectangular room with enemies and items
class Room:
    room_id: int
    x1: int
    y1: int
    x2: int
    y2: int
    enemy_ids: list[int] = field(default_factory=list)
    item_positions: list[dict[str, Any]] = field(default_factory=list)

    # Check if a position lies inside this room
    def contains(self, position: Position) -> bool:
        return self.x1 <= position.x <= self.x2 and self.y1 <= position.y <= self.y2

    # Get integer center position of the room
    def center(self) -> Position:
        return Position((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

    # List floor positions inside the room for spawns
    def interior_positions(self) -> list[Position]:
        return [
            Position(x, y)
            for y in range(self.y1 + 1, self.y2)
            for x in range(self.x1 + 1, self.x2)
        ]

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, int]:
        return {
            "room_id": self.room_id,
            "x1": self.x1,
            "y1": self.y1,
            "x2": self.x2,
            "y2": self.y2,
            "enemy_ids": self.enemy_ids,
            "item_positions": self.item_positions,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, int]) -> "Room":
        return cls(**data)


@dataclass
# Path between two rooms represented by points
class Corridor:
    points: list[Position]

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {"points": [point.to_dict() for point in self.points]}

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "Corridor":
        return cls(points=[Position.from_dict(point) for point in data["points"]])


@dataclass
# Item data including stats and optional map position
class Item:
    item_type: ItemType
    name: str
    position: Position | None = None
    health: int = 0
    max_health: int = 0
    strength: int = 0
    agility: int = 0
    value: int = 0
    duration: int = 0

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "item_type": self.item_type.value,
            "name": self.name,
            "position": None if self.position is None else self.position.to_dict(),
            "health": self.health,
            "max_health": self.max_health,
            "strength": self.strength,
            "agility": self.agility,
            "value": self.value,
            "duration": self.duration,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "Item":
        return cls(
            item_type=ItemType(data["item_type"]),
            name=data["name"],
            position=None if data["position"] is None else Position.from_dict(data["position"]),
            health=data["health"],
            max_health=data["max_health"],
            strength=data["strength"],
            agility=data.get("agility", data.get("dexterity", 0)),
            value=data["value"],
            duration=data["duration"],
        )


@dataclass
# A temporary stat modifier that expires by turns
class ActiveEffect:
    stat: EffectStat
    amount: int
    remaining_turns: int

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "stat": self.stat.value,
            "amount": self.amount,
            "remaining_turns": self.remaining_turns,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "ActiveEffect":
        return cls(
            stat=EffectStat(data["stat"]),
            amount=data["amount"],
            remaining_turns=data["remaining_turns"],
        )


@dataclass
# Player inventory organized by item type
class Backpack:
    food: list[Item] = field(default_factory=list)
    elixirs: list[Item] = field(default_factory=list)
    scrolls: list[Item] = field(default_factory=list)
    weapons: list[Item] = field(default_factory=list)
    treasure: int = 0

    # Try to add an item to the backpack or treasure
    def add_item(self, item: Item) -> bool:
        if item.item_type is ItemType.TREASURE:
            self.treasure += item.value
            return True

        bucket = self.bucket_for(item.item_type)
        if len(bucket) >= 9:
            return False
        bucket.append(item)
        return True

    # Return the list storing items of given type
    def bucket_for(self, item_type: ItemType) -> list[Item]:
        mapping = {
            ItemType.FOOD: self.food,
            ItemType.ELIXIR: self.elixirs,
            ItemType.SCROLL: self.scrolls,
            ItemType.WEAPON: self.weapons,
        }
        return mapping[item_type]

    # Remove and return item from a bucket
    def remove_item(self, item_type: ItemType, index: int) -> Item:
        return self.bucket_for(item_type).pop(index)

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "food": [item.to_dict() for item in self.food],
            "elixirs": [item.to_dict() for item in self.elixirs],
            "scrolls": [item.to_dict() for item in self.scrolls],
            "weapons": [item.to_dict() for item in self.weapons],
            "treasure": self.treasure,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "Backpack":
        return cls(
            food=[Item.from_dict(item) for item in data["food"]],
            elixirs=[Item.from_dict(item) for item in data["elixirs"]],
            scrolls=[Item.from_dict(item) for item in data["scrolls"]],
            weapons=[Item.from_dict(item) for item in data["weapons"]],
            treasure=data["treasure"],
        )


@dataclass
# Player character state, inventory and effects
class Character:
    position: Position
    max_health: int
    health: int
    agility: int
    strength: int
    backpack: Backpack = field(default_factory=Backpack)
    equipped_weapon: Item | None = None
    active_effects: list[ActiveEffect] = field(default_factory=list)
    sleeping_turns: int = 0

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "position": self.position.to_dict(),
            "max_health": self.max_health,
            "health": self.health,
            "agility": self.agility,
            "strength": self.strength,
            "backpack": self.backpack.to_dict(),
            "equipped_weapon": None if self.equipped_weapon is None else self.equipped_weapon.to_dict(),
            "active_effects": [effect.to_dict() for effect in self.active_effects],
            "sleeping_turns": self.sleeping_turns,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "Character":
        return cls(
            position=Position.from_dict(data["position"]),
            max_health=data["max_health"],
            health=data["health"],
            agility=data.get("agility", data.get("dexterity")),
            strength=data["strength"],
            backpack=Backpack.from_dict(data["backpack"]),
            equipped_weapon=None
            if data["equipped_weapon"] is None
            else Item.from_dict(data["equipped_weapon"]),
            active_effects=[ActiveEffect.from_dict(effect) for effect in data["active_effects"]],
            sleeping_turns=data["sleeping_turns"],
        )

    @property
    # Alias for agility used by some code paths
    def dexterity(self) -> int:
        return self.agility

    @dexterity.setter
    # Alias for agility used by some code paths
    def dexterity(self, value: int) -> None:
        self.agility = value

    @property
    def weapon(self) -> Item | None:
        return self.equipped_weapon

    @weapon.setter
    def weapon(self, value: Item | None) -> None:
        self.equipped_weapon = value

    @property
    def inventory(self) -> Backpack:
        return self.backpack


@dataclass
# Enemy state and behavior flags used by engine
class Enemy:
    enemy_id: int
    enemy_type: EnemyType
    position: Position
    max_health: int
    health: int
    agility: int
    strength: int
    hostility_range: int
    is_chasing: bool = False
    invisible: bool = False
    phase: int = 0
    cooldown: int = 0
    first_hit_negated: bool = False
    behavior: str = "idle"
    counterattack_ready: bool = False

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "enemy_id": self.enemy_id,
            "enemy_type": self.enemy_type.value,
            "position": self.position.to_dict(),
            "max_health": self.max_health,
            "health": self.health,
            "agility": self.agility,
            "strength": self.strength,
            "hostility_range": self.hostility_range,
            "is_chasing": self.is_chasing,
            "invisible": self.invisible,
            "phase": self.phase,
            "cooldown": self.cooldown,
            "first_hit_negated": self.first_hit_negated,
            "behavior": self.behavior,
            "counterattack_ready": self.counterattack_ready,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "Enemy":
        return cls(
            enemy_id=data["enemy_id"],
            enemy_type=EnemyType(data["enemy_type"]),
            position=Position.from_dict(data["position"]),
            max_health=data["max_health"],
            health=data["health"],
            agility=data.get("agility", data.get("dexterity")),
            strength=data["strength"],
            hostility_range=data.get("hostility_range", data.get("hostility")),
            is_chasing=data["is_chasing"],
            invisible=data["invisible"],
            phase=data["phase"],
            cooldown=data["cooldown"],
            first_hit_negated=data["first_hit_negated"],
            behavior=data.get("behavior", "idle"),
            counterattack_ready=data.get("counterattack_ready", False),
        )

    @property
    # Alias for agility used by some code paths
    def dexterity(self) -> int:
        return self.agility

    @dexterity.setter
    # Alias for agility used by some code paths
    def dexterity(self, value: int) -> None:
        self.agility = value

    @property
    def hostility(self) -> int:
        return self.hostility_range

    @hostility.setter
    def hostility(self, value: int) -> None:
        self.hostility_range = value


@dataclass
# Collected run statistics counters
class Statistics:
    treasure_collected: int = 0
    deepest_level: int = 1
    enemies_defeated: int = 0
    food_eaten: int = 0
    elixirs_used: int = 0
    scrolls_read: int = 0
    hits_dealt: int = 0
    hits_taken: int = 0
    tiles_walked: int = 0

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, int]:
        return {
            "treasure_collected": self.treasure_collected,
            "deepest_level": self.deepest_level,
            "enemies_defeated": self.enemies_defeated,
            "food_eaten": self.food_eaten,
            "elixirs_used": self.elixirs_used,
            "scrolls_read": self.scrolls_read,
            "hits_dealt": self.hits_dealt,
            "hits_taken": self.hits_taken,
            "tiles_walked": self.tiles_walked,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, int]) -> "Statistics":
        return cls(**data)


@dataclass
# Map tiles, rooms, items and enemies for a floor
class Level:
    index: int
    width: int
    height: int
    tiles: list[list[str]]
    rooms: list[Room]
    corridors: list[Corridor]
    start_room_id: int
    exit_room_id: int
    exit_position: Position
    items: list[Item] = field(default_factory=list)
    enemies: list[Enemy] = field(default_factory=list)
    explored: set[tuple[int, int]] = field(default_factory=set)
    visible: set[tuple[int, int]] = field(default_factory=set)
    seed: int = 0

    # Check if a map position is within level bounds
    def in_bounds(self, position: Position) -> bool:
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    # Get tile glyph at a position
    def tile_at(self, position: Position) -> str:
        return self.tiles[position.y][position.x]

    # Place a tile glyph at a position
    def set_tile(self, position: Position, tile: Tile) -> None:
        self.tiles[position.y][position.x] = tile.value

    # Find which room contains a position
    def room_for_position(self, position: Position) -> Room | None:
        for room in self.rooms:
            if room.contains(position):
                return room
        return None

    # Return True when a position can be walked on
    def walkable(self, position: Position) -> bool:
        return self.in_bounds(position) and self.tile_at(position) in {
            Tile.FLOOR.value,
            Tile.CORRIDOR.value,
            Tile.EXIT.value,
        }

    # Return item at position or None
    def item_at(self, position: Position) -> Item | None:
        for item in self.items:
            if item.position and item.position.x == position.x and item.position.y == position.y:
                return item
        return None

    # Return live enemy at position or None
    def enemy_at(self, position: Position) -> Enemy | None:
        for enemy in self.enemies:
            if enemy.position.x == position.x and enemy.position.y == position.y and enemy.health > 0:
                return enemy
        return None

    # Update rooms with current enemy and item lists
    def sync_room_contents(self) -> None:
        for room in self.rooms:
            room.enemy_ids = []
            room.item_positions = []
        for enemy in self.enemies:
            room = self.room_for_position(enemy.position)
            if room is not None and enemy.health > 0:
                room.enemy_ids.append(enemy.enemy_id)
        for item in self.items:
            if item.position is None:
                continue
            room = self.room_for_position(item.position)
            if room is not None:
                room.item_positions.append(
                    {
                        "type": item.item_type.value,
                        "name": item.name,
                        "x": item.position.x,
                        "y": item.position.y,
                    }
                )

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "width": self.width,
            "height": self.height,
            "tiles": self.tiles,
            "rooms": [room.to_dict() for room in self.rooms],
            "corridors": [corridor.to_dict() for corridor in self.corridors],
            "start_room_id": self.start_room_id,
            "exit_room_id": self.exit_room_id,
            "exit_position": self.exit_position.to_dict(),
            "items": [item.to_dict() for item in self.items],
            "enemies": [enemy.to_dict() for enemy in self.enemies],
            "explored": [[x, y] for x, y in sorted(self.explored)],
            "visible": [[x, y] for x, y in sorted(self.visible)],
            "seed": self.seed,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "Level":
        return cls(
            index=data["index"],
            width=data["width"],
            height=data["height"],
            tiles=data["tiles"],
            rooms=[Room.from_dict(room) for room in data["rooms"]],
            corridors=[Corridor.from_dict(corridor) for corridor in data["corridors"]],
            start_room_id=data["start_room_id"],
            exit_room_id=data["exit_room_id"],
            exit_position=Position.from_dict(data["exit_position"]),
            items=[Item.from_dict(item) for item in data["items"]],
            enemies=[Enemy.from_dict(enemy) for enemy in data["enemies"]],
            explored={tuple(cell) for cell in data["explored"]},
            visible={tuple(cell) for cell in data["visible"]},
            seed=data["seed"],
        )


@dataclass
# Short list of recent messages for the UI
class MessageLog:
    messages: list[str] = field(default_factory=list)

    # Append a message and keep only the last few
    def add(self, message: str) -> None:
        self.messages.append(message)
        self.messages[:] = self.messages[-6:]

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, list[str]]:
        return {"messages": self.messages}

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, list[str]]) -> "MessageLog":
        return cls(messages=list(data["messages"]))


@dataclass
# Full game state that can be saved and restored
class GameSession:
    player: Character
    level: Level
    current_level: int
    completed: bool = False
    game_over: bool = False
    statistics: Statistics = field(default_factory=Statistics)
    message_log: MessageLog = field(default_factory=MessageLog)
    next_enemy_id: int = 1

    @property
    # Convenience alias to access current level
    def map(self) -> Level:
        return self.level

    @property
    # Human-readable state string for session
    def state(self) -> str:
        return "game over" if self.game_over else "active"

    # Convert the object to a plain dict for saving
    def to_dict(self) -> dict[str, Any]:
        return {
            "player": self.player.to_dict(),
            "level": self.level.to_dict(),
            "current_level": self.current_level,
            "completed": self.completed,
            "game_over": self.game_over,
            "statistics": self.statistics.to_dict(),
            "message_log": self.message_log.to_dict(),
            "next_enemy_id": self.next_enemy_id,
        }

    @classmethod
    # Create the object from a saved dict
    def from_dict(cls, data: dict[str, Any]) -> "GameSession":
        return cls(
            player=Character.from_dict(data["player"]),
            level=Level.from_dict(data["level"]),
            current_level=data["current_level"],
            completed=data["completed"],
            game_over=data["game_over"],
            statistics=Statistics.from_dict(data["statistics"]),
            message_log=MessageLog.from_dict(data["message_log"]),
            next_enemy_id=data["next_enemy_id"],
        )

class Mimic(Enemy):
    def __init__(self):
        super().__init__(
            name="Mimic",
            health=40,
            strength=2,
            dexterity=14,
            hostility_range=1
        )

        self.disguised = True
        self.revealed = False

        # Mimic disguises as random item
        self.disguise_item = random.choice([
            ItemType.WEAPON,
            ItemType.FOOD,
            ItemType.TREASURE
        ])

    def reveal(self):
        """Reveal mimic when player interacts"""
        if self.disguised:
            self.disguised = False
            self.revealed = True
            self.hostility = True
            print("The item was a Mimic!")

    def interact(self, player):
        """Player interacts with mimic"""
        if self.disguised:
            self.reveal()
            return "mimic"

    def get_symbol(self):
        """Return correct symbol"""
        if self.disguised:
            return self.disguise_item.get_symbol()
        return "m"

    def get_name(self):
        if self.disguised:
            return self.disguise_item.name
        return "Mimic"