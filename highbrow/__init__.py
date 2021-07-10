from flask import Flask


def create_app():
    app = Flask(__name__)

    from highbrow.users.routes import users
    from highbrow.posts.routes import posts
    from highbrow.main.routes import main
    from highbrow.topics.routes import topics

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(topics)

    app.config['SECRET_KEY'] = "c37b6431d31de6dcc7e1a1fa5243c976"

    return app
