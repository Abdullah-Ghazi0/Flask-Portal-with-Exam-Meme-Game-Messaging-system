import os
from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, session, current_app
from ..models import db, Questions, Users, Words
from .utils import find_known_char, banUser
from . import admin_bp


@admin_bp.route("/panel")
def panel():
    if "user_id" not in session:
        flash("Please Login to access your panel!", 'danger')
        return redirect(url_for('auth.login'))
    
    usrid = session.get("user_id")
    user = Users.query.get(usrid)

    if user.username == "admin":
        return render_template("admin/admin.html", user=user)
    
    flash("You are not allowed access this page!", 'danger')
    return redirect(url_for('home'))

@admin_bp.route("/create-exam", methods = ["GET","POST"])
def create_exam():
    if "user_id" not in session:
        flash("Please login first!", 'danger')
        return redirect(url_for('auth.login'))

    user = Users.query.get(session.get("user_id"))
    if user.username == "admin":

        if request.method == "POST":
            q = request.form.get("question")
            a = bool(request.form.get("answer"))

            question = Questions(
                q_text = q,
                answer = a
            )
            db.session.add(question)
            db.session.commit()

            flash("Question Added Sccessfully!", 'success')
            return redirect(url_for("admin.create_exam"))

        return render_template("admin/create_exam.html")

    flash("You are not allowed to access this page!", 'danger')
    return redirect(url_for('home'))

@admin_bp.route("/add-words", methods=["POST", "GET"])
def adding_word():
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
            return redirect(url_for("admin.adding_word"))

        return render_template("admin/adding_words.html")
    
    flash("You are not allowed access this page!", 'danger')
    return redirect(url_for('home'))

@admin_bp.route("/manage-users", methods=["POST", "GET"])
def manage_user():
    if "user_id" not in session:
        flash("You need to login first!", 'danger')
        return redirect(url_for("auth.login"))
    
    user = Users.query.get(session.get("user_id"))
    if user.username == "admin":
        if request.method == "POST":

            username = request.form.get("userToBan") if request.form.get("userToBan") else request.form.get("userToVerify")
            verification = request.form.get("verification") == "True"

            userToActOn = Users.query.filter_by(username=username).first()

            if userToActOn:
                if request.form.get("userToBan"):
                    banUser(userToActOn)
                else:
                    userToActOn.profile.verified = verification
                    db.session.commit()

                    flash("Action Completed!", 'success')
                    return redirect(url_for('admin.manage_user'))
                
            else:
                flash("User Not Found!", 'danger')
                return redirect(url_for('admin.manage_user'))

        return render_template("admin/manage_user.html")
    
    flash("You are not allowed access this page!", 'danger')
    return redirect(url_for('home'))