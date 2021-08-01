from flask import render_template, request, Blueprint, redirect, url_for
from highbrow.main.forms import NewPostForm
from highbrow.main.utils import create_new_post, fetch_index_posts
from highbrow.utils import fetch_notifications, fetch_followed_topics
from flask_login import current_user, login_required

main = Blueprint('main', __name__)  # similar to app = Flask(__name__)


def create_tags(tags):
    post_tags = list()
    for tag in tags:
        tag = tag.upper()
        post_tags.append(tag)
    return post_tags


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
@main.route("/index", methods=["GET", "POST"])
@login_required
def home():
    posts = fetch_index_posts(current_user.username)
    notifications = fetch_notifications(current_user.username)
    interests = fetch_followed_topics(current_user.username)
    form = NewPostForm()
    if form.validate_on_submit() and request.method == "POST":
        create_new_post(current_user.username, form.title.data, form.content.data, create_tags(form.topic.data.split(', ')))
        return redirect(url_for("main.home"))
    return render_template("home.html", posts=posts, form=form, interests=interests, notifications=notifications,
                           current_user=current_user.username)
