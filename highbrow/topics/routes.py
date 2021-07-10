from flask import render_template, url_for, redirect, request, Blueprint

topics = Blueprint('topics', __name__)  # similar to app = Flask(__name__)


topic_details = {
    "name": "CNN"
}

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

posts = [
    {
        "username": "Tauseef Tajwar",
        "time": 3,
        "title": "Hello World",
        "link": "/post",
        "user_profile_link": "/user",
        "tags": [
            {
                "name": "HTML",
                "link": "/topic"
            },
            {
                "name": "CSS",
                "link": "/topic"
            }
        ],
        "likes": 25,
        "comments": 4
    },
    {
        "username": "Tauseef Tajwar",
        "time": 30,
        "title": "First Post",
        "link": "/post",
        "user_profile_link": "/user",
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
            }
        ],
        "likes": 125,
        "comments": 533
    },
    {
        "username": "Tauseef Tajwar",
        "time": 45,
        "title": "Eta ki free?",
        "link": "/post",
        "user_profile_link": "/user",
        "tags": [
            {
                "name": "QUESTION",
                "link": "/topic"
            },
            {
                "name": "HELP",
                "link": "/topic"
            }
        ],
        "likes": 525,
        "comments": 14
    }
]

initial_topics = ["HTML", "CSS", "AI", "ML", "RNN", "CNN", "NEURAL NETWORKS", "QUESTION", "HELP",
                  "LSTM", "NLP", "IMAGE PROCESSING", "FLASK", "NETWORKS", "PYTHON", "DJANGO"]


@topics.route("/topic")
def topic():
    return render_template("topic.html", notifications=notifications, posts=posts, topic_details=topic_details)


@topics.route("/choose_topics")
def choose_topics():
    return render_template("choose_topics.html", initial_topics=initial_topics)
