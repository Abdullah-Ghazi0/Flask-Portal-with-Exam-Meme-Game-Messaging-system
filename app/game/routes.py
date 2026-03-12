from flask import render_template, session, request, flash, redirect, url_for
from ..models import db, Words, Users
from .game_logic import game_start, winorloss, find_known_char
from . import game_bp

@game_bp.route("/")
def game_play():
    if "user_id" not in session:
        flash("You need to login first!", 'danger')
        return redirect(url_for("auth.login"))
    if "word" not in session:
        game_start()

    display = [letter if letter in session["guessed"] else '_' for letter in session["word"]]
    word_shown =" ".join(display)
    lives = session["lives"]
    mistakes = 6 - lives
    return render_template("game/game.html", word_shown=word_shown, lives=lives, mistakes=mistakes)

@game_bp.route("/guess", methods=["POST"])
def guessing():
    char = request.form.get("char").upper()
    if char in session["guessed"]:
        flash("You Already guessed this charater!", 'info')
    else:
        session["guessed"].append(char)
        if char not in session["word"]:
            session["lives"] -= 1
        session.modified = True

    status = winorloss()
    if status == "win":
        flash("Congratulations! You Won", 'success')
    if status == "loss":
        flash(f"GAME OVER! The word was : {session["word"]}", 'danger')
    
    return redirect(url_for("game.game_play"))

@game_bp.route("/add-words", methods=["POST", "GET"])
def adding():
    if "user_id" not in session:
        flash("You need to login first!", 'danger')
        return redirect(url_for("auth.login"))
    
    user = Users.query.get(session.get("user_id"))

    if user.username == "admin":
        if request.method == "POST":
            word = request.form.get("word")
            word = word.upper()

            new_word = Words(
                word = word,
                k_char = find_known_char(word)
            )
            db.session.add(new_word)
            db.session.commit()
            
            flash("Word Added Sccessfully!", 'success')
            return redirect(url_for("game.adding"))

        return render_template("admin/adding_words.html")
    
    flash("You are not allowed access this page!")
    return redirect(url_for('home'))
    
@game_bp.route("/playagain")
def again():
    session.pop("lives")
    session.pop("word")
    session.pop("guessed")
    return redirect(url_for("game.game_play"))