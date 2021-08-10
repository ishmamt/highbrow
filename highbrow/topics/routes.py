from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.topics.utils import fetch_topic_posts, follow_unfollow_topic, if_is_following_topic
from highbrow.utils import fetch_notifications
from flask_login import current_user

topics = Blueprint('topics', __name__)  # similar to app = Flask(__name__)

initial_topics = ["HTML", "CSS", "AI", "ML", "RNN", "CNN", "NEURAL NETWORKS", "QUESTION", "HELP",
                  "LSTM", "NLP", "IMAGE PROCESSING", "FLASK", "NETWORKS", "PYTHON", "DJANGO"]


@topics.route("/topic/<string:topic_name>")
def topic(topic_name):
    posts = fetch_topic_posts(topic_name, current_user.username)
    notifications = fetch_notifications(current_user.username)
    is_following = if_is_following_topic(current_user.username, topic_name)
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_name,
                           current_user=current_user.username, is_following=is_following, profile_picture=profile_picture)


@topics.route("/follow/topic/<string:username>/<string:topic_name>/<string:is_following>")
def follow_topic(username, topic_name, is_following):
    profile_picture = url_for('static', filename='profile_pictures/' + current_user.profile_picture)
    follow_unfollow_topic(username, topic_name, is_following)
    return redirect(url_for("topics.topic", topic_name=topic_name, profile_picture=profile_picture))


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html", initial_topics=initial_topics)
