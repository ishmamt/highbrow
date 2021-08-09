from flask import render_template, url_for, redirect, request, Blueprint, flash
from highbrow.users.forms import SigninForm, SignupForm, User_settings_short_bio_form, User_settings_experience_form, User_settings_contact_form, User_settings_profile_picture_form
from flask_login import login_user, logout_user, current_user
from highbrow import load_user, bcrypt
from highbrow.users.utils import find_user, fetch_own_posts, create_new_user, if_is_following, follow_unfollow_user, fetch_saved_posts
from highbrow.utils import fetch_notifications, fetch_followed_topics, add_remove_to_saved

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)


contacts = [
    {
        "name": "Twitter",
        "link": "https://twitter.com"
    },
    {
        "name": "Facebook",
        "link": "https://facebook.com"
    },
    {
        "name": "Email",
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


@users.route("/user/<string:username>/saved_posts")
def saved_posts(username):
    user_details = find_user(username)
    notifications = fetch_notifications(current_user.username)
    if username == current_user.username:
        user_saved_posts = fetch_saved_posts(current_user.username)
    else:
        return redirect(url_for("users.user", username=current_user.username))
    interests = fetch_followed_topics(username)
    is_following = if_is_following(current_user.username, username)
    return render_template("user.html", user_details=user_details, posts=user_saved_posts, interests=interests, contacts=contacts,
                           jobs=jobs, notifications=notifications, current_user=current_user.username, is_following=is_following)


@users.route("/post/save/<string:username>/<string:post_id>/<string:is_saved>")
def add_post_to_saved(username, post_id, is_saved):
    add_remove_to_saved(username, post_id, is_saved)
    return redirect(url_for("posts.post", post_id=post_id))


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


@users.route("/<string:username>/profile_setting")
def user_settings(username):
    bio_form = User_settings_short_bio_form()
    experience_form = User_settings_experience_form()
    contact_form = User_settings_contact_form()
    profile_pic_form = User_settings_profile_picture_form()
    if username == current_user.username:
        if bio_form.validate_on_submit():
            pass
        if experience_form.validate_on_submit():
            pass
        if contact_form.validate_on_submit():
            pass
        if profile_pic_form.validate_on_submit():
            pass
        return render_template("profile_settings.html", bio_form=bio_form, experience_form=experience_form,
                               contact_form=contact_form, profile_pic_form=profile_pic_form, jobs=jobs, contacts=contacts)
    return redirect(url_for("users.user", username=current_user.username))


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
