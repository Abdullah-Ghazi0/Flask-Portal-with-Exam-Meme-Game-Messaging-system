import os
from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, session, current_app
from sqlalchemy.orm import joinedload
from ..models import db, Questions, Users, Words, Feedbacks, Reports
from .utils import find_known_char, banUser, priority
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

    # optional autofill username
    banFromReport = request.args.get('usertoban')
    report_id = request.args.get('report_id')

    if user.username == "admin":
        if request.method == "POST":

            username = request.form.get("userToBan") if request.form.get("userToBan") else request.form.get("userToVerify")
            verification = request.form.get("verification") == "True"

            userToActOn = Users.query.filter_by(username=username).first()

            if userToActOn:
                if request.form.get("userToBan"):
                    report_id = request.form.get("report")
                    if report_id:
                        report = Reports.query.get(report_id)
                        report.status = 'resolved'
                        db.session.commit()

                    banUser(userToActOn)
                else:
                    userToActOn.profile.verified = verification
                    db.session.commit()

                    flash("Action Completed!", 'success')
                    return redirect(url_for('admin.manage_user'))
                
            else:
                flash("User Not Found!", 'danger')
                return redirect(url_for('admin.manage_user'))

        return render_template("admin/manage_user.html", banThisUser=[banFromReport, report_id])
    
    flash("You are not allowed access this page!", 'danger')
    return redirect(url_for('home'))


@admin_bp.route("/support/<tab>", methods=['GET', 'POST'])
def user_support(tab):
    if "user_id" not in session:
        flash("You need to login first!", 'danger')
        return redirect(url_for("auth.login"))
    
    user = Users.query.get(session.get("user_id"))
    if user.username == "admin":

        page = request.args.get("page" ,1 , type=int)

        query = Reports.query

        if tab not in ['report', 'feedback']:
            return render_template('page_not_found.html')
        
        if tab == 'feedback':
            list_of_items = Feedbacks.query.join(Users, Feedbacks.sender_id == Users.id).add_entity(Users).paginate(page=page, per_page=10)

        if tab == 'report':
            if request.args.get('filter') == 'all':
                query = query.options(joinedload(Reports.reporter)
                                ).join(Users, Reports.target_id == Users.id).filter(Reports.target_type == 'user'
                                ).execution_options(include_deleted=True)
            else:
                query = query.options(joinedload(Reports.reporter)
                                ).join(Users, Reports.target_id == Users.id).filter(Reports.target_type == 'user', Reports.status == 'pending'
                                )

            if request.args.get('sort') == 'time':
                list_of_items = query.add_entity(Users).paginate(page=page, per_page=10)

            else:
                list_of_items = query.order_by(priority, Reports.created_at.desc()).add_entity(Users).paginate(page=page, per_page=10)

        args = request.args.to_dict()
        args.pop('page') if args.get('page') else None
        args['tab'] = tab
        return render_template("admin/support.html", list_of_items=list_of_items, args=args)
    
    flash("You are not allowed access this page!", 'danger')
    return redirect(url_for('home'))


@admin_bp.route("report/dismiss", methods=["POST"])
def dismissReport():
    report_id = request.form.get("report_id")

    args = request.args.to_dict()

    report = Reports.query.get(report_id)
    report.status = 'dismissed'
    
    db.session.commit()
    return redirect(url_for('admin.user_support', **args))

