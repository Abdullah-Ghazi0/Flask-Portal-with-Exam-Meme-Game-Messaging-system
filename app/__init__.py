from flask import Flask, render_template, flash, redirect, url_for, session
from .models import Messages
import os
from werkzeug.exceptions import RequestEntityTooLarge
from dotenv import load_dotenv
from .extensions import db, migrate

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "supersecretkey"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/images/avatars")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 *1024
    app.config["FERNET_KEY"] = os.getenv("FERNET_KEY")

    app.json.sort_keys = False

    db.init_app(app)
    migrate.init_app(app, db)

    from .memes import meme_bp
    from .exam import exam_bp
    from .auth import auth_bp
    from .game import game_bp
    from .message import msg_bp
    from .user import user_bp

    app.register_blueprint(meme_bp)
    app.register_blueprint(exam_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(msg_bp)
    app.register_blueprint(user_bp)

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(e):
        flash("Image Too Large! Maximum size is 2MB.", "danger")
        return redirect(url_for("auth.sett"))

    @app.context_processor
    def unread_messages():
        if "user_id" in session:
            unread = Messages.query.filter_by(r_id=session["user_id"], read=False).first() is not None
            return {"has_unread_msgs": unread}
        return {"has_unread_msgs": False}
        
    @app.route("/")
    def home():
        return render_template("home.html")
    
    return app