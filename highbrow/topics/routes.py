from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.topics.utils import fetch_next_topic_posts, fetch_previous_topic_posts, follow_unfollow_topic, if_is_following_topic
from highbrow.utils import fetch_notifications
from flask_login import current_user
from highbrow import pagination
from datetime import datetime

topics = Blueprint('topics', __name__)  # similar to app = Flask(__name__)

initial_topics = ["HTML", "CSS", "AI", "ML", "RNN", "CNN", "NEURAL NETWORKS", "QUESTION", "HELP",
                  "LSTM", "NLP", "IMAGE PROCESSING", "FLASK", "NETWORKS", "PYTHON", "DJANGO"]


@topics.route("/topic/<string:topic_name>")
def topic(topic_name):
    posts, pagination.topic_posts_first_post_time, pagination.topic_posts_last_post_time = fetch_next_topic_posts(topic_name, current_user.username, datetime.now(), pagination.number_of_posts_in_a_page)
    pagination.current_topic_posts_page = 1
    # posts = fetch_topic_posts(topic_name, current_user.username)
    notifications = fetch_notifications(current_user.username)
    is_following = if_is_following_topic(current_user.username, topic_name)
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_name,
                           current_user=current_user.username, is_following=is_following, profile_picture=profile_picture,
                           current_topic_posts_page=pagination.current_topic_posts_page,
                           number_of_posts_in_a_page=pagination.number_of_posts_in_a_page)


@topics.route("/topic/next/<string:topic_name>")
def topic_next(topic_name):
    if pagination.topic_posts_first_post_time is None or pagination.topic_posts_last_post_time is None:
        pagination.topic_posts_first_post_time, pagination.topic_posts_last_post_time = pagination.previous_topic_posts_first_post_time, pagination.previous_topic_posts_last_post_time

    pagination.previous_topic_posts_first_post_time, pagination.previous_topic_posts_last_post_time = pagination.topic_posts_first_post_time, pagination.topic_posts_last_post_time

    posts, pagination.topic_posts_first_post_time, pagination.topic_posts_last_post_time = fetch_next_topic_posts(topic_name, current_user.username, pagination.topic_posts_last_post_time, pagination.number_of_posts_in_a_page)
    pagination.current_topic_posts_page = pagination.current_topic_posts_page + 1
    # posts = fetch_topic_posts(topic_name, current_user.username)
    notifications = fetch_notifications(current_user.username)
    is_following = if_is_following_topic(current_user.username, topic_name)
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_name,
                           current_user=current_user.username, is_following=is_following, profile_picture=profile_picture,
                           current_topic_posts_page=pagination.current_topic_posts_page,
                           number_of_posts_in_a_page=pagination.number_of_posts_in_a_page)


@topics.route("/topic/previous/<string:topic_name>")
def topic_previous(topic_name):
    if pagination.topic_posts_first_post_time is None or pagination.topic_posts_last_post_time is None:
        return redirect(url_for('topics.topic', topic_name=topic_name))

    posts, pagination.topic_posts_first_post_time, pagination.topic_posts_last_post_time = fetch_previous_topic_posts(topic_name, current_user.username, pagination.topic_posts_first_post_time, pagination.number_of_posts_in_a_page)
    pagination.current_topic_posts_page = pagination.current_topic_posts_page - 1
    # posts = fetch_topic_posts(topic_name, current_user.username)
    notifications = fetch_notifications(current_user.username)
    is_following = if_is_following_topic(current_user.username, topic_name)
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_name,
                           current_user=current_user.username, is_following=is_following, profile_picture=profile_picture,
                           current_topic_posts_page=pagination.current_topic_posts_page,
                           number_of_posts_in_a_page=pagination.number_of_posts_in_a_page)


@topics.route("/follow/topic/<string:username>/<string:topic_name>/<string:is_following>")
def follow_topic(username, topic_name, is_following):
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    follow_unfollow_topic(username, topic_name, is_following)
    return redirect(url_for("topics.topic", topic_name=topic_name, profile_picture=profile_picture))


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html", initial_topics=initial_topics)
