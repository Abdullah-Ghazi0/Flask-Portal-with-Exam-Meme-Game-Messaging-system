from flask import Blueprint

msg_bp = Blueprint("message", __name__, url_prefix="/message")

from . import routes