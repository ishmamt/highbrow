from flask import render_template, request, Blueprint, redirect, url_for
from highbrow.main.forms import NewPostForm
from highbrow.main.utils import create_new_post, fetch_own_posts
from flask_login import current_user

main = Blueprint('main', __name__)  # similar to app = Flask(__name__)


interests = [
    {
        "name": "CNN",
        "link": "/topic"
    },
    {
        "name": "RNN",
        "link": "/topic"
    },
    {
        "name": "ML",
        "link": "/topic"
    },
    {
        "name": "DEEP LEARNING",
        "link": "/topic"
    },
    {
        "name": "MACHINE LEARNING",
        "link": "/topic"
    },
    {
        "name": "LSTM",
        "link": "/topic"
    },
    {
        "name": "AI",
        "link": "/topic"
    },

]

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


def create_tags(tags):
    post_tags = list()
    for tag in tags:
        tag = tag.upper()
        post_tags.append(tag)
    return post_tags


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
@main.route("/index", methods=["GET", "POST"])
def home():
    posts = fetch_own_posts("tauseef09")
    form = NewPostForm()
    if form.validate_on_submit() and request.method == "POST":
        create_new_post(current_user.username, form.title.data, form.content.data, create_tags(form.topic.data.split(', ')))
        return redirect(url_for("main.home"))
    return render_template("home.html", posts=posts, form=form, interests=interests, notifications=notifications)
