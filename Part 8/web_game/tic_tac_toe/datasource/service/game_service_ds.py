from tic_tac_toe.domain.model.game import CurrentGame
from tic_tac_toe.datasource.repository.game_repository import GameRepository
from tic_tac_toe.domain.service.game_service_impl import GameServiceImpl

class GameServiceDS(GameServiceImpl):

    def __init__(self, repository: GameRepository):
        self.repository = repository

    def next_move(self, new_game: CurrentGame) -> CurrentGame:

        stored = self.repository.get(new_game.game_id)

        if stored is not None and super().is_finished(stored):
            return stored

        if not super().validate(stored, new_game):
            raise ValueError("Invalid")

        super().next_move(new_game)

        self.repository.save(new_game)

        return new_game
