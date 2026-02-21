from flask import Flask, render_template, flash, redirect, url_for
from .models import db
import os
from werkzeug.exceptions import RequestEntityTooLarge

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "supersecretkey"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/images/avatars")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 *1024
    app.json.sort_keys = False

    db.init_app(app)

    from .memes.routes import meme_bp
    from .exam.routes import exam_bp
    from .auth.routes import auth_bp
    from .game.routes import game_bp
    from .message.routes import msg_bp

    app.register_blueprint(meme_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(msg_bp)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        flash("Image Too Large! Maximum size is 2MB.", "danger")
        return redirect(url_for("auth.sett"))

    @app.route("/")
    def home():
        return render_template("home.html")
    
    return app