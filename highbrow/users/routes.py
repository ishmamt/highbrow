from flask import render_template, url_for, redirect, request, Blueprint

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)


@users.route("/user")
def user():
    return render_template("user.html")


@users.route("/sign-in")
@users.route("/login")
@users.route("/register")
@users.route("/sign-up")
@users.route("/join")
def signin():
    return render_template("signin.html")
