from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.topics.utils import fetch_topic_posts
from highbrow.utils import fetch_notifications
from flask_login import current_user

topics = Blueprint('topics', __name__)  # similar to app = Flask(__name__)

initial_topics = ["HTML", "CSS", "AI", "ML", "RNN", "CNN", "NEURAL NETWORKS", "QUESTION", "HELP",
                  "LSTM", "NLP", "IMAGE PROCESSING", "FLASK", "NETWORKS", "PYTHON", "DJANGO"]


@topics.route("/topic/<string:topic_name>")
def topic(topic_name):
    posts = fetch_topic_posts(topic_name)
    notifications = fetch_notifications(current_user.username)
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_name,
                           current_user=current_user.username)


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html", initial_topics=initial_topics)
