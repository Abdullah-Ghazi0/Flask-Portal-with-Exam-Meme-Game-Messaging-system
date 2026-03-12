from flask import session
from ..models import Words
from sqlalchemy import func
import random

def random_word():
    w = Words.query.order_by(func.random()).first()
    word_text = w.word
    known_char = w.k_char
    return word_text, known_char

def game_start():
    w, c = random_word()
    hints = random.sample(w, k=c)

    session["word"] = w
    session["guessed"] = hints
    session["lives"] = 6


def winorloss():
    if all(l in session['guessed'] for l in session['word']):
        return "win"
    if session["lives"] <= 0:
        return "loss"
    
def find_known_char(word):
    word_len = len(word)
    if word_len <= 4:
        known_char = 0
    elif word_len <= 8:
        known_char = 1
    elif word_len <= 13:
        known_char = 2
    else:
        known_char = 3

    return known_char


