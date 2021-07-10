from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.posts.forms import PostForm

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

post_details = {
    "username": "Tauseef Tajwar",
    "user_profile_link": "/user",
    "time": 3,
    "likes": 200,
    "title": "Intro to ML",
    "tags": [
        {
            "name": "RNN",
            "link": "/topic"
        },
        {
            "name": "CNN",
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
            "name": "NEURAL NETWORKS",
            "link": "/topic"
        },
        {
            "name": "AI",
            "link": "/topic"
        }
    ],
    "content": """Machine learning (ML) is the study of computer algorithms that improve automatically through experience and by the use of data.[1] It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on sample data, known as "training data", in order to make predictions or decisions without being explicitly programmed to do so.[2] Machine learning algorithms are used in a wide variety of applications, such as in medicine, email filtering, speech recognition, and computer vision, where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks.[3]

A subset of machine learning is closely related to computational statistics, which focuses on making predictions using computers; but not all machine learning is statistical learning. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a related field of study, focusing on exploratory data analysis through unsupervised learning.[5][6] In its application across business problems, machine learning is also referred to as predictive analytics."""
}


@posts.route("/post", methods=["GET", "POST"])
def post():
    comment_form = PostForm()
    if comment_form.validate_on_submit() and request.method == "POST":
        comment_entry = {
            "username": "Tauseef Tajwaar",
            "time": 0,
            "comment": comment_form.comment.data
        }
        comments.append(comment_entry)
    return render_template("post.html", comment_form=comment_form, comments=comments,
                           number_of_comments=len(comments), post_details=post_details, notifications=notifications)
