from flask import render_template, request, Blueprint
from highbrow.main.forms import NewPostForm

main = Blueprint('main', __name__)  # similar to app = Flask(__name__)


posts = [
    {
        "username": "Tauseef Tajwar",
        "time": 3,
        "title": "Hello World",
        "link": "/post",
        "user_profile_link": "/user",
        "content": "Testing 123",
        "tags": [
            {
                "name": "HTML",
                "link": "/topic"
            },
            {
                "name": "CSS",
                "link": "/topic"
            },
            {
                "name": "PHP",
                "link": "/topic"
            },
            {
                "name": "FLASK",
                "link": "/topic"
            }
        ],
        "likes": 25,
        "comments": 4
    },
    {
        "username": "Ishmam",
        "time": 3,
        "title": "First Post",
        "link": "/post",
        "user_profile_link": "/user",
        "content": "The website is live and this is my very first post",
        "tags": [
            {
                "name": "ML",
                "link": "/topic"
            },
            {
                "name": "AI",
                "link": "/topic"
            },
            {
                "name": "CNN",
                "link": "/topic"
            },
            {
                "name": "RNN",
                "link": "/topic"
            }
        ],
        "likes": 125,
        "comments": 533
    },
    {
        "username": "Nafis",
        "time": 3,
        "title": "Eta ki free?",
        "link": "/post",
        "user_profile_link": "/user",
        "content": "Etae taka deya lagbe ki?",
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


@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
@main.route("/index", methods=["GET", "POST"])
def home():
    form = NewPostForm()
    if form.validate_on_submit() and request.method == "POST":
        post_entry = {
            "username": "Tauseef Tajwar",
            "time": 0,
            "title": form.title.data,
            "content": form.content.data,
            "tags": form.topic.data.split(),
            "likes": 0,
            "comments": 0
        }
        posts.append(post_entry)
    return render_template("home.html", posts=posts, form=form, interests=interests, notifications=notifications)
