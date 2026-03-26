import os
import secrets
from datetime import datetime, timezone
from flask import render_template, session, request, redirect, url_for, current_app, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from . import user_bp
from ..models import db, Users
from .forms import ProfilePicForm


@user_bp.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please Login to access your profile!", 'danger')
        return redirect(url_for('auth.login'))
    
    usrid = session.get("user_id")
    user = Users.query.get(usrid)

    if user.username == "admin":
        return redirect(url_for('admin.panel'))

    return redirect(url_for('social.view_profile', username=user.username))
    
    

@user_bp.route("/settings", methods=["GET","POST"])
def setting():
    if "user_id" not in session:
        flash("Please Login to access your profile!", 'danger')
        return redirect(url_for('auth.login'))

    user_id = session.get("user_id")

    user = Users.query.get(user_id)

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

            user.profile.picture = file_name
            db.session.commit()

            session["profile_picture"] = file_name

            return redirect(url_for('user.profile'))

            
        o_pass = request.form.get("old_pass")
        n_pass = request.form.get("new_pass")
        c_pass = request.form.get("conf_pass")
            
        new_dname = request.form.get("disname")

        bio = request.form.get("bioData")

        link = request.form.get("link")

        # Changing password

        if o_pass:

                
            if not check_password_hash(user.password, o_pass):
                flash("Current Password is incorrect!", 'danger')
                return redirect(url_for('user.setting'))
                
            if n_pass != c_pass:
                flash("New Password does not match!", 'danger')
                return redirect(url_for('user.setting'))
                
            new_hashed_pw = generate_password_hash(n_pass)
            user.password = new_hashed_pw
            db.session.commit()
            flash("Password Changed Sccessfully!", 'success')
            return redirect(url_for('user.profile'))
            
        # Changing display name

        if new_dname:
            user.profile.displayname = new_dname
            db.session.commit()
            flash("Display name changed!", 'success')
            return redirect(url_for('user.profile'))
        
        if bio:
            user.profile.bio = bio
            db.session.commit()
            flash("Bio changed!", 'success')
            return redirect(url_for('user.profile'))
        
        if link:
            user.profile.link = link
            db.session.commit()
            flash("Link changed!", 'success')
            return redirect(url_for('user.profile'))
        
    return render_template("user/setting.html", form=form, user=user)


@user_bp.route("/delete", methods = ["POST"])
def delete():
    user_id = session.get("user_id")
    user = Users.query.get(user_id)

    password = request.form.get("confirm_pass")
    
    if user and check_password_hash(user.password, password):
        user.username = f"deleted_user_{user.id}"
        user.email = None
        user.password = secrets.token_urlsafe(32)
        user.status = "deleted"
        user.status_changed_at = datetime.now(timezone.utc)
        user.profile.bio = None
        user.profile.link = None
        user.profile.verified = False
        user.profile.displayname = "Deleted User"

        old_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], user.profile.picture)
        if os.path.exists(old_filepath) and user.profile.picture != "default.png":
            os.remove(old_filepath)

        user.profile.picture = "default.png"

        session.clear()
        db.session.commit()
        
        flash("Your account has been successfully deleted!", 'success')
        return redirect(url_for('home'))
    
    flash("Password is incorrect!", 'danger')
    return redirect(url_for('user.setting'))