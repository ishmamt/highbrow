from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class PostForm(FlaskForm):
    # for commenting on a post
    comment = TextAreaField("Comment")
    submit = SubmitField("Post Comment")
