from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.topics.utils import fetch_topic_posts

topics = Blueprint('topics', __name__)  # similar to app = Flask(__name__)


notifications = [
    {
        "time": 2,
        "content": "Ishmam Tashdeed commented on your post.",
        "link": "/post"
    },
    {
        "time": 4,
        "content": "Nafis Faiyaz liked your post.",
        "link": "/post"
    },
    {
        "time": 20,
        "content": "Ishmam Tashdeed liked your post.",
        "link": "/post"
    },
    {
        "time": 23,
        "content": "Nafis Faiyaz started following you.",
        "link": "/user"
    }
]

initial_topics = ["HTML", "CSS", "AI", "ML", "RNN", "CNN", "NEURAL NETWORKS", "QUESTION", "HELP",
                  "LSTM", "NLP", "IMAGE PROCESSING", "FLASK", "NETWORKS", "PYTHON", "DJANGO"]


@topics.route("/<string:topic_name>")
def topic(topic_name):
    posts = fetch_topic_posts(topic_name)
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_name)


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html", initial_topics=initial_topics)
