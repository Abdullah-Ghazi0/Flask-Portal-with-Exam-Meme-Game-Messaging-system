from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from ..models import db, Users
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import ProfilePicForm
import os
from werkzeug.utils import secure_filename

auth_bp = Blueprint("auth", __name__)


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

    return render_template("register.html")

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
            return redirect(url_for('auth.dash'))

        else:
            flash("Wrong Username or Password!", 'danger')

    return render_template("login.html")

@auth_bp.route("/profile")
def dash():
    if "user_id" in session:
        usrid = session.get("user_id")
        user = Users.query.get(usrid)
        name = user.username
        display_name = user.displayname
        if name == "admin":
            return render_template("admin.html", name=name)

        return render_template("dashboard.html", name=name, display_name=display_name)
    else:
        return "<h1>You need to login to access dashboard!"
    
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Logout Successful!", 'success')
    return redirect(url_for('home'))

@auth_bp.route("/settings", methods=["GET","POST"])
def sett():
    if "user_id" in session:
        user_id = session.get("user_id")

        user = Users.query.get(user_id)
        displayn = user.displayname

        # Changing Profile Picture

        form = ProfilePicForm()

        if request.method == "POST":

            if form.validate_on_submit():
                file = form.picture.data

                og_filename = secure_filename(file.filename)
                ext = og_filename.rsplit('.', 1)[1].lower()

                file_name = f"profile{user.id}.{ext}"
                file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], file_name)

                old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], f"profile{user.id}.{ext}")
                if os.path.exists(old_filepath):
                    os.remove(old_filepath)

                file.save(file_path)

                user.picture = file_name
                db.session.commit()

                session["profile_picture"] = file_name

                return redirect(url_for('auth.dash'))

            
            o_pass = request.form.get("old_pass")
            n_pass = request.form.get("new_pass")
            c_pass = request.form.get("conf_pass")
            
            new_dname = request.form.get("disname")

            # Changing password

            if o_pass:

                
                if not check_password_hash(user.password, o_pass):
                    flash("Current Password is incorrect!", 'danger')
                    return redirect(url_for('auth.sett'))
                
                if n_pass != c_pass:
                    flash("New Password does not match!", 'danger')
                    return redirect(url_for('auth.sett'))
                
                new_hashed_pw = generate_password_hash(n_pass)
                user.password = new_hashed_pw
                db.session.commit()
                flash("Password Changed Sccessfully!", 'success')
                return redirect(url_for('auth.dash'))
            
            # Changing display name

            if new_dname:
                user.displayname = new_dname
                db.session.commit()
                flash("Display name changed!", 'success')
                return redirect(url_for('auth.dash'))
        
        return render_template("setting.html", displayn=displayn, form=form)
    else:
        return "<h1>You need to login to access settings!"

@auth_bp.route("/delete", methods = ["POST"])
def delete():
    user_id = session.get("user_id")
    user = Users.query.get(user_id)
    
    if user:
        session.pop("user_id")
        db.session.delete(user)
        db.session.commit()
        
        flash("Your account has been successfully deleted", 'success')
        return redirect(url_for('home'))
    