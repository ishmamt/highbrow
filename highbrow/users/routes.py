from flask import render_template, url_for, redirect, request, Blueprint

users = Blueprint('users', __name__)  # similar to app = Flask(__name__)
