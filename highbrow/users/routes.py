from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.users.forms import SigninForm, SignupForm
from flask_login import login_user, logout_user, current_user
from highbrow import load_user
from highbrow.users.utils import find_user, fetch_own_posts
from highbrow.utils import fetch_notifications

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)

interests = [
    {
        "name": "CNN",
        "link": "/topic"
    },
    {
        "name": "RNN",
        "link": "/topic"
    },
    {
        "name": "ML",
        "link": "/topic"
    },
    {
        "name": "DEEP LEARNING",
        "link": "/topic"
    },
    {
        "name": "MACHINE LEARNING",
        "link": "/topic"
    },
    {
        "name": "LSTM",
        "link": "/topic"
    },
    {
        "name": "AI",
        "link": "/topic"
    },

]

contacts = [
    {
        "website_name": "Twitter",
        "link": "https://twitter.com"
    },
    {
        "website_name": "Facebook",
        "link": "https://facebook.com"
    },
    {
        "website_name": "Email",
        "link": "https://gmail.com"
    }
]

jobs = [
    {
        "name": "Senior Product Designer",
        "details": "cwybciwbviuv"
    },
    {
        "name": "Senior UI / UX Designer",
        "details": "vcwuvybwiucvnwiucn"
    },
    {
        "name": "Senior PHP Designer",
        "details": "cwbugbwihcbwib"
    }
]


@users.route("/<string:username>")
def user(username):
    user_details = find_user(username)
    notifications = fetch_notifications(username)
    own_posts = fetch_own_posts(username)
    return render_template("user.html", user_details=user_details, posts=own_posts, interests=interests, contacts=contacts,
                           jobs=jobs, notifications=notifications, current_user=current_user.username)


@users.route("/sign-in", methods=["GET", "POST"])
@users.route("/login", methods=["GET", "POST"])
def signin():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("main.home"))
    signin_form = SigninForm()
    if request.method == "POST":
        if signin_form.validate_on_submit():
            user = load_user(signin_form.signin_username.data)
            if user and user.password == signin_form.signin_password.data:
                login_user(user, remember=signin_form.c1.data)
                return redirect(url_for("main.home"))
    return render_template("signin.html", signin_form=signin_form)


@users.route("/register", methods=["GET", "POST"])
@users.route("/sign-up", methods=["GET", "POST"])
@users.route("/join", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        # if user is already logged in
        return redirect(url_for("main.home"))
    signup_form = SignupForm()
    if request.method == "POST":
        if signup_form.validate_on_submit():
            return redirect(url_for("main.home"))
    return render_template("signup.html", signup_form=signup_form)


@users.route("/contact")
def contact():
    return render_template("contact.html")


@users.route("/about")
def about():
    return render_template("about.html")


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("users.signin"))
