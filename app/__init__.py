from flask import Flask, render_template
from .models import db

def create_app():
    app = Flask(__name__)

    app.secret_key = "supersecretkey"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.json.sort_keys = False

    db.init_app(app)

    from .memes.routes import meme_bp
    from .exam.routes import exam_bp
    from .auth.routes import auth_bp
    from .game.routes import game_bp

    app.register_blueprint(meme_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)

    @app.route("/")
    def home():
        return render_template("home.html")
    
    return app