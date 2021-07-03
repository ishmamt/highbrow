from flask import render_template, request, Blueprint
from highbrow.main.forms import NewPostForm

main = Blueprint('main', __name__)  # similar to app = Flask(__name__)


posts = [
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
        "username": "Ishmam",
        "time": 3,
        "title": "First Post",
        "content": "The website is live and this is my very first post",
        "tags": ["HTML", "CSS", "Flask", "Python", "Webdev"],
        "likes": 125,
        "comments": 533
    },
    {
        "username": "Nafis",
        "time": 3,
        "title": "Eta ki free?",
        "content": "Etae taka deya lagbe ki?",
        "tags": ["Question", "Confused", "Help"],
        "likes": 525,
        "comments": 14
    }
]
interests = ["HTML", "PHP", "CSS", "JAVASCRIPT", "PYTHON"]


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
    return render_template("home.html", posts=posts, form=form, interests=interests)
