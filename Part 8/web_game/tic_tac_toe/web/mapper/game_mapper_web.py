from tic_tac_toe.domain.model.board import GameBoard
from tic_tac_toe.domain.model.game import CurrentGame

from tic_tac_toe.web.model.game_board_web import GameBoardWeb
from tic_tac_toe.web.model.current_game_web import CurrentGameWeb


class GameMapperWeb:

    @staticmethod
    def to_domain(game_web: CurrentGameWeb) -> CurrentGame:

        board = GameBoard(game_web.board.board)

        return CurrentGame(
            game_web.game_id,
            board
        )

    @staticmethod
    def to_web(game: CurrentGame) -> CurrentGameWeb:

        board_web = GameBoardWeb(game.board.board)

        return CurrentGameWeb(
            game.game_id,
            board_web
        )