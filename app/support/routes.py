from flask import render_template
from . import support_bp
from ..models import Reports

@support_bp.route("/report")
def report():
    return