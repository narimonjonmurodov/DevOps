from tic_tac_toe.web.route.game_controller import game_blueprint
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.register_blueprint(game_blueprint)

    # UI route
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("index.html")

    return app