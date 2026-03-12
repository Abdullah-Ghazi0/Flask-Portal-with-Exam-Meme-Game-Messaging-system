import os
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
        return render_template("admin/admin.html", user=user)

    return render_template("user/profile.html", user=user)
    
    

@user_bp.route("/settings", methods=["GET","POST"])
def setting():
    if "user_id" not in session:
        flash("Please Login to access your profile!", 'danger')
        return redirect(url_for('auth.login'))

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

            return redirect(url_for('user.profile'))

            
        o_pass = request.form.get("old_pass")
        n_pass = request.form.get("new_pass")
        c_pass = request.form.get("conf_pass")
            
        new_dname = request.form.get("disname")

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
            user.displayname = new_dname
            db.session.commit()
            flash("Display name changed!", 'success')
            return redirect(url_for('user.profile'))
        
    return render_template("user/setting.html", displayn=displayn, form=form)


@user_bp.route("/delete", methods = ["POST"])
def delete():
    user_id = session.get("user_id")
    user = Users.query.get(user_id)
    
    if user:
        session.pop("user_id")
        db.session.delete(user)
        db.session.commit()
        
        flash("Your account has been successfully deleted", 'success')
        return redirect(url_for('home'))