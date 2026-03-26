from flask import render_template, request, redirect, url_for, session, flash
from . import support_bp
from ..models import db, Reports, Feedbacks

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
    flash("Thanks for your Feedback. We will try work on this soon!", 'success')
    return redirect(request.referrer)


# @support_bp.route("/feedback/request-new-feature", methods=["POST"])
# def newFeature():
#     featTitle = request.form.get("featureName")
#     featDesc = request.form.get("featureDescription")

#     if not (featTitle and featDesc):
#         flash("Please Enter Title and Description!", 'danger')
#         return redirect(request.referrer)
    
#     new_fb = Feedbacks(
#         catagory = "new feature request",
#         sender_id = session.get("user_id"),
#         title = featTitle,
#         description = featDesc
#     )

#     db.session.add(new_fb)
#     db.session.commit()
#     flash("Thanks for your Feedback. We will try to add this feature soon!", 'success')
#     return redirect(request.referrer)