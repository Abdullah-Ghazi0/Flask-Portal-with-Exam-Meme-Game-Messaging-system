from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from ..models import db, Questions, Results
from .simple_api import convertor
from sqlalchemy.sql import func


exam_bp = Blueprint("exam", __name__, url_prefix="/exam")

@exam_bp.route("/create-exam", methods = ["GET","POST"])
def create():
    if "user_id" in session and session["user_id"] == 1:

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

        return render_template("create.html")
    else:
        return "<h1>You are not allowed access this page!"

@exam_bp.route("/")
def exam():
    if "user_id" in session:
        questions = Questions.query.order_by(func.random()).limit(10).all()
        return render_template("exam.html", questions=questions)
    else:
        return "<h1>Please Login First!"

@exam_bp.route("/result", methods = ["GET", "POST"])
def result():
    if "user_id" in session:
        id = session.get("user_id")
        msg = None
        if request.method == "POST":
            
            score = 0
            
            for key, value in request.form.items():
                q_id = int(key)
                u_ans = True if  value == "True" else False
            
                question = Questions.query.get(q_id)
                if question and question.answer == u_ans:
                    score += 1
            if Results.query.filter_by(user_id=id).first():
                result_info = Results.query.filter_by(user_id=id).first()
                result_info.score = score
            else:
                new_result = Results(user_id=id, score=score)
                db.session.add(new_result)

            db.session.commit()

        if Results.query.filter_by(user_id=id).first():
            info = Results.query.filter_by(user_id=id).first()
            marks = info.score
            if marks >= 7:
                msg= "Congratulation You have passed, Marks:"
                return render_template("result.html", score=marks, msg= msg)
            else:
                msg= "You have failed, Marks:"
                return render_template("result.html", score=marks, msg= msg)
        else:
            msg = "Please Take Test to view your result" 
            return render_template("result.html", msg= msg)
    else:
        return "<h1> You Don't have access to this page"
    
@exam_bp.route("/api")
def data():
    return jsonify(convertor())