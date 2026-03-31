import os
from datetime import datetime, timezone
from flask import redirect, url_for, flash
from sqlalchemy import case
from ..models import db, Reports

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

def banUser(userToActOn):
    userToActOn.status = "banned"
    userToActOn.status_changed_at = datetime.now(timezone.utc)
    userToActOn.profile.verified = False
    userToActOn.profile.displayname = "Banned User"
    userToActOn.profile.picture = "default.png"
    
    db.session.commit()
    flash("User Banned successfully!", 'success')
    return redirect(url_for('admin.manage_user'))


priority = case(
    (Reports.catagory == "abuse" , 1),
    (Reports.catagory == "inappropriateContent" , 2),
    (Reports.catagory == "spam" , 3),
    else_=4
)