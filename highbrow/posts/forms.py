from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    # for commenting on a post
    comment = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")
