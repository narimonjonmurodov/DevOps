from __future__ import annotations

import curses
from pathlib import Path

from rogue.data.repository import JsonGameRepository, RunRecord
from rogue.domain.engine import GameEngine
from rogue.domain.models import ItemType


# Terminal UI that handles menus, input and rendering
class CursesApp:
    # Create engine and repository for game data
    def __init__(self) -> None:
        self.engine = GameEngine()
        self.repository = JsonGameRepository(Path(__file__).resolve().parents[1] / "data")

    # Start curses and enter the main program loop
    def run(self) -> None:
        curses.wrapper(self._main)

    # Main control: menus, loading and running game sessions
    def _main(self, stdscr: curses.window) -> None:
        curses.curs_set(0)
        stdscr.nodelay(False)
        stdscr.keypad(True)
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            self._init_colors()

        # Loop while condition
        while True:
            action = self._main_menu(stdscr)
            if action == "quit":
                return
            if action == "scores":
                self._show_scores(stdscr)
                continue
            session = self.repository.load_session() if action == "continue" else self.engine.new_session()
            if session is None:
                session = self.engine.new_session()
            self.engine.update_visibility(session)
            result = self._game_loop(stdscr, session)
            if result in {"died", "won"}:
                self.repository.append_record(
                    RunRecord.from_statistics(session.statistics, "victory" if result == "won" else "defeat")
                )
                self.repository.clear_session()

    # Let player choose new, continue, scores or quit
    def _main_menu(self, stdscr: curses.window) -> str:
        options = [("new", "New Game"), ("continue", "Continue"), ("scores", "Scoreboard"), ("quit", "Quit")]
        selected = 0
        # Loop while condition
        while True:
            stdscr.erase()
            stdscr.addstr(2, 4, "ROGUE", curses.A_BOLD)
            stdscr.addstr(4, 4, "WASD move, h/j/k/e use items, q save and quit")
            can_continue = self.repository.load_session() is not None
            for index, (value, label) in enumerate(options):
                text = label if value != "continue" or can_continue else "Continue (no save)"
                attr = curses.A_REVERSE if index == selected else curses.A_NORMAL
                stdscr.addstr(7 + index, 6, text, attr)
            stdscr.refresh()
            key = stdscr.getch()
            if key in (curses.KEY_UP, ord("w")):
                selected = (selected - 1) % len(options)
            elif key in (curses.KEY_DOWN, ord("s")):
                selected = (selected + 1) % len(options)
            elif key in (10, 13, curses.KEY_ENTER):
                chosen = options[selected][0]
                if chosen == "continue" and not can_continue:
                    continue
                return chosen

    # Run game frames until save, death or victory
    def _game_loop(self, stdscr: curses.window, session) -> str:
        # Loop while condition
        while True:
            self._render(stdscr, session)
            if session.game_over:
                footer = "Victory" if session.completed else "Game Over"
                self._pause_message(stdscr, f"{footer}. Press any key.")
                return "won" if session.completed else "died"

            key = stdscr.getch()
            if key == ord("q"):
                self.repository.save_session(session)
                self._pause_message(stdscr, "Game saved. Press any key.")
                return "saved"
            direction = self._movement_key(key)
            if direction is not None:
                self.engine.handle_player_move(session, direction)
                if session.current_level > session.statistics.deepest_level:
                    session.statistics.deepest_level = session.current_level
                self.repository.save_session(session)
            elif key == ord("h"):
                self._prompt_item_use(stdscr, session, ItemType.WEAPON, allow_empty_hands=True)
                self.repository.save_session(session)
            elif key == ord("j"):
                self._prompt_item_use(stdscr, session, ItemType.FOOD)
                self.repository.save_session(session)
            elif key == ord("k"):
                self._prompt_item_use(stdscr, session, ItemType.ELIXIR)
                self.repository.save_session(session)
            elif key == ord("e"):
                self._prompt_item_use(stdscr, session, ItemType.SCROLL)
                self.repository.save_session(session)

    # Draw the map, player stats and message log on screen
    def _render(self, stdscr: curses.window, session) -> None:
        stdscr.erase()
        rows = self.engine.render_grid(session)
        for row_index, row in enumerate(rows):
            try:
                stdscr.addstr(row_index, 0, row)
            except curses.error:
                pass
        info_x = session.level.width + 2
        player = session.player
        stats = [
            f"Level: {session.current_level}/{21}",
            f"HP: {player.health}/{player.max_health}",
            f"STR: {player.strength}",
            f"AGI: {player.agility}",
            f"Gold: {player.backpack.treasure}",
            f"Weapon: {player.equipped_weapon.name if player.equipped_weapon else 'None'}",
            f"Food: {len(player.backpack.food)}",
            f"Elixirs: {len(player.backpack.elixirs)}",
            f"Scrolls: {len(player.backpack.scrolls)}",
            f"Weapons: {len(player.backpack.weapons)}",
        ]

        info_x = session.level.width + 2

        for index, line in enumerate(stats):
            try:
                stdscr.addstr(index, info_x, line)
            except curses.error:
                pass

        for row_index, row in enumerate(rows):
            for col_index, char in enumerate(row):
                try:
                    color = self._get_color(char)
                    stdscr.addstr(row_index, col_index, char, color)
                except curses.error:
                    pass

        log_y = 12
        try:
            stdscr.addstr(log_y, info_x, "Log:")
        except curses.error:
            pass
        for index, message in enumerate(session.message_log.messages[-6:]):
            try:
                stdscr.addstr(log_y + 1 + index, info_x, message[:40])
            except curses.error:
                pass
        stdscr.refresh()

    # Show a small menu to choose an item to use
    def _prompt_item_use(self, stdscr: curses.window, session, item_type: ItemType, allow_empty_hands: bool = False) -> None:
        bucket = session.player.backpack.bucket_for(item_type)
        if not bucket and not (allow_empty_hands and session.player.equipped_weapon is not None):
            session.message_log.add("Nothing to use.")
            return

        choices = [f"{index + 1}. {item.name}" for index, item in enumerate(bucket)]
        if allow_empty_hands and session.player.equipped_weapon is not None:
            choices.insert(0, "0. Unequip current weapon")

        height = max(8, len(choices) + 4)
        width = 42
        window = curses.newwin(height, width, 2, 8)
        window.box()
        title = f"Choose {item_type.value}"
        window.addstr(1, 2, title)
        for index, choice in enumerate(choices[:9]):
            window.addstr(2 + index, 2, choice[: width - 4])
        window.refresh()
        key = stdscr.getch()
        if allow_empty_hands and key == ord("0"):
            self.engine.use_item(session, item_type, -1)
            return
        if ord("1") <= key <= ord("9"):
            chosen = key - ord("1")
            self.engine.use_item(session, item_type, chosen)

    # Display saved top runs from the scoreboard
    def _show_scores(self, stdscr: curses.window) -> None:
        records = self.repository.load_records()
        stdscr.erase()
        stdscr.addstr(1, 2, "Scoreboard", curses.A_BOLD)
        if not records:
            stdscr.addstr(3, 2, "No runs saved yet.")
        else:
            for index, record in enumerate(records[:10], start=1):
                line = (
                    f"{index:02d}. gold={record.treasure_collected} "
                    f"level={record.deepest_level} kills={record.enemies_defeated} "
                    f"result={record.result}"
                )
                stdscr.addstr(2 + index, 2, line[: min(len(line), 100)])
        stdscr.addstr(16, 2, "Press any key to return.")
        stdscr.refresh()
        stdscr.getch()

    # Show a message at bottom and wait for a key
    def _pause_message(self, stdscr: curses.window, message: str) -> None:
        height, width = stdscr.getmaxyx()
        stdscr.addstr(height - 2, 2, message[: max(1, width - 4)])
        stdscr.refresh()
        stdscr.getch()

    # Map keys to movement directions
    def _movement_key(self, key: int) -> str | None:
        mapping = {
            ord("w"): "w",
            ord("a"): "a",
            ord("s"): "s",
            ord("d"): "d",
            curses.KEY_UP: "w",
            curses.KEY_LEFT: "a",
            curses.KEY_DOWN: "s",
            curses.KEY_RIGHT: "d",
        }
        return mapping.get(key)

    # Define color pairs used in UI if supported
    def _init_colors(self) -> None:
        curses.init_pair(1, curses.COLOR_CYAN, -1)  # Player
        curses.init_pair(2, curses.COLOR_GREEN, -1)  # Zombie
        curses.init_pair(3, curses.COLOR_RED, -1)  # Vampire
        curses.init_pair(4, curses.COLOR_WHITE, -1)  # Ghost
        curses.init_pair(5, curses.COLOR_YELLOW, -1)  # Ogre
        curses.init_pair(6, curses.COLOR_MAGENTA, -1)  # Snake Mage
        curses.init_pair(7, curses.COLOR_YELLOW, -1)  # Treasure
        curses.init_pair(8, curses.COLOR_GREEN, -1)  # Food
        curses.init_pair(9, curses.COLOR_MAGENTA, -1)  # Elixir
        curses.init_pair(10, curses.COLOR_WHITE, -1)  # Scroll
        curses.init_pair(11, curses.COLOR_RED, -1)  # Weapon
        curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Walls

    def _get_color(self, char):

        # Player
        if char == "@":
            return curses.color_pair(1)

        # Enemies
        if char == "z":  # Zombie
            return curses.color_pair(2)

        if char == "v":  # Vampire
            return curses.color_pair(3)

        if char == "g":  # Ghost
            return curses.color_pair(4)

        if char == "o":  # Ogre
            return curses.color_pair(5)

        if char == "s":  # Snake Mage
            return curses.color_pair(6)

        # Items
        if char == "$":  # Treasure
            return curses.color_pair(7)

        if char == "f":  # Food
            return curses.color_pair(8)

        if char == "!":  # Elixir
            return curses.color_pair(9)

        if char == "?":  # Scroll
            return curses.color_pair(10)

        if char == ")":  # Weapon
            return curses.color_pair(11)

        # Environment
        if char == "#":  # Wall
            return curses.color_pair(12)

        # Default
        return curses.A_NORMAL