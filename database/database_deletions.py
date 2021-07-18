import mysql.connector
from datetime import datetime

DELETE_ALL = "NO"

if DELETE_ALL is "YES":
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="root",
                                 database='highbrow_db')
    mycursor = db.cursor()

    # Deleting the Post_like_decrement_via_users trigger
    try:
        mycursor.execute("DROP TRIGGER Post_like_decrement_via_users")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the Post_like_increment trigger
    try:
        mycursor.execute("DROP TRIGGER Post_like_increment")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the Post_like_decrement trigger
    try:
        mycursor.execute("DROP TRIGGER Post_like_decrement")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the Post_comment_decrement_via_users trigger
    try:
        mycursor.execute("DROP TRIGGER Post_comment_decrement_via_users")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the Post_comment_increment trigger
    try:
        mycursor.execute("DROP TRIGGER Post_comment_increment")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the Post_comment_decrement trigger
    try:
        mycursor.execute("DROP TRIGGER Post_comment_decrement")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the User_follower_increment trigger
    try:
        mycursor.execute("DROP TRIGGER Users_follower_increment")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the User_following_increment trigger
    try:
        mycursor.execute("DROP TRIGGER Users_following_increment")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the User_follower_decrement trigger
    try:
        mycursor.execute("DROP TRIGGER Users_follower_decrement")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the User_following_decrement trigger
    try:
        mycursor.execute("DROP TRIGGER Users_following_decrement")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the users_likes_post table
    try:
        mycursor.execute("DROP TABLE User_likes_post")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the user_comments_on_post table
    try:
        mycursor.execute("DROP TABLE User_comments_on_post")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the User_follows_user table
    try:
        mycursor.execute("DROP TABLE User_follows_user")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the user_saves_post table
    try:
        mycursor.execute("DROP TABLE User_saves_post")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the user_reports_post table
    try:
        mycursor.execute("DROP TABLE User_reports_post")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the notifications table first because it has the foreign key to posts and topics
    try:
        mycursor.execute("DROP TABLE Notifications")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the post_has_topic table first because it has the foreign key to posts and topics
    try:
        mycursor.execute("DROP TABLE Post_has_topic")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the posts table first because it has the foreign key to users
    try:
        mycursor.execute("DROP TABLE Posts")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the contact_info table first because it has the foreign key to users
    try:
        mycursor.execute("DROP TABLE Contact_info")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the experience table first because it has the foreign key to users
    try:
        mycursor.execute("DROP TABLE Experience")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the user_follows_topic table first because it has the foreign key to users and topics
    try:
        mycursor.execute("DROP TABLE User_follows_topic")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the topics table
    try:
        mycursor.execute("DROP TABLE Topics")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Deleting the users table
    try:
        mycursor.execute("DROP TABLE Users")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Should close connection after retrieving result from a query otherwise server might reach connection limit
    mycursor.close()
    db.close()
