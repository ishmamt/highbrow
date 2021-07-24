from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.posts.forms import PostForm
from highbrow.posts.utils import fetch_post, create_comment, fetch_comments
from highbrow.utils import fetch_notifications
from flask_login import current_user

posts = Blueprint('posts', __name__)  # similar to app = Flask(__name__)


@posts.route("/post/<string:post_id>", methods=["GET", "POST"])
def post(post_id):
    post = fetch_post(post_id)
    comments = fetch_comments(post_id)
    notifications = fetch_notifications(current_user.username)
    comment_form = PostForm()
    if comment_form.validate_on_submit() and request.method == "POST":
        create_comment(current_user.username, post["link"], post["username"], comment_form.comment.data)
        return redirect(url_for('posts.post', post_id=post_id))
    return render_template("post.html", comment_form=comment_form, comments=comments,
                           number_of_comments=post["comments"], post_details=post, notifications=notifications,
                           current_user=current_user.username)
