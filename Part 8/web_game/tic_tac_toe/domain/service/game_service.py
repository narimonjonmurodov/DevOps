from abc import ABC, abstractmethod
from tic_tac_toe.domain.model.game import CurrentGame

class GameService(ABC):

    @abstractmethod
    def next_move(self, game: CurrentGame) -> CurrentGame:
        pass

    @abstractmethod
    def validate(self, old_game: CurrentGame, new_game: CurrentGame) -> bool:
        pass

    @abstractmethod
    def is_finished(self, game: CurrentGame) -> bool:
        pass