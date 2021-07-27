from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
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
