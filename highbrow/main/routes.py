from flask import render_template, request, Blueprint, redirect, url_for, flash
from highbrow.main.forms import NewPostForm
from highbrow.main.utils import create_new_post, fetch_next_newsfeed_posts, fetch_previous_newsfeed_posts, list_to_string_tags, update_post, delete_post, check_topic_validity, save_post_picture, update_post_picture
from highbrow.posts.utils import fetch_post
from highbrow.utils import fetch_notifications, fetch_followed_topics
from flask_login import current_user, login_required
from highbrow import pagination
from datetime import datetime

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
    posts, pagination.newsfeed_first_post_time, pagination.newsfeed_last_post_time = fetch_next_newsfeed_posts(current_user.username, datetime.now(), pagination.number_of_posts_in_a_page)
    pagination.current_newsfeed_page = 1
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
                           current_user=current_user.username, profile_picture=profile_picture,
                           current_newsfeed_page=pagination.current_newsfeed_page,
                           number_of_posts_in_a_page=pagination.number_of_posts_in_a_page)


@main.route("/next", methods=["GET", "POST"])
@main.route("/home/next", methods=["GET", "POST"])
@main.route("/index/next", methods=["GET", "POST"])
@login_required
def home_next():
    if pagination.newsfeed_first_post_time is None or pagination.newsfeed_last_post_time is None:
        pagination.newsfeed_first_post_time, pagination.newsfeed_last_post_time = pagination.previous_newsfeed_first_post_time, pagination.previous_newsfeed_last_post_time

    pagination.previous_newsfeed_first_post_time, pagination.previous_newsfeed_last_post_time = pagination.newsfeed_first_post_time, pagination.newsfeed_last_post_time

    posts, pagination.newsfeed_first_post_time, pagination.newsfeed_last_post_time = fetch_next_newsfeed_posts(current_user.username, pagination.newsfeed_last_post_time, pagination.number_of_posts_in_a_page)

    pagination.current_newsfeed_page = pagination.current_newsfeed_page + 1
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
                           current_user=current_user.username, profile_picture=profile_picture,
                           current_newsfeed_page=pagination.current_newsfeed_page,
                           number_of_posts_in_a_page=pagination.number_of_posts_in_a_page)


@main.route("/previous", methods=["GET", "POST"])
@main.route("/home/previous", methods=["GET", "POST"])
@main.route("/index/previous", methods=["GET", "POST"])
@login_required
def home_previous():
    posts, pagination.newsfeed_first_post_time, pagination.newsfeed_last_post_time = fetch_previous_newsfeed_posts(current_user.username, pagination.newsfeed_first_post_time, pagination.number_of_posts_in_a_page)

    if pagination.newsfeed_first_post_time is None or pagination.newsfeed_last_post_time is None:
        return redirect(url_for('main.home'))

    pagination.current_newsfeed_page = pagination.current_newsfeed_page - 1
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
                           current_user=current_user.username, profile_picture=profile_picture,
                           current_newsfeed_page=pagination.current_newsfeed_page,
                           number_of_posts_in_a_page=pagination.number_of_posts_in_a_page)


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
