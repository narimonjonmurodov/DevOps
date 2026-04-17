from tic_tac_toe.datasource.model.game_board_ds import GameBoardDS
from typing import List
import uuid

class CurrentGameDS:

    def __init__(self, game_id: uuid.UUID, board: GameBoardDS):
        self.game_id = game_id
        self.board = board

    def get_board(self) -> List[List[int]]:
        return self.board.board