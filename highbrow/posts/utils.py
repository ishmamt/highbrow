import mysql.connector
from highbrow import db
from highbrow.utils import generate_notif_msg, fetch_profile_picture, process_tag_links
from datetime import datetime


def fetch_post(post_id):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor(buffered=True)
    mycursor_topics = topics_connection.cursor(buffered=True)
    try:
        mycursor.execute("SELECT * FROM Posts WHERE post_id = '%s'" % (post_id))
        post = mycursor.fetchone()
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

        post = {
            "username": post[0],
            "time": post[1],
            "link": post[2],
            "title": post[3],
            "content": post[4],
            "likes": post[6],
            "comments": post[7],
            "tags": tags,
            "user_profile_link": post[0],
            "creator_profile_pic": fetch_profile_picture(post[0])
        }
        mycursor.close()
        topics_connection.close()
        return post
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        topics_connection.close()
        mycursor.close()


def fetch_comments(post_id):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute("SELECT * FROM User_comments_on_post WHERE post_id = '%s' ORDER BY created_on DESC" % (post_id))
        comments = list()
        for comment in mycursor:
            single_comment = {
                "username": comment[1],
                "user_profile_link": comment[1],
                "time": comment[4],
                "comment": comment[3],
                "creator_profile_pic": fetch_profile_picture(comment[1])
            }
            comments.append(single_comment)
        mycursor.close()
        return comments
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()
        return list()


def create_comment(notifying_user, post_id, notified_user, comment_body):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute('''INSERT INTO User_comments_on_post(comment_id, username, post_id, comment_body, created_on)
                            VALUES(UUID(), %s, %s, %s, %s)''',
                         (notifying_user, post_id, comment_body, datetime.now()))
        msg = generate_notif_msg(notifying_user, 'comment')
        mycursor.execute('''INSERT INTO Notifications(notif_id, hyperlink_post, notif_msg, notified_user, notifying_user, type, not_time)
                            VALUES(UUID(), %s, %s, %s, %s, 'comment', %s)''',
                         (post_id, msg, notified_user, notifying_user, datetime.now()))
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()
    mycursor.close()


def like_unlike_post(notifying_user, notified_user, post_id, is_liked):
    mycursor = db.cursor(buffered=True)
    if is_liked == "True":
        # unlike
        try:
            mycursor.execute("DELETE FROM User_likes_post WHERE username= '%s' AND post_id='%s'" % (notifying_user, post_id))
            mycursor.execute('''DELETE FROM Notifications WHERE notified_user='%s' AND notifying_user='%s'
                                AND hyperlink_post='%s' AND type='like' ''' % (notified_user, notifying_user, post_id))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    else:
        # like
        try:
            mycursor.execute('''INSERT INTO User_likes_post(username, post_id) VALUES(%s, %s)''',
                             (notifying_user, post_id))
            msg = generate_notif_msg(notifying_user, 'like')
            mycursor.execute('''INSERT INTO Notifications(notif_id, hyperlink_post, notif_msg, notified_user, notifying_user, type, not_time)
                                VALUES(UUID(), %s, %s, %s, %s, 'like', %s)''',
                             (post_id, msg, notified_user, notifying_user, datetime.now()))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    mycursor.close()
