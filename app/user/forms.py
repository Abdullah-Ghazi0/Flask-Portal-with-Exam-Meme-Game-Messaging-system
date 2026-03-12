from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileAllowed, FileRequired

class ProfilePicForm(FlaskForm):
    picture = FileField("Upload Profile Picture",
                        validators=[FileRequired(), FileAllowed(['png', 'jpeg', 'jpg'], "Images Only!")])
    submit = SubmitField("Update")