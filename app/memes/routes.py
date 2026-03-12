from flask import render_template, session, flash, redirect, url_for
from .meme_api import memer
from . import meme_bp

@meme_bp.route("/")
def show_meme():
    if "user_id" not in session:
        flash("Please login first!", 'danger')
        return redirect(url_for('auth.login'))
    
    meme_post = memer()
    return render_template("memes/meme.html", meme=meme_post)