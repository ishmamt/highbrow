from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class NewPostForm(FlaskForm):
    # for posting new blog
    title = StringField("Title", validators=[DataRequired()])
    topic = StringField("Choose topic", validators=[DataRequired()])
    content = TextAreaField("Share your experience...", validators=[DataRequired()])
    picture = FileField('Upload a picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Post')
