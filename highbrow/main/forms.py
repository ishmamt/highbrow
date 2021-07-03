from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class NewPostForm(FlaskForm):
    # for posting new blog
    title = StringField("Title", validators=[DataRequired()])
    topic = StringField("Choose topic", validators=[DataRequired()])
    content = TextAreaField("Share your experience...", validators=[DataRequired()])
    submit = SubmitField('Post')
