from flask import render_template, request, Blueprint, redirect, url_for
from highbrow.main.forms import NewPostForm
from highbrow.main.utils import create_new_post, fetch_index_posts, list_to_string_tags, update_post
from highbrow.posts.utils import fetch_post
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


@main.route("/edit_post/<string:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    form = NewPostForm()
    notifications = fetch_notifications(current_user.username)
    post = fetch_post(post_id)
    if form.validate_on_submit():
        # update
        update_post(post["username"], form.title.data, form.content.data, create_tags(form.topic.data.split(', ')), post["link"])
        return redirect(url_for("posts.post", post_id=post_id))
    elif request.method == "GET":
        form.title.data = post["title"]
        form.topic.data = list_to_string_tags(post["tags"])
        form.content.data = post["content"]
    return render_template("edit_post.html", form=form, notifications=notifications, current_user=current_user.username)
