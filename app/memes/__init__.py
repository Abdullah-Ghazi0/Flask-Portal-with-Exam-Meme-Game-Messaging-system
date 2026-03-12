from flask import Blueprint

meme_bp = Blueprint("meme", __name__, url_prefix="/memes", template_folder="templates")

from . import routes