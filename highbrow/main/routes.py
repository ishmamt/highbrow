from flask import render_template, request, Blueprint, redirect, url_for, flash
from highbrow.main.forms import NewPostForm
from highbrow.main.utils import create_new_post, fetch_index_posts, list_to_string_tags, update_post, delete_post, check_topic_validity, save_post_picture, update_post_picture
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
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    form = NewPostForm()
    if form.validate_on_submit() and request.method == "POST":
        if check_topic_validity(form.topic.data):
            post_id = create_new_post(current_user.username, form.title.data, form.content.data, create_tags(form.topic.data.split(',')))
            if form.picture.data and post_id:
                picture_file = save_post_picture(post_id, form.picture.data, None)
                update_post_picture(post_id, picture_file)
            return redirect(url_for("users.user", username=current_user.username))
        else:
            flash('Allowed characters in topics field A~Z and a~z and 0~9 and " " and ","', "danger")

    return render_template("home.html", posts=posts, form=form, interests=interests, notifications=notifications,
                           current_user=current_user.username, profile_picture=profile_picture)


@main.route("/edit_post/<string:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    form = NewPostForm()
    notifications = fetch_notifications(current_user.username)
    post = fetch_post(post_id)
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    if form.validate_on_submit():
        if check_topic_validity(form.topic.data):
            update_post(post["username"], form.title.data, form.content.data, create_tags(form.topic.data.split(',')), post["link"])
            if form.picture.data and post["link"]:
                picture_file = save_post_picture(post["link"], form.picture.data, post["image"])
                update_post_picture(post["link"], picture_file)
            return redirect(url_for("posts.post", post_id=post_id))
        else:
            flash('Allowed characters in topics field A~Z and a~z and 0~9 and " " and ","', "danger")
    elif request.method == "GET":
        form.title.data = post["title"]
        form.topic.data = list_to_string_tags(post["tags"])
        form.content.data = post["content"]
        form.picture.data = post["image"]
    return render_template("edit_post.html", form=form, notifications=notifications, current_user=current_user.username,
                           profile_picture=profile_picture)


@main.route("/delete_post/<string:post_id>")
def delete_post_route(post_id):
    delete_post(post_id)
    return redirect(url_for("users.user", username=current_user.username))
