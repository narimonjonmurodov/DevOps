from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rogue.domain.models import GameSession, Statistics


@dataclass
# Small record storing a finished run's stats
class RunRecord:
    treasure_collected: int
    deepest_level: int
    enemies_defeated: int
    food_eaten: int
    elixirs_used: int
    scrolls_read: int
    hits_dealt: int
    hits_taken: int
    tiles_walked: int
    result: str

    @classmethod
    # Build a RunRecord from game statistics
    def from_statistics(cls, statistics: Statistics, result: str) -> "RunRecord":
        return cls(result=result, **statistics.to_dict())

    # Convert record to dict for JSON
    def to_dict(self) -> dict[str, Any]:
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
            "result": self.result,
        }

    @classmethod
    # Recreate record from saved dict
    def from_dict(cls, data: dict[str, Any]) -> "RunRecord":
        return cls(**data)


# Save and load game data to JSON files
class JsonGameRepository:
    # Set file paths and ensure data folder exists
    def __init__(self, base_path: Path) -> None:
        self.base_path = base_path
        self.save_path = base_path / "save.json"
        self.scoreboard_path = base_path / "scoreboard.json"
        self.base_path.mkdir(parents=True, exist_ok=True)

    # Save current game session to disk
    def save_session(self, session: GameSession) -> None:
        # Serialization format is defined by the domain objects themselves.
        self.save_path.write_text(
            json.dumps(session.to_dict(), ensure_ascii=True, indent=2),
            encoding="utf-8",
        )

    # Load saved session or return None
    def load_session(self) -> GameSession | None:
        if not self.save_path.exists():
            return None
        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        return GameSession.from_dict(data)

    # Remove saved session file
    def clear_session(self) -> None:
        if self.save_path.exists():
            self.save_path.unlink()

    # Add a run to scoreboard and keep it sorted
    def append_record(self, record: RunRecord) -> None:
        records = self.load_records()
        records.append(record)
        # Higher treasure always wins; deeper progress breaks ties.
        records.sort(key=lambda item: (-item.treasure_collected, -item.deepest_level, item.result))
        self.scoreboard_path.write_text(
            json.dumps([record.to_dict() for record in records], ensure_ascii=True, indent=2),
            encoding="utf-8",
        )

    # Read scoreboard file and return records
    def load_records(self) -> list[RunRecord]:
        if not self.scoreboard_path.exists():
            return []
        data = json.loads(self.scoreboard_path.read_text(encoding="utf-8"))
        return [RunRecord.from_dict(item) for item in data]
