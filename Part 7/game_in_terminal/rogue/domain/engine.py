from __future__ import annotations

import math
import random
from collections import deque

from rogue.domain.generation import generate_level, spawn_position_in_start
from rogue.domain.models import (
    TOTAL_LEVELS,
    ActiveEffect,
    Character,
    EffectStat,
    Enemy,
    EnemyType,
    GameSession,
    Item,
    ItemType,
    Level,
    MessageLog,
    Position,
    Statistics,
    Tile,
)


CARDINALS = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}
ALL_DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
DIAGONALS = [(-1, -1), (1, -1), (1, 1), (-1, 1)]


# Core game logic: actions, enemy AI, and rules
class GameEngine:
    # Initialize RNG used to generate levels and seeds
    def __init__(self, seed: int | None = None) -> None:
        self._seed_rng = random.Random(seed)

    # Start a fresh game with a generated first level
    def new_session(self) -> GameSession:
        """Create a brand new run with a generated first level."""
        level_seed = self._seed_rng.randrange(1_000_000_000)
        level, next_enemy_id = generate_level(1, next_enemy_id=1, seed=level_seed)
        player_rng = random.Random(level_seed ^ 0xA5A5)
        player = Character(
            position=spawn_position_in_start(level, player_rng),
            max_health=30,
            health=30,
            agility=6,
            strength=5,
        )
        session = GameSession(
            player=player,
            level=level,
            current_level=1,
            statistics=Statistics(deepest_level=1),
            message_log=MessageLog(messages=["Find the stairs and survive."]),
            next_enemy_id=next_enemy_id,
        )
        self.update_visibility(session)
        return session

    # Move to next level while preserving player state
    def advance_level(self, session: GameSession) -> None:
        """Replace the current floor while preserving the player state."""
        if session.current_level >= TOTAL_LEVELS:
            session.completed = True
            session.game_over = True
            session.message_log.add("You escaped the dungeon.")
            return

        session.current_level += 1
        session.statistics.deepest_level = max(session.statistics.deepest_level, session.current_level)
        level_seed = self._seed_rng.randrange(1_000_000_000)
        level, session.next_enemy_id = generate_level(session.current_level, session.next_enemy_id, seed=level_seed)
        player_rng = random.Random(level_seed ^ 0x55AA)
        session.level = level
        session.player.position = spawn_position_in_start(level, player_rng)
        session.message_log.add(f"Level {session.current_level} begins.")
        session.level.sync_room_contents()
        self.update_visibility(session)

    # Handle movement, attacks, pickups and level change
    def handle_player_move(self, session: GameSession, command: str) -> bool:
        """Process one player action and, if valid, consume one full turn."""
        if session.game_over:
            return False
        if session.player.sleeping_turns > 0:
            session.player.sleeping_turns -= 1
            session.message_log.add("You are asleep and lose the turn.")
            self._end_turn(session)
            return True

        dx, dy = CARDINALS[command]
        target = session.player.position.shifted(dx, dy)
        if not session.level.in_bounds(target):
            return False

        enemy = session.level.enemy_at(target)
        if enemy is not None:
            # Walking into an occupied enemy tile is the player's attack action.
            self._attack_player_to_enemy(session, enemy)
            self._end_turn(session)
            return True

        if not session.level.walkable(target):
            return False

        session.player.position = target
        session.statistics.tiles_walked += 1
        self._pickup_item(session)
        if target.x == session.level.exit_position.x and target.y == session.level.exit_position.y:
            session.message_log.add("You descend deeper.")
            self.advance_level(session)
            return True

        self._end_turn(session)
        return True

    # Use or equip an item and apply its effects
    def use_item(self, session: GameSession, item_type: ItemType, index: int) -> bool:
        player = session.player
        if item_type is ItemType.WEAPON and index == -1:
            if player.equipped_weapon is None:
                session.message_log.add("Hands already empty.")
                return False
            if not self._drop_item_near_player(session, player.equipped_weapon):
                session.message_log.add("No space to drop the weapon.")
                return False
            session.message_log.add(f"You unequip {player.equipped_weapon.name}.")
            player.equipped_weapon = None
            self._end_turn(session)
            return True

        bucket = player.backpack.bucket_for(item_type)
        if not 0 <= index < len(bucket):
            return False
        item = player.backpack.remove_item(item_type, index)

        if item_type is ItemType.FOOD:
            healed = min(item.health, player.max_health - player.health)
            player.health += healed
            session.statistics.food_eaten += 1
            session.message_log.add(f"You eat {item.name} and restore {healed} HP.")
        elif item_type is ItemType.SCROLL:
            self._apply_permanent_item(player, item)
            session.statistics.scrolls_read += 1
            session.message_log.add(f"You read {item.name}.")
        elif item_type is ItemType.ELIXIR:
            self._apply_temporary_item(player, item)
            session.statistics.elixirs_used += 1
            session.message_log.add(f"You drink {item.name}.")
        elif item_type is ItemType.WEAPON:
            if player.equipped_weapon is not None and not self._drop_item_near_player(session, player.equipped_weapon):
                player.backpack.weapons.insert(index, item)
                session.message_log.add("No space to switch weapon.")
                return False
            if player.equipped_weapon is not None:
                session.message_log.add(f"You drop {player.equipped_weapon.name}.")
            player.equipped_weapon = item
            session.message_log.add(f"You equip {item.name}.")
        else:
            return False

        self._end_turn(session)
        return True

    # Compute which tiles the player can currently see
    def update_visibility(self, session: GameSession) -> None:
        level = session.level
        player_position = session.player.position
        visible: set[tuple[int, int]] = set()

        room = level.room_for_position(player_position)
        if room is not None:
            for y in range(room.y1, room.y2 + 1):
                for x in range(room.x1, room.x2 + 1):
                    visible.add((x, y))

        radius = 8
        # Rooms are revealed whole, while corridors rely on line-of-sight checks.
        for y in range(max(0, player_position.y - radius), min(level.height, player_position.y + radius + 1)):
            for x in range(max(0, player_position.x - radius), min(level.width, player_position.x + radius + 1)):
                if self._line_of_sight(level, player_position, Position(x, y)):
                    visible.add((x, y))

        level.visible = visible
        level.explored.update(visible)

    # Produce a list of text rows representing current view
    def render_grid(self, session: GameSession) -> list[str]:
        level = session.level
        rows: list[str] = []
        for y in range(level.height):
            chars: list[str] = []
            for x in range(level.width):
                position = Position(x, y)
                if (x, y) not in level.explored:
                    chars.append(" ")
                    continue
                if session.player.position.x == x and session.player.position.y == y:
                    chars.append("@")
                    continue

                enemy = level.enemy_at(position)
                if enemy and (x, y) in level.visible and not enemy.invisible:
                    chars.append(self._enemy_glyph(enemy.enemy_type))
                    continue

                item = level.item_at(position)
                if item and (x, y) in level.visible:
                    chars.append(self._item_glyph(item.item_type))
                    continue

                tile = level.tile_at(position)
                if (x, y) in level.visible:
                    chars.append(tile)
                elif tile in {Tile.WALL.value, Tile.EXIT.value, Tile.CORRIDOR.value, Tile.FLOOR.value}:
                    chars.append(Tile.WALL.value)
                else:
                    chars.append(" ")
            rows.append("".join(chars))
        return rows

    # Progress timed effects, let enemies act, update sight
    def _end_turn(self, session: GameSession) -> None:
        # One turn = expire timed effects, let every enemy act, then refresh vision.
        self._tick_effects(session)
        self._move_enemies(session)
        session.level.sync_room_contents()
        self.update_visibility(session)
        self._check_game_over(session)

    # Pick up an item if player stands on one
    def _pickup_item(self, session: GameSession) -> None:
        item = session.level.item_at(session.player.position)
        if item is None:
            return
        if session.player.backpack.add_item(item):
            session.level.items.remove(item)
            if item.item_type is ItemType.TREASURE:
                session.statistics.treasure_collected = session.player.backpack.treasure
            session.message_log.add(f"Picked up {item.name}.")
        else:
            session.message_log.add("Backpack is full for that item type.")

    # Player attacks enemy; handle special cases
    def _attack_player_to_enemy(self, session: GameSession, enemy: Enemy) -> None:
        if enemy.enemy_type is EnemyType.VAMPIRE and not enemy.first_hit_negated:
            enemy.first_hit_negated = True
            session.message_log.add("The first strike against the vampire misses.")
            return
        if not self._roll_hit(session.player.agility, enemy.agility):
            session.message_log.add("You miss.")
            return
        damage = self._calculate_damage(session.player.strength, session.player.equipped_weapon)
        enemy.health -= damage
        session.statistics.hits_dealt += 1
        session.message_log.add(f"You hit {enemy.enemy_type.value} for {damage}.")
        if enemy.health <= 0:
            self._kill_enemy(session, enemy)

    # Remove enemy and give treasure reward
    def _kill_enemy(self, session: GameSession, enemy: Enemy) -> None:
        session.level.enemies = [existing for existing in session.level.enemies if existing.enemy_id != enemy.enemy_id]
        # Reward grows with both enemy danger and current floor depth.
        minimum = max(1, session.current_level // 2)
        maximum = enemy.hostility_range + enemy.strength + enemy.agility + enemy.max_health // 4 + session.current_level * 2
        treasure = random.randint(minimum, maximum)
        session.player.backpack.treasure += treasure
        session.statistics.treasure_collected = session.player.backpack.treasure
        session.statistics.enemies_defeated += 1
        session.message_log.add(f"{enemy.enemy_type.value.title()} falls. Treasure +{treasure}.")

    # Update each enemy's behavior and actions
    def _move_enemies(self, session: GameSession) -> None:
        for enemy in list(session.level.enemies):
            if enemy.health <= 0:
                continue
            if enemy.enemy_type is EnemyType.GHOST:
                # Ghosts keep blinking and re-rolling their in-room position.
                enemy.phase += 1
                if enemy.phase % 3 == 0:
                    enemy.invisible = not enemy.invisible
                self._teleport_within_room(session.level, enemy)

            distance = self._distance(enemy.position, session.player.position)
            if distance <= enemy.hostility_range:
                enemy.is_chasing = True
                enemy.behavior = "chasing"

            if enemy.cooldown > 0:
                enemy.behavior = "resting"
                enemy.cooldown -= 1
                # Ogre pattern is intentionally attack -> rest -> guaranteed counterattack.
                if enemy.enemy_type is EnemyType.OGRE and enemy.cooldown == 0:
                    enemy.counterattack_ready = True
                continue

            if enemy.is_chasing:
                enemy.behavior = "chasing"
                self._move_enemy_towards_player(session, enemy)
            else:
                enemy.behavior = "patrolling"
                self._move_enemy_by_pattern(session, enemy)

            if self._distance(enemy.position, session.player.position) == 1:
                guaranteed_hit = enemy.enemy_type is EnemyType.OGRE and enemy.counterattack_ready
                self._enemy_attack(session, enemy, guaranteed_hit=guaranteed_hit)

    # Enemy attacks player and applies special effects
    def _enemy_attack(self, session: GameSession, enemy: Enemy, guaranteed_hit: bool = False) -> None:
        if enemy.enemy_type is EnemyType.OGRE and enemy.cooldown > 0:
            return
        if not guaranteed_hit and not self._roll_hit(enemy.agility, session.player.agility):
            session.message_log.add(f"{enemy.enemy_type.value.title()} misses.")
            return
        damage = max(1, enemy.strength + random.randint(0, 2) - session.player.agility // 5)
        session.player.health -= damage
        session.statistics.hits_taken += 1
        attack_label = "counterattacks" if guaranteed_hit else "hits"
        session.message_log.add(f"{enemy.enemy_type.value.title()} {attack_label} you for {damage}.")
        if enemy.enemy_type is EnemyType.VAMPIRE:
            session.player.max_health = max(1, session.player.max_health - 1)
            session.player.health = min(session.player.health, session.player.max_health)
            session.message_log.add("The vampire drains your vitality.")
        elif enemy.enemy_type is EnemyType.SNAKE_MAGE and random.random() < 0.35:
            session.player.sleeping_turns = max(session.player.sleeping_turns, 1)
            session.message_log.add("Sleep spell hits you.")
        elif enemy.enemy_type is EnemyType.OGRE:
            enemy.counterattack_ready = False
            enemy.cooldown = 1

    # Move enemy along shortest path toward player
    def _move_enemy_towards_player(self, session: GameSession, enemy: Enemy) -> None:
        path = self._bfs_path(session.level, enemy.position, session.player.position)
        if len(path) < 2:
            # No path means the enemy falls back to its idle movement pattern.
            self._move_enemy_by_pattern(session, enemy)
            return
        step_count = 2 if enemy.enemy_type is EnemyType.OGRE else 1
        for step in path[1 : 1 + step_count]:
            if step.x == session.player.position.x and step.y == session.player.position.y:
                break
            if session.level.enemy_at(step) is None:
                enemy.position = step

    # Move enemy according to its patrol pattern
    def _move_enemy_by_pattern(self, session: GameSession, enemy: Enemy) -> None:
        # Snake mages patrol diagonally; other enemies move cardinally.
        if enemy.enemy_type is EnemyType.SNAKE_MAGE:
            directions = DIAGONALS
        else:
            directions = ALL_DIRECTIONS
        start = enemy.phase % len(directions)
        enemy.phase += 1
        for offset in range(len(directions)):
            dx, dy = directions[(start + offset) % len(directions)]
            target = enemy.position.shifted(dx, dy)
            if self._can_enemy_step(session, target):
                enemy.position = target
                break

    # Teleport enemy to a random position in its room
    def _teleport_within_room(self, level: Level, enemy: Enemy) -> None:
        room = level.room_for_position(enemy.position)
        if room is None:
            return
        options = room.interior_positions()
        if options:
            enemy.position = random.choice(options)

    # Check if enemy can step into a tile
    def _can_enemy_step(self, session: GameSession, position: Position) -> bool:
        return (
            session.level.walkable(position)
            and session.level.enemy_at(position) is None
            and not (position.x == session.player.position.x and position.y == session.player.position.y)
        )

    # Find shortest walkable path with BFS
    def _bfs_path(self, level: Level, start: Position, goal: Position) -> list[Position]:
        """Return the shortest walkable path using 4-direction BFS."""
        queue: deque[Position] = deque([start])
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {(start.x, start.y): None}
        # Loop while condition
        while queue:
            current = queue.popleft()
            if current.x == goal.x and current.y == goal.y:
                break
            for dx, dy in ALL_DIRECTIONS:
                candidate = current.shifted(dx, dy)
                key = (candidate.x, candidate.y)
                if key in came_from or not level.walkable(candidate):
                    continue
                came_from[key] = (current.x, current.y)
                queue.append(candidate)

        if (goal.x, goal.y) not in came_from:
            return []

        path: list[Position] = []
        current_key: tuple[int, int] | None = (goal.x, goal.y)
        # Loop while condition
        while current_key is not None:
            path.append(Position(*current_key))
            current_key = came_from[current_key]
        path.reverse()
        return path

    # Probabilistic hit roll using agility difference
    def _roll_hit(self, attacker_agility: int, defender_agility: int) -> bool:
        # Clamp the result so agility matters without making combat deterministic.
        chance = max(0.2, min(0.9, 0.55 + (attacker_agility - defender_agility) * 0.04))
        return random.random() < chance

    # Compute damage including weapon bonus
    def _calculate_damage(self, strength: int, weapon: Item | None) -> int:
        bonus = 0 if weapon is None else weapon.strength
        return max(1, strength + bonus + random.randint(0, 3) - 1)

    # Apply permanent stat gains from items
    def _apply_permanent_item(self, player: Character, item: Item) -> None:
        if item.max_health:
            player.max_health += item.max_health
            player.health += item.max_health
        player.strength += item.strength
        player.agility += item.agility

    # Apply temporary buffs and record effects
    def _apply_temporary_item(self, player: Character, item: Item) -> None:
        # Timed buffs are tracked explicitly so they can expire turn-by-turn.
        if item.max_health:
            player.max_health += item.max_health
            player.health += item.max_health
            player.active_effects.append(ActiveEffect(EffectStat.MAX_HEALTH, item.max_health, item.duration))
        if item.strength:
            player.strength += item.strength
            player.active_effects.append(ActiveEffect(EffectStat.STRENGTH, item.strength, item.duration))
        if item.agility:
            player.agility += item.agility
            player.active_effects.append(ActiveEffect(EffectStat.AGILITY, item.agility, item.duration))

    # Decrease effect timers and remove expired ones
    def _tick_effects(self, session: GameSession) -> None:
        expired: list[ActiveEffect] = []
        for effect in session.player.active_effects:
            effect.remaining_turns -= 1
            if effect.remaining_turns <= 0:
                expired.append(effect)
        for effect in expired:
            session.player.active_effects.remove(effect)
            if effect.stat is EffectStat.MAX_HEALTH:
                # Expiring health buffs are never allowed to kill the player outright.
                session.player.max_health -= effect.amount
                session.player.health = max(1, min(session.player.health - effect.amount, session.player.max_health))
            elif effect.stat is EffectStat.STRENGTH:
                session.player.strength -= effect.amount
            elif effect.stat is EffectStat.AGILITY:
                session.player.agility -= effect.amount
            session.message_log.add(f"{effect.stat.value.replace('_', ' ')} bonus fades.")

    # Try to drop an item adjacent to player
    def _drop_item_near_player(self, session: GameSession, item: Item) -> bool:
        for dx, dy in ALL_DIRECTIONS:
            target = session.player.position.shifted(dx, dy)
            if session.level.walkable(target) and session.level.item_at(target) is None:
                item.position = target
                session.level.items.append(item)
                session.level.sync_room_contents()
                return True
        return False

    # Check visibility using Bresenham line algorithm
    def _line_of_sight(self, level: Level, start: Position, end: Position) -> bool:
        # Bresenham is enough here: fast, deterministic, and grid-friendly.
        for point in self._bresenham(start, end):
            if point.x == start.x and point.y == start.y:
                continue
            if level.tile_at(point) == Tile.VOID.value:
                return False
            if level.tile_at(point) == Tile.WALL.value and (point.x != end.x or point.y != end.y):
                return False
        return True

    # Generate straight-line points between two positions
    def _bresenham(self, start: Position, end: Position) -> list[Position]:
        points: list[Position] = []
        x1, y1 = start.x, start.y
        x2, y2 = end.x, end.y
        dx = abs(x2 - x1)
        dy = -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy
        # Loop while condition
        while True:
            points.append(Position(x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy
        return points

    # End game if player has no health
    def _check_game_over(self, session: GameSession) -> None:
        if session.player.health > 0:
            return
        session.game_over = True
        session.message_log.add("You died.")

    # Integer distance between two positions
    def _distance(self, a: Position, b: Position) -> int:
        return math.ceil(math.dist((a.x, a.y), (b.x, b.y)))

    # Map enemy types to single-character glyphs
    def _enemy_glyph(self, enemy_type: EnemyType) -> str:
        mapping = {
            EnemyType.ZOMBIE: "z",
            EnemyType.VAMPIRE: "v",
            EnemyType.GHOST: "g",
            EnemyType.OGRE: "O",
            EnemyType.SNAKE_MAGE: "s",
        }
        return mapping[enemy_type]

    # Map item types to single-character glyphs
    def _item_glyph(self, item_type: ItemType) -> str:
        mapping = {
            ItemType.FOOD: ":",
            ItemType.ELIXIR: "!",
            ItemType.SCROLL: "?",
            ItemType.WEAPON: ")",
            ItemType.TREASURE: "*",
        }
        return mapping[item_type]
