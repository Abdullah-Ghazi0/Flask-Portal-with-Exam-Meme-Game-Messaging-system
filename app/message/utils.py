from flask import session
from ..models import db, Messages, Users
from sqlalchemy import or_


def send(r, m):
    recievingUser = Users.query.filter_by(username=r).first()
    new_msg = Messages(
        s_id = session["user_id"],
        r_id = recievingUser.id,
        content = m
    )
    db.session.add(new_msg)
    db.session.commit()


def all_chats():
    my_id = session["user_id"]
    all_msg = Messages.query.filter(or_(Messages.r_id==my_id, Messages.s_id==my_id)).order_by(Messages.time).all()
    if all_msg:
        convos = set()

        for msg in all_msg:
            if msg.s_id != my_id:
                convos.add(msg.s_id)
            if msg.r_id != my_id:
                convos.add(msg.r_id)

        chats_list = {}
        msged_users = Users.query.filter(Users.id.in_(convos)).all()

        for user in msged_users:
            last_msgs = Messages.query.filter(or_((Messages.r_id==my_id) & (Messages.s_id==user.id),
                                                  (Messages.s_id==my_id) & (Messages.r_id==user.id))
                                                  ).order_by(Messages.time.desc()).first()
            
            chats_list[user.username] = {"id": user.id, "msg": last_msgs.content, "time": last_msgs.time, "name": user.displayname, "pic": user.picture}
            sorted_chats = dict(sorted(chats_list.items(), key=lambda x: x[1]['time'], reverse=True))

        return sorted_chats
    else:
        return None
    
def search_filter(search, chats):

    for chat in chats:
        if chats[chat]["name"].lower().startswith(search.lower()):
            chats[chat]["score"] = 4

        elif chat.lower().startswith(search.lower()):
            chats[chat]["score"] = 3
        
        elif search.lower() in chats[chat]["name"]:
            chats[chat]["score"] = 2
        
        elif search.lower() in chat:
            chats[chat]["score"] = 1
        
        else:
            chats[chat]["score"] = 0

    for chat in list(chats):
        if chats[chat]["score"] == 0:
            chats.pop(chat)
    
    searched_chats = dict(sorted(chats.items(), key=lambda x: x[1]['score'], reverse=True))
    print(searched_chats)

    return searched_chats