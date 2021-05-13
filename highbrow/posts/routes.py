from flask import render_template, url_for, redirect, request, Blueprint

posts = Blueprint('posts', __name__)  # similar to app = Flask(__name__)


@posts.route("/post")
def post():
    return render_template("post.html")
