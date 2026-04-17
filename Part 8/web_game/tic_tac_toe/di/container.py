from tic_tac_toe.datasource.repository.storage import Storage
from tic_tac_toe.datasource.repository.game_repository import GameRepository
from tic_tac_toe.datasource.service.game_service_ds import GameServiceDS


class Container:

    def __init__(self):

        # Singleton storage
        self.storage = Storage()

        # Repository
        self.repository = GameRepository(self.storage)

        # Service
        self.service = GameServiceDS(self.repository)