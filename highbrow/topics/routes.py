from flask import render_template, url_for, redirect, request, Blueprint

topics = Blueprint('topics', __name__)  # similar to app = Flask(__name__)


@topics.route("/topic")
def topic():
    return render_template("topic.html")


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html")
