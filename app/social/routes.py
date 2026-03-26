from flask import render_template
from ..models import Users
from . import social_bp

@social_bp.route("/u/<username>")
def view_profile(username):

    user = Users.query.filter_by(username=username).first()
    if user:
        return render_template("social/profile.html", user=user)
    
    return render_template("page_not_found.html")
    