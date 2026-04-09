from flask import render_template, request, redirect, url_for, session, flash
from sqlalchemy.orm import joinedload
from ..models import db, Users, Follows
from . import social_bp

@social_bp.route("/u/<username>")
def view_profile(username):

    user = Users.query.filter_by(username=username).first()
    if user:

        followORnot = Follows.query.filter_by(follower_id=session.get('user_id'), followed_id=user.id).first() is not None
        followers = Follows.query.filter_by(followed_id=user.id).count()
        following = Follows.query.filter_by(follower_id=user.id).count()

        user.followStatus = followORnot
        user.followers = followers
        user.following = following

        return render_template("social/profile.html", user=user)
    
    return render_template("page_not_found.html")


@social_bp.route("/follow", methods=["POST"])
def follow():
    my_id =  session.get('user_id')

    if not my_id:
        flash("Please login to Follow this user!", 'danger')
        return redirect(url_for('auth.login'))

    followed = request.form.get('followed_id')


    if followed == my_id:
        flash("You cannot Follow yourself!", 'danger')
        return redirect(request.referrer)
    
    if Follows.query.filter_by(follower_id = my_id, followed_id = followed).first():
        flash("You already follow this user!", 'danger')
        return redirect(request.referrer)

    new_follow = Follows(
        follower_id = my_id,
        followed_id = followed
    )

    db.session.add(new_follow)
    db.session.commit()

    return redirect(request.referrer)


@social_bp.route("/un-follow", methods=["POST"])
def unFollow():
    followed = request.form.get('followed_id')
    my_id =  session.get('user_id')

    follow = Follows.query.filter_by(follower_id = my_id, followed_id = followed).first()

    if follow:
        db.session.delete(follow)
        db.session.commit()

    return redirect(request.referrer)


@social_bp.route("/u/<username>/<follow>")
def view_profile_follows(username, follow):
    if "user_id" not in session:
        flash("You need to login first!", 'danger')
        return redirect(url_for("auth.login"))
    
    user = Users.query.filter_by(username=username).first()
    if not user:
        return render_template("page_not_found.html")
    
    followORnot = Follows.query.filter_by(follower_id=session.get('user_id'), followed_id=user.id).first() is not None
    followers = Follows.query.filter_by(followed_id=user.id).count()
    following = Follows.query.filter_by(follower_id=user.id).count()

    user.followStatus = followORnot
    user.followers = followers
    user.following = following
    user.followInfo = follow.capitalize()
    
    if follow == 'following':
        followList = Follows.query.options(joinedload(Follows.followed)).filter_by(follower_id=user.id).all()

    elif follow == 'followers':
        followList  = Follows.query.options(joinedload(Follows.follower)).filter_by(followed_id=user.id).all()
    
    elif follow:
        return render_template("page_not_found.html")

    return render_template("social/profile.html", user=user, followList=followList)