from highbrow import db
from highbrow.utils import generate_notif_msg, if_is_liked, if_is_saved
import mysql.connector
from datetime import datetime


def find_user(username):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute("SELECT * FROM Users WHERE username = '%s'" % (username))
        user = mycursor.fetchone()
        user_details = {
            "name": user[0],
            "username": user[1],
            "short_bio": user[8],
            "following": user[7],
            "followers": user[6]
        }
        mycursor.close()
        return user_details
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()


def process_tag_links(topic_name):
    topic_name = topic_name.split()
    link = ""
    for section in topic_name:
        link = link + section

    return link


def fetch_own_posts(username, current_user):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor(buffered=True)
    mycursor_topics = topics_connection.cursor(buffered=True)
    try:
        posts = list()
        mycursor.execute("SELECT * FROM Posts WHERE created_by = '%s' ORDER BY created_on DESC" % (username))
        for post in mycursor:
            tags = list()
            try:
                mycursor_topics.execute("SELECT topic_name FROM post_has_topic WHERE post_id = '%s'" % (post[2]))
                for tag in mycursor_topics:
                    single_tag = {
                        "name": tag[0],
                        "link": process_tag_links(tag[0])
                    }
                    tags.append(single_tag)
            except mysql.connector.Error as err:
                print("Something went wrong {}".format(err))

            single_post = {
                "username": post[0],
                "time": post[1],
                "link": post[2],
                "title": post[3],
                "content": post[4],
                "likes": post[6],
                "comments": post[7],
                "tags": tags,
                "user_profile_link": post[0],
                "is_liked": if_is_liked(current_user, post[2]),
                "is_saved": if_is_saved(current_user, post[2])
            }
            posts.append(single_post)
        mycursor.close()
        topics_connection.close()
        return posts
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        topics_connection.close()
        mycursor.close()


def check_user(username):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute("SELECT * FROM Users WHERE username = '%s'" % (username))
        user = mycursor.fetchone()
        mycursor.close()
        return user
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()
        return None


def check_email(email):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute("SELECT * FROM Users WHERE email = '%s'" % (email))
        email = mycursor.fetchone()
        mycursor.close()
        return email
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()
        return None


def create_new_user(fullname, username, email, password):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute('''INSERT INTO Users(full_name, username, email, password) VALUES(%s, %s, %s, %s)''',
                         (fullname, username, email, password))
        db.commit()
        mycursor.close()
        return True
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()
        mycursor.close()
        return False


def if_is_following(follower, following):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute('''SELECT * FROM User_follows_user WHERE follower = '%s' AND following = '%s' ''' % (follower, following))
        follows = mycursor.fetchone()
        mycursor.close()
        if follows:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()


def follow_unfollow_user(notifying_user, notified_user, is_following):
    mycursor = db.cursor(buffered=True)
    if is_following == "True":
        # unfollow
        try:
            mycursor.execute("DELETE FROM User_follows_user WHERE follower='%s' AND following='%s'" % (notifying_user, notified_user))
            mycursor.execute('''DELETE FROM Notifications WHERE notified_user='%s' AND notifying_user='%s'
                                AND hyperlink_user='%s' AND type='follow' ''' % (notified_user, notifying_user, notifying_user))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    else:
        # follow
        try:
            mycursor.execute('''INSERT INTO User_follows_user(follower, following) VALUES(%s, %s)''',
                             (notifying_user, notified_user))
            msg = generate_notif_msg(notifying_user, 'follow')
            mycursor.execute('''INSERT INTO Notifications(notif_id, hyperlink_user, notif_msg, notified_user, notifying_user, type, not_time)
                                VALUES(UUID(), %s, %s, %s, %s, 'follow', %s)''',
                             (notifying_user, msg, notified_user, notifying_user, datetime.now()))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    mycursor.close()


def fetch_saved_posts(current_user):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor(buffered=True)
    mycursor_topics = topics_connection.cursor(buffered=True)
    try:
        posts = list()
        mycursor.execute("""SELECT * FROM Posts WHERE post_id IN (
                        SELECT post_id FROM User_saves_post WHERE username ='%s')
                        ORDER BY created_on DESC""" % (current_user))
        for post in mycursor:
            tags = list()
            try:
                mycursor_topics.execute("SELECT topic_name FROM post_has_topic WHERE post_id = '%s'" % (post[2]))
                for tag in mycursor_topics:
                    single_tag = {
                        "name": tag[0],
                        "link": process_tag_links(tag[0])
                    }
                    tags.append(single_tag)
            except mysql.connector.Error as err:
                print("Something went wrong {}".format(err))

            single_post = {
                "username": post[0],
                "time": post[1],
                "link": post[2],
                "title": post[3],
                "content": post[4],
                "likes": post[6],
                "comments": post[7],
                "tags": tags,
                "user_profile_link": post[0],
                "is_liked": if_is_liked(current_user, post[2]),
                "is_saved": if_is_saved(current_user, post[2])
            }
            posts.append(single_post)
        mycursor.close()
        topics_connection.close()
        return posts
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        topics_connection.close()
        mycursor.close()
