import uuid
from .board import GameBoard
from typing import List


class CurrentGame:
    def __init__(self, game_id: uuid.UUID, board: GameBoard):
        self.game_id = game_id
        self.board = board

    def get_board(self) -> List[List[int]]:
        return self.board.board

    def set_board(self, board: List[List[int]]):
        self.board.board = board