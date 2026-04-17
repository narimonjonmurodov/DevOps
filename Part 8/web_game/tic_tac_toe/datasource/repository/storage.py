import threading
from tic_tac_toe.datasource.model.current_game_ds import CurrentGameDS
import uuid

class Storage:

    def __init__(self):
        self._lock = threading.Lock()
        self._games = {}

    def save(self, game: CurrentGameDS) -> None:

        with self._lock:
            self._games[game.game_id] = game

    def get(self, game_id: uuid.UUID) -> CurrentGameDS:

        with self._lock:
            return self._games.get(game_id)