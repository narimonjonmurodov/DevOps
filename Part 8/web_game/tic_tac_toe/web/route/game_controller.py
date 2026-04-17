from flask import Blueprint, request, jsonify

from tic_tac_toe.web.mapper.game_mapper_web import GameMapperWeb
from tic_tac_toe.web.model.current_game_web import CurrentGameWeb
from tic_tac_toe.web.model.game_board_web import GameBoardWeb

from tic_tac_toe.di.container import Container


game_blueprint = Blueprint("game", __name__)

container = Container()
mapper = GameMapperWeb()


@game_blueprint.route("/game/<game_id>", methods=["POST"])
def play(game_id):
    try:
        data = request.json

        board = GameBoardWeb(data["board"])

        game_web = CurrentGameWeb(
            game_id,
            board
        )

        service = container.service

        game_domain = mapper.to_domain(game_web)

        result = service.next_move(game_domain)

        result_web = mapper.to_web(result)

        if service.is_finished(result):
            return jsonify({
                "game_id": result_web.game_id,
                "board": result_web.get_board(),
                "is_finished": True,
                "result": service.check_winner(result_web.get_board())
            })

        else:
            return jsonify({
                "game_id": result_web.game_id,
                "board": result_web.get_board(),
                "is_finished": False
            })

    except ValueError:
        return jsonify({
            "error": "Invalid game board"
        }), 400