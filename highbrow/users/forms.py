from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


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
    signup_password = PasswordField("Password", validators=[DataRequired(), EqualTo("signup_repeat_password")])
    signup_repeat_password = PasswordField("Repeat Password")
    c2 = BooleanField("Yes, I understand and agree to the workwise Terms & Conditions.", validators=[DataRequired()])
    submit = SubmitField('Signup')

    def validate_terms_and_conditions(self, c2):
        if c2.data == False:
            raise ValidationError("You must agree to the terms and conditions.")
