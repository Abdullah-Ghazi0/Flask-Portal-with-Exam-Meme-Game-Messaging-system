from flask import render_template, session, redirect, url_for, request, flash, jsonify
from ..models import db, Questions, Results, Users
from .simple_api import convertor
from sqlalchemy.sql import func
from . import exam_bp

@exam_bp.route("/create-exam", methods = ["GET","POST"])
def create():
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
            return redirect(url_for("exam.create"))

        return render_template("admin/create_exam.html")

    flash("You are not allowed to access this page!", 'danger')
    return redirect(url_for('home'))


@exam_bp.route("/")
def exam():
    if "user_id" not in session:
        flash("Please login first!", 'danger')
        return redirect(url_for('auth.login'))
    
    questions = Questions.query.order_by(func.random()).limit(10).all()
    return render_template("exam/exam.html", questions=questions)
    

@exam_bp.route("/result", methods = ["GET", "POST"])
def result():
    if "user_id" not in session:
        flash("Please login first!", 'danger')
        return redirect(url_for('auth.login'))
    
    id = session.get("user_id")

    if request.method == "POST":
            
        score = 0
            
        for key, value in request.form.items():
            q_id = int(key)
            u_ans = True if  value == "True" else False
            
            question = Questions.query.get(q_id)
            if question and question.answer == u_ans:
                score += 1

        result = Results.query.filter_by(user_id=id).first()
        if result:
            result.score = score
        else:
            new_result = Results(user_id=id, score=score)
            db.session.add(new_result)

        db.session.commit()

    result = Results.query.filter_by(user_id=id).first()

    return render_template("exam/result.html", result=result)
    
@exam_bp.route("/api")
def data():
    return jsonify(convertor())