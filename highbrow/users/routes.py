from flask import render_template, url_for, redirect, request, Blueprint, flash
from highbrow.users.forms import SigninForm, SignupForm
from flask_login import login_user, logout_user, current_user
from highbrow import load_user, bcrypt
from highbrow.users.utils import find_user, fetch_own_posts, create_new_user, if_is_following, follow_unfollow_user
from highbrow.utils import fetch_notifications, fetch_followed_topics

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)


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


@users.route("/user/<string:username>")
def user(username):
    user_details = find_user(username)
    notifications = fetch_notifications(current_user.username)
    own_posts = fetch_own_posts(username, current_user.username)
    interests = fetch_followed_topics(username)
    is_following = if_is_following(current_user.username, username)
    return render_template("user.html", user_details=user_details, posts=own_posts, interests=interests, contacts=contacts,
                           jobs=jobs, notifications=notifications, current_user=current_user.username, is_following=is_following)


@users.route("/follow/<string:notified_user>/<string:notifying_user>/<string:is_following>")
def follow_user(notifying_user, notified_user, is_following):
    follow_unfollow_user(notifying_user, notified_user, is_following)
    return redirect(url_for("users.user", username=notified_user))


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
            if user and bcrypt.check_password_hash(user.password, signin_form.signin_password.data):
                login_user(user, remember=signin_form.c1.data)
                return redirect(url_for("main.home"))
            else:
                flash("Login unsuccessful. Please check username or password.", "danger")
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
            hashed_password = bcrypt.generate_password_hash(signup_form.signup_password.data).decode('utf-8')  # decode needed to get string hash
            status = create_new_user(signup_form.signup_fullname.data, signup_form.signup_username.data,
                                     signup_form.signup_email.data, hashed_password)
            if status:
                user = load_user(signup_form.signup_username.data)
                login_user(user, remember=False)
                return redirect(url_for("main.home"))
            else:
                return redirect(url_for("users.signup"))
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
