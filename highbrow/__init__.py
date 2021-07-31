from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from highbrow.config import Config
import mysql.connector
from highbrow.current_user import User


"""
extensions created outside of the create_app function to keep these isolated from different versions of the
app being created. Also different versions of the app can use same extensions
"""
db = mysql.connector.connect(host="localhost",
                             user="root",
                             passwd="root",
                             database='highbrow_db')
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.signin"  # the name of the function to handle log in page.
login_manager.login_message_category = "info"  # bootsrap class


@login_manager.user_loader
def load_user(username):
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT * FROM Users WHERE username = '%s'" % (username))
        user_details = mycursor.fetchone()
        if user_details is None:
            mycursor.close()
            return user_details
        user = User(user_details[0], user_details[1], user_details[2], user_details[3], user_details[4],
                    user_details[5], user_details[6], user_details[7], user_details[8])
        mycursor.close()
        return user
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extentions
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from highbrow.users.routes import users
    from highbrow.posts.routes import posts
    from highbrow.main.routes import main
    from highbrow.topics.routes import topics

    # Blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(topics)

    return app
