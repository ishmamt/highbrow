from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)  # similar to app = Flask(__name__)


@main.route("/")
@main.route("/home")
@main.route("/index")
def home():
    return render_template("home.html")
