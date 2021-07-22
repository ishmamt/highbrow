from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.posts.forms import PostForm
from highbrow.posts.utils import fetch_post

posts = Blueprint('posts', __name__)  # similar to app = Flask(__name__)


comments = [
    {
        "username": "Tauseef Tajwar",
        "user_profile_link": "/user",
        "time": 3,
        "comment": "Testing 123"
    },
    {
        "username": "Ishmam",
        "user_profile_link": "/user",
        "time": 4,
        "comment": "Hello"
    },
    {
        "username": "Nafis",
        "user_profile_link": "/user",
        "time": 10,
        "comment": "Hello World"
    }
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


@posts.route("/post/<string:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = fetch_post(post_id)
    comment_form = PostForm()
    if comment_form.validate_on_submit() and request.method == "POST":
        comment_entry = {
            "username": "Tauseef Tajwaar",
            "user_profile_link": "/user",
            "time": 0,
            "comment": comment_form.comment.data
        }
        comments.append(comment_entry)
    return render_template("post.html", comment_form=comment_form, comments=comments,
                           number_of_comments=post["comments"], post_details=post, notifications=notifications)
