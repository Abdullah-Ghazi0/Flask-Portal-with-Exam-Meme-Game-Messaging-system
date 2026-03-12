from flask import Blueprint

game_bp = Blueprint("game", __name__, url_prefix="/game", template_folder="templates")

from . import routes