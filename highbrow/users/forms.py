from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from highbrow.users.utils import check_user, check_email


class SigninForm(FlaskForm):
    # for logging in
    signin_username = StringField("Username", validators=[DataRequired()])
    signin_password = PasswordField("Password", validators=[DataRequired()])
    c1 = BooleanField("Remember Me")
    submit = SubmitField('Login')


class SignupForm(FlaskForm):
    # for signing up
    signup_fullname = StringField("Fullname", validators=[DataRequired()])
    signup_username = StringField("Username", validators=[DataRequired()])
    signup_email = StringField("Email", validators=[DataRequired(), Email()])
    signup_password = PasswordField("Password", validators=[DataRequired()])
    signup_repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("signup_password", message='Passwords must match')])
    c2 = BooleanField("Yes, I understand and agree to the workwise Terms & Conditions.")
    submit = SubmitField('Signup')

    def validate_c2(self, c2):
        if c2.data is False:
            raise ValidationError("You must agree to the terms and conditions.")

    def validate_signup_username(self, username):
        # custom validation check to see if username already exists
        user = check_user(username.data)  # if user doesn't exist, returns none
        if user:
            raise ValidationError("Username already in use.")

    def validate_signup_email(self, email):
        # custom validation check to see if email already exists
        email = check_email(email.data)  # if email doesn't exist, returns none
        if email:
            raise ValidationError("Email already in use.")


class User_settings_short_bio_form(FlaskForm):
    # for editing user info
    short_bio = TextAreaField("Something about yourself...", validators=[DataRequired()])
    submit = SubmitField('Update Bio')


class User_settings_experience_form(FlaskForm):
    # for editing and adding experience
    designation = StringField("Enter designation", validators=[DataRequired()])
    institution = StringField("Enter institution", validators=[DataRequired()])
    submit = SubmitField('Add experience')


class User_settings_contact_form(FlaskForm):
    # for editing and adding contacts
    title = StringField("Enter contact name", validators=[DataRequired()])
    contact_link = StringField("Enter contact link", validators=[DataRequired()])
    submit = SubmitField('Add contact')


class User_settings_profile_picture_form(FlaskForm):
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'])])
    submit = SubmitField('Update')
