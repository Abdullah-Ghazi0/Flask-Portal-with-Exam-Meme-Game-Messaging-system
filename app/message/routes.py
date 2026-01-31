from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from .sending import send
from ..models import Users, Messages
from sqlalchemy import or_

msg_bp = Blueprint("message", __name__, url_prefix="/message")

@msg_bp.route("/send", methods=["POST", "GET"])
def msg_send():
    if "user_id" not in session:
        flash("You need to login first!")
        return redirect(url_for("auth.login"))
    
    users_list = Users.query.filter(Users.id != session["user_id"], Users.username!="admin").all()
    unames = [user.username for user in users_list ]
    print(unames)

    if request.method == "POST":
        rcvr = request.form.get("reciever")

        if Users.query.filter_by(username=rcvr).first():

            msg = request.form.get("msg_content")
            send(rcvr, msg)
            flash("Message Sent!")
        else:
            flash("Please Send message to a valid user!")
            return redirect(url_for("message.msg_send"))

    return render_template("message.html", allUsers=unames)

@msg_bp.route("/inbox")
def inbox():
    if "user_id" not in session:
        flash("You need to login first!")
        return redirect(url_for("auth.login"))
    my_id = session["user_id"]
    
    all_msg = Messages.query.filter(or_(Messages.r_id==my_id, Messages.s_id==my_id)).order_by(Messages.time).all()
    if all_msg:    
        return render_template("inbox.html", all_msg=all_msg, id=my_id)
    else:
        flash("No Messages yet!")
        return render_template("inbox.html")