from tic_tac_toe.domain.model.board import GameBoard
from tic_tac_toe.domain.model.game import CurrentGame

from tic_tac_toe.datasource.model.game_board_ds import GameBoardDS
from tic_tac_toe.datasource.model.current_game_ds import CurrentGameDS


class GameMapperDS:

    @staticmethod
    def to_datasource(game: CurrentGame) -> CurrentGameDS:

        board_ds = GameBoardDS(game.get_board())

        return CurrentGameDS(
            game.game_id,
            board_ds
        )


    @staticmethod
    def to_domain(game_ds: CurrentGameDS) -> CurrentGame:

        board = GameBoard(game_ds.get_board())

        return CurrentGame(
            game_ds.game_id,
            board
        )