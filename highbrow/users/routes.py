from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.users.forms import SigninForm, SignupForm

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)


user_details = {
    "name": "Tauseef Tajwar",
    "current_job": "AI Researcher",
    "current_job_details": "Carnegie Mellon University",
    "following": 34,
    "followers": 115
}

own_posts = [
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
        "content": "The website is live and this is my very first post",
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

contacts = [
    {
        "website_name": "Twitter",
        "link": "https://twitter.com"
    },
    {
        "website_name": "Facebook",
        "link": "https://facebook.com"
    },
    {
        "website_name": "Email",
        "link": "https://gmail.com"
    }
]

jobs = [
    {
        "name": "Senior Product Designer",
        "details": "cwybciwbviuv"
    },
    {
        "name": "Senior UI / UX Designer",
        "details": "vcwuvybwiucvnwiucn"
    },
    {
        "name": "Senior PHP Designer",
        "details": "cwbugbwihcbwib"
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


@users.route("/user")
def user():
    return render_template("user.html", user_details=user_details, posts=own_posts, interests=interests, contacts=contacts,
                           jobs=jobs, notifications=notifications)


@users.route("/sign-in", methods=["GET", "POST"])
@users.route("/login", methods=["GET", "POST"])
@users.route("/register", methods=["GET", "POST"])
@users.route("/sign-up", methods=["GET", "POST"])
@users.route("/join", methods=["GET", "POST"])
def signin():
    signin_form = SigninForm()
    signup_form = SignupForm()
    if (signin_form.validate_on_submit() or signup_form.validate_on_submit()) and request.method == "POST":
        print(signin_form.signin_username.data)
        print(signin_form.signin_password.data)
        print(signin_form.c1.data)
        print("")
        print(signup_form.signup_fullname.data)
        print(signup_form.signup_username.data)
        print(signup_form.signup_email.data)
        print(signup_form.signup_password.data)
    return render_template("signin.html", signin_form=signin_form, signup_form=signup_form)


@users.route("/contact")
def contact():
    return render_template("contact.html")


@users.route("/about")
def about():
    return render_template("about.html")
