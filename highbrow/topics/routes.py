from flask import render_template, url_for, redirect, request, Blueprint

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


@topics.route("/topic")
def topic():
    return render_template("topic.html", notifications=notifications)


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html")
