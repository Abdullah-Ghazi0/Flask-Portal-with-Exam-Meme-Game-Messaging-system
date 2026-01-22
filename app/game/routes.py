from flask import Blueprint, render_template, session, request, flash, redirect, url_for
from .word_adding import find_known_char
from ..models import db, Words
from .game_logic import game_start, winorloss

game_bp = Blueprint("game", __name__, url_prefix="/game")

@game_bp.route("/")
def game_play():
    if "user_id" not in session:
        flash("You need to login first!")
        return redirect(url_for("auth.login"))
    if "word" not in session:
        game_start()

    display = [letter if letter in session["guessed"] else '_' for letter in session["word"]]
    word_shown =" ".join(display)
    lives = session["lives"]
    mistakes = 6 - lives
    return render_template("game.html", word_shown=word_shown, lives=lives, mistakes=mistakes)

@game_bp.route("/guess", methods=["POST"])
def guessing():
    char = request.form.get("char").upper()
    if char in session["guessed"]:
        flash("You Already guessed this charater!")
    else:
        session["guessed"].append(char)
        if char not in session["word"]:
            session["lives"] -= 1
        session.modified = True

    status = winorloss()
    if status == "win":
        flash("Congratulations! You Won")
    if status == "loss":
        flash(f"GAME OVER! The word was :{session["word"]}")
    
    return redirect(url_for("game.game_play"))

@game_bp.route("/add-words", methods=["POST", "GET"])
def adding():
    if "user_id" in session and session["user_id"] == 1:
        if request.method == "POST":
            word = request.form.get("word")
            word = word.upper()

            word_len = len(word)

            new_word = Words(
                word = word,
                k_char = find_known_char(word_len)
            )
            db.session.add(new_word)
            db.session.commit()
            flash("Word Added Sccessfully!")
            return redirect(url_for("game.adding"))

        return render_template("adding_words.html")
    else:
        return "<h1>You are not allowed access this page!"
    
@game_bp.route("/playagain")
def again():
    session.pop("lives")
    session.pop("word")
    session.pop("guessed")
    print(session)
    return redirect(url_for("game.game_play"))