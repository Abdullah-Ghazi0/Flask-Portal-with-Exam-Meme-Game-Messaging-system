from flask import Flask, render_template, request, session, redirect, flash, url_for
from models import db, Users, Questions, Results
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import func

app = Flask(__name__)

app.secret_key = "supersecretkey"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET","POST"])
def reg():
    
    if request.method == "POST":
        uname = request.form.get("username")
        pword = request.form.get("password")

        hashed_pw = generate_password_hash(pword)

        if Users.query.filter_by(username=uname).first():
            flash("User already Exist!")
        else:
            user = Users(
                username = uname,
                password = hashed_pw
            )
            db.session.add(user)
            db.session.commit()
            flash("Registered Sccessfully!")
            return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=["GET","POST"])
def login():
    
    if request.method == "POST":
        log_uname = request.form.get("username")
        log_pword = request.form.get("password")

        user = Users.query.filter_by(username=log_uname).first()
        if user and check_password_hash(user.password, log_pword):
            session["user_id"] = user.id
            flash("Login Sccessful!")
            return redirect(url_for('dash'))

        else:
            flash("Wrong Username or Password!")

    return render_template("login.html")

@app.route("/dashboard")
def dash():
    if "user_id" in session:
        usrid = session.get("user_id")
        user = Users.query.get(usrid)
        name = user.username
        if name == "admin":
            return render_template("admin.html", name=name)

        return render_template("dashboard.html", name=name)
    else:
        return "<h1>You need to login to access dashboard!"
    
@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id")
    return redirect(url_for('home'))

@app.route("/settings", methods=["GET","POST"])
def sett():
    if "user_id" in session:
        user_id = session.get("user_id")

        if request.method == "POST":
            o_pass = request.form.get("old_pass")
            n_pass = request.form.get("new_pass")
            c_pass = request.form.get("conf_pass")

            user_info = Users.query.get(user_id)
            if not check_password_hash(user_info.password, o_pass):
                flash("Current Password is incorrect!")
                return redirect(url_for('sett'))
            
            if n_pass != c_pass:
                flash("New Password does not match!")
                return redirect(url_for('sett'))
            
            new_hashed_pw = generate_password_hash(n_pass)
            user_info.password = new_hashed_pw
            db.session.commit()
            flash("Password Changed Sccessfully!")
            return redirect(url_for('dash'))
        
        return render_template("setting.html")
    else:
        return "<h1>You need to login to access settings!"

@app.route("/delete", methods = ["POST"])
def delete():
    user_id = session.get("user_id")
    user = Users.query.get(user_id)
    
    if user:
        session.pop("user_id")
        db.session.delete(user)
        db.session.commit()
        
        flash("Your account has been successfully deleted.")
        return redirect(url_for('home'))
    
@app.route("/create-exam", methods = ["GET","POST"])
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
            flash("Question Added Sccessfully!")
            return redirect(url_for("create"))

        return render_template("create.html")
    else:
        return "<h1>You are not allowed access this page!"

@app.route("/exam")
def exam():
    if "user_id" in session:
        questions = Questions.query.order_by(func.random()).limit(10).all()
        return render_template("exam.html", questions=questions)
    else:
        return "<h1>Please Login First!"

@app.route("/result", methods = ["GET", "POST"])
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


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug = True)