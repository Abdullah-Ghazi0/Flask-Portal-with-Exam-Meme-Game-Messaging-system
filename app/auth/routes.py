import os
from flask import render_template, session, redirect, url_for, request, flash, current_app
from ..models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import auth_bp


@auth_bp.route("/register", methods=["GET","POST"])
def reg():
    
    if request.method == "POST":
        uname = request.form.get("username")
        pword = request.form.get("password")
        dname = request.form.get("display")

        hashed_pw = generate_password_hash(pword)

        if Users.query.filter_by(username=uname).first():
            flash("This username is taken!", 'danger')
        else:
            user = Users(
                username = uname,
                displayname = dname,
                password = hashed_pw
            )
            db.session.add(user)
            db.session.commit()
            flash("Registered Sccessfully!", 'success')
            return redirect(url_for('auth.login'))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET","POST"])
def login():
    
    if request.method == "POST":
        log_uname = request.form.get("username")
        log_pword = request.form.get("password")

        user = Users.query.filter_by(username=log_uname).first()
        if user and check_password_hash(user.password, log_pword):
            session["user_id"] = user.id

            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], user.picture)
            if os.path.exists(filepath):
                session["profile_picture"] = user.picture
            else:
                session["profile_picture"] = "default.png"
            flash("Login Sccessful!", 'success')
            return redirect(url_for('user.profile'))

        else:
            flash("Wrong Username or Password!", 'danger')

    return render_template("auth/login.html")

    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logout Successful!", 'success')
    return redirect(url_for('home'))

    