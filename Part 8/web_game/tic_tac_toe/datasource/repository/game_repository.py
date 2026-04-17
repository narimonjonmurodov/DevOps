from tic_tac_toe.datasource.repository.storage import Storage
from tic_tac_toe.datasource.mapper.game_mapper_ds import GameMapperDS
from tic_tac_toe.domain.model.game import CurrentGame
import uuid

class GameRepository:

    def __init__(self, storage: Storage):
        self.storage = storage

    def save(self, game: CurrentGame) -> None:

        game_ds =  GameMapperDS.to_datasource(game)

        self.storage.save(game_ds)

    def get(self, game_id: uuid.UUID) -> CurrentGame | None:

        game_ds = self.storage.get(game_id)

        if not game_ds:
            return None

        return GameMapperDS.to_domain(game_ds)