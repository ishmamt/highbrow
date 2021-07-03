from flask import render_template, url_for, redirect, request, Blueprint
from highbrow.users.forms import SigninForm, SignupForm

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)


own_posts = [
    {
        "username": "Tauseef Tajwar",
        "time": 3,
        "title": "Hello World",
        "content": "Testing 123",
        "tags": ["HTML", "CSS", "Flask"],
        "likes": 25,
        "comments": 4
    },
    {
        "username": "Tauseef Tajwar",
        "time": 3,
        "title": "First Post",
        "content": "The website is live and this is my very first post",
        "tags": ["HTML", "CSS", "Flask", "Python", "Webdev"],
        "likes": 125,
        "comments": 533
    },
    {
        "username": "Tauseef Tajwar",
        "time": 3,
        "title": "Eta ki free?",
        "content": "Etae taka deya lagbe ki?",
        "tags": ["Question", "Confused", "Help"],
        "likes": 525,
        "comments": 14
    }
]

interests = ["HTML", "PHP", "CSS", "JAVASCRIPT", "PYTHON"]

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


@users.route("/user")
def user():
    return render_template("user.html", posts=own_posts, interests=interests, contacts=contacts, jobs=jobs)


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
        print("""
            """)
        print(signup_form.signup_fullname.data)
        print(signup_form.signup_username.data)
        print(signup_form.signup_email.data)
        print(signup_form.signup_password.data)
    return render_template("signin.html", signin_form=signin_form, signup_form=signup_form)
