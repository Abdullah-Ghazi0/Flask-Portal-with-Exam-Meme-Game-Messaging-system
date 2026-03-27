from flask import render_template, request, redirect, url_for, session, flash
from . import support_bp
from ..models import db, Reports, Feedbacks, Users

@support_bp.route("/feedback", methods=["POST"])
def feedback():
    bugTitle = request.form.get("bugName")
    bugDesc = request.form.get("bugDescription")

    featTitle = request.form.get("featureName")
    featDesc = request.form.get("featureDescription")

    if not ((bugTitle and bugDesc) or (featTitle and featDesc)):
        flash("Please Enter Title and Description!", 'danger')
        return redirect(request.referrer)

    new_fb = Feedbacks(
        catagory = "bug report" if bugTitle else "new feature request",
        sender_id = session.get("user_id"),
        title = bugTitle or featTitle,
        description = bugDesc or featDesc
    )

    db.session.add(new_fb)
    db.session.commit()
    flash("Thanks for your feedback. We're always working to improve your experience.", 'success')
    return redirect(request.referrer)

@support_bp.route("/report", methods=["POST"])
def report():
    catagory = request.form.get("catagory")
    uname = request.form.get("userName")
    desc = request.form.get("reportDescription")

    target_user = Users.query.filter_by(username=uname).first()
    if not target_user:
        flash("The User you are trying to report doesn't exist!", 'danger')
        return redirect(request.referrer)
    
    if target_user.id == session.get("user_id"):
        flash("You cannot report yourself.", 'danger')
        return redirect(request.referrer)
    
    if not catagory:
        flash("Please Select a category to report!", 'danger')
        return redirect(request.referrer)
    
    if catagory == 'other' and not desc.strip():
        flash("Please provide a description when selecting 'Other' as the category.", 'danger')
        return redirect(request.referrer)
    
    if Reports.query.filter_by(catagory=catagory,
                               reporter_id=session.get("user_id"),
                               target_type='user',
                               target_id=target_user.id
                               ).first():

        flash("We appreciate you bringing this to our attention", 'success')
        return redirect(request.referrer)
    
    new_report = Reports(
        catagory=catagory,
        reporter_id=session.get("user_id"),
        target_type='user',
        target_id=target_user.id,
        description= desc if desc else None
    )

    db.session.add(new_report)
    db.session.commit()
    flash("We appreciate you bringing this to our attention", 'success')
    return redirect(request.referrer)