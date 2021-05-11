from flask import Flask


def create_app():
    app = Flask(__name__)

    from highbrow.users.routes import users
    # from highbrow.posts.routes import posts
    from highbrow.main.routes import main

    app.register_blueprint(users)
    # app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
