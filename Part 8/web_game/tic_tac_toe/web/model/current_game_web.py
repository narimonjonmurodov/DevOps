from tic_tac_toe.web.model.game_board_web import GameBoardWeb
from typing import List
import uuid


class CurrentGameWeb:

    def __init__(self, game_id: uuid.UUID, board: GameBoardWeb):
        self.game_id = game_id
        self.board = board

    def get_board(self) -> List[List[int]]:
        return self.board.board