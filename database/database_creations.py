import mysql.connector
from datetime import datetime

DATABASE_CREATION = "NO"
TABLE_TRIGGER_CREATION = "NO"


if DATABASE_CREATION is "YES":
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="root")
    mycursor = db.cursor()
    mycursor.execute("CREATE DATABASE highbrow_db")

    # Should close connection after retrieving result from a query otherwise server might reach connection limit
    mycursor.close()
    db.close()


if TABLE_TRIGGER_CREATION is "YES":
    db = mysql.connector.connect(host="localhost",
                                 user="root",
                                 passwd="root",
                                 database='highbrow_db')
    mycursor = db.cursor()

    # Creating the users table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Users
	                        (
	                            full_name VARCHAR(50) NOT NULL,
	                            username VARCHAR(20),
	                            email VARCHAR(50) NOT NULL UNIQUE,
	                            password VARCHAR(65) NOT NULL,
	                            remember_me SMALLINT DEFAULT 0,
	                            profile_picture VARCHAR(30) DEFAULT NULL,
	                            num_followers INT DEFAULT 0,
	                            num_following INT DEFAULT 0,
	                            short_bio TINYTEXT DEFAULT NULL,
	                            CONSTRAINT user_pk PRIMARY KEY(username)
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the posts table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Posts
	                        (
	                            created_by VARCHAR(20) NOT NULL,
	                            created_on DATETIME NOT NULL,
	                            post_id VARCHAR(36),
	                            title TINYTEXT NOT NULL,
	                            content TEXT NOT NULL,
	                            img VARCHAR(30) DEFAULT NULL,
	                            num_likes INT DEFAULT 0,
	                            num_comments INT DEFAULT 0,
	                            CONSTRAINT posts_pk PRIMARY KEY(post_id),
	                            CONSTRAINT user_post_fk FOREIGN KEY(created_by) REFERENCES Users(username) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the notifications table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Notifications
	                        (
	                            notif_id VARCHAR(36),
	                            hyperlink_post VARCHAR(36) DEFAULT NULL,
	                            hyperlink_user VARCHAR(20) DEFAULT NULL,
	                            notif_msg TINYTEXT DEFAULT NULL,
	                            notified_user VARCHAR(20) NOT NULL,
	                            notifying_user VARCHAR(20) NOT NULL,
	                            type ENUM('like', 'comment', 'follow') NOT NULL,
	                            not_time DATETIME NOT NULL,
	                            CONSTRAINT notif_pk PRIMARY KEY(notif_id),
	                            CONSTRAINT notified_user_fk FOREIGN KEY(notified_user) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT notifying_user_fk FOREIGN KEY(notifying_user) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT notif_hyp_user_fk FOREIGN KEY(hyperlink_user) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT notif_post_fk FOREIGN KEY(hyperlink_post) REFERENCES Posts(post_id) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the user_likes_post table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS User_likes_post
	                        (
	                            username VARCHAR(20),
	                            post_id VARCHAR(36),
	                            CONSTRAINT user_likes_post_pk PRIMARY KEY(username, post_id),
	                            CONSTRAINT user_like_post_users_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT user_like_post_posts_fk FOREIGN KEY(post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to increment likes
    try:
        mycursor.execute('''CREATE TRIGGER Post_like_increment
	                        AFTER INSERT ON User_likes_post
	                        FOR EACH ROW
	                        UPDATE Posts
	                        SET num_likes = num_likes+1
	                        WHERE post_id = NEW.post_id
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to decrement likes
    try:
        mycursor.execute('''CREATE TRIGGER Post_like_decrement
	                        AFTER DELETE ON User_likes_post
	                        FOR EACH ROW
	                        UPDATE Posts
	                        SET num_likes = num_likes-1
	                        WHERE post_id = OLD.post_id
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to decrement likes via users
    # An extra trigger is needed because mysql doesn't fire a trigger for foreign key constraints
    try:
        mycursor.execute('''CREATE TRIGGER Post_like_decrement_via_users
	                        BEFORE DELETE ON Users
	                        FOR EACH ROW
	                        UPDATE Posts
	                        SET num_likes = num_likes-1
	                        WHERE post_id IN (SELECT post_id FROM User_likes_post WHERE username=OLD.username)
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the user_comments_on_post table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS User_comments_on_post
	                        (
	                            comment_id VARCHAR(36),
	                            username VARCHAR(20),
	                            post_id VARCHAR(36),
	                            comment_body TEXT NOT NULL,
	                            created_on DATETIME NOT NULL,
	                            CONSTRAINT user_comm_on_post_pk PRIMARY KEY(comment_id, username, post_id),
	                            CONSTRAINT user_comm_post_users_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT user_comm_post_posts_fk FOREIGN KEY(post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to increment number of comments
    try:
        mycursor.execute('''CREATE TRIGGER Post_comment_increment
	                        AFTER INSERT ON User_comments_on_post
	                        FOR EACH ROW
	                        UPDATE Posts
	                        SET num_comments = num_comments+1
	                        WHERE post_id = NEW.post_id
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to decrement number of comments
    try:
        mycursor.execute('''CREATE TRIGGER Post_comment_decrement
	                        AFTER DELETE ON User_comments_on_post
	                        FOR EACH ROW
	                        UPDATE Posts
	                        SET num_comments = num_comments-1
	                        WHERE post_id = OLD.post_id
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to decrement comments via users
    # An extra trigger is needed because mysql doesn't fire a trigger for foreign key constraints
    try:
        mycursor.execute('''CREATE TRIGGER Post_comment_decrement_via_users
	                        BEFORE DELETE ON Users
	                        FOR EACH ROW
	                        UPDATE Posts
	                        SET num_comments = num_comments-1
	                        WHERE post_id IN (SELECT post_id FROM User_comments_on_post WHERE username=OLD.username)
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the user_saves_post table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS User_saves_post
	                        (
	                            username VARCHAR(20),
	                            post_id VARCHAR(36),
	                            CONSTRAINT user_saves_post_pk PRIMARY KEY(username, post_id),
	                            CONSTRAINT user_saves_post_users_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT user_saves_post_posts_fk FOREIGN KEY(post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the user_reports_post table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS User_reports_post
	                        (
	                            username VARCHAR(20),
	                            post_id VARCHAR(36),
	                            CONSTRAINT user_reports_post_pk PRIMARY KEY(username, post_id),
	                            CONSTRAINT user_reports_post_users_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT user_reports_post_posts_fk FOREIGN KEY(post_id) REFERENCES Posts(post_id) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the user_follows_user table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS User_follows_user
	                        (
	                            follower VARCHAR(20),
	                            following VARCHAR(20),
	                            CONSTRAINT user_follows_user_pk PRIMARY KEY(follower, following),
	                            CONSTRAINT user_follower_fk FOREIGN KEY(follower) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT user_following_fk FOREIGN KEY(following) REFERENCES Users(username) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to increment followers
    try:
        mycursor.execute('''CREATE TRIGGER Users_follower_increment
	                        AFTER INSERT ON User_follows_user
	                        FOR EACH ROW
	                        UPDATE Users
	                        SET num_followers = num_followers+1
	                        WHERE username = NEW.following
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to increment following
    try:
        mycursor.execute('''CREATE TRIGGER Users_following_increment
	                        AFTER INSERT ON User_follows_user
	                        FOR EACH ROW
	                        UPDATE Users
	                        SET num_following = num_following+1
	                        WHERE username = NEW.follower
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to decrement followers
    try:
        mycursor.execute('''CREATE TRIGGER Users_follower_decrement
	                        AFTER DELETE ON User_follows_user
	                        FOR EACH ROW
	                        UPDATE Users
	                        SET num_followers = num_followers-1
	                        WHERE username = OLD.following
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the trigger to decrement following
    try:
        mycursor.execute('''CREATE TRIGGER Users_following_decrement
	                        AFTER DELETE ON User_follows_user
	                        FOR EACH ROW
	                        UPDATE Users
	                        SET num_following = num_following-1
	                        WHERE username = OLD.follower
	                        ''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the Contact_info table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Contact_info
	                        (
	                            contact_title VARCHAR(20),
	                            contact_link VARCHAR(50),
	                            username VARCHAR(20),
	                            CONSTRAINT contact_info_pk PRIMARY KEY(contact_title, contact_link, username),
	                            CONSTRAINT contact_info_user_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the Experience table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Experience
	                        (
	                            designation VARCHAR(30),
	                            institution VARCHAR(40),
	                            username VARCHAR(20),
	                            CONSTRAINT experience_pk PRIMARY KEY(designation, institution, username),
	                            CONSTRAINT experience_user_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the Topics table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Topics
	                        (
	                            topic_name VARCHAR(35),
	                            CONSTRAINT topics_pk PRIMARY KEY(topic_name)
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the user_follows_topic table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS User_follows_topic
	                        (
	                            topic_name VARCHAR(35),
	                            username VARCHAR(20),
	                            CONSTRAINT user_follows_topic_pk PRIMARY KEY(topic_name, username),
	                            CONSTRAINT topic_follow_user_user_fk FOREIGN KEY(username) REFERENCES Users(username) ON DELETE CASCADE,
	                            CONSTRAINT topic_follow_user_topic_fk FOREIGN KEY(topic_name) REFERENCES Topics(topic_name) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Creating the post_has_topic table
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS Post_has_topic
	                        (
	                            topic_name VARCHAR(35),
	                            post_id VARCHAR(36),
	                            CONSTRAINT post_has_topic_pk PRIMARY KEY(topic_name, post_id),
	                            CONSTRAINT post_has_topic_post_fk FOREIGN KEY(post_id) REFERENCES Posts(post_id) ON DELETE CASCADE,
	                            CONSTRAINT post_has_topic_topic_fk FOREIGN KEY(topic_name) REFERENCES Topics(topic_name) ON DELETE CASCADE
	                        )''')
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

    # Should close connection after retrieving result from a query otherwise server might reach connection limit
    db.commit()
    mycursor.close()
    db.close()
