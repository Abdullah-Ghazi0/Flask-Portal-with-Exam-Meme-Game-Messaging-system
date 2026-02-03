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

    convos = set()

    for msg in all_msg:
        if msg.s_id != my_id:
            convos.add(msg.s_id)
        if msg.r_id != my_id:
            convos.add(msg.r_id)

    msged_users = Users.query.filter(Users.id.in_(convos)).all()

    if all_msg:    
        return render_template("inbox.html", id=my_id, msged_users=msged_users)
    else:
        flash("No Messages yet!")
        return render_template("inbox.html")
    

@msg_bp.route("/inbox/chat/<int:others_id>")
def chats(others_id):
    if "user_id" not in session:
        flash("You need to login first!")
        return redirect(url_for("auth.login"))
    
    my_id = session["user_id"]

    others_info = Users.query.get(others_id)
    others_name = others_info.username


    our_msgs = Messages.query.filter(or_((Messages.r_id==others_id) & (Messages.s_id==my_id),
                                          (Messages.s_id==others_id) & (Messages.r_id==my_id))
                                          ).order_by(Messages.time.asc()).all()
    
    all_msg = Messages.query.filter(or_(Messages.r_id==my_id, Messages.s_id==my_id)).order_by(Messages.time).all()
    
    convos = set()

    for msg in all_msg:
        if msg.s_id != my_id:
            convos.add(msg.s_id)
        if msg.r_id != my_id:
            convos.add(msg.r_id)

    msged_users = Users.query.filter(Users.id.in_(convos)).all()
    
    return render_template("inbox.html", all_msg=our_msgs, id=my_id, msged_users=msged_users, others_name=others_name)