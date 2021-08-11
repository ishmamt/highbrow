import mysql.connector
from highbrow import db
from datetime import datetime
HYPERLINK_POST = 1
HYPERLINK_USER = 2


def fetch_notifications(username):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute("SELECT * FROM Notifications WHERE notified_user='%s' ORDER BY not_time DESC LIMIT 5" % (username))
        notifications = list()
        for notification in mycursor:
            if notification[HYPERLINK_POST] is None:
                link = notification[HYPERLINK_USER]
                notif_type = "USER"
            else:
                link = notification[HYPERLINK_POST]
                notif_type = "POST"
            single_notification = {
                "time": notification[7],
                "content": notification[3],
                "link": link,
                "type": notif_type,
                "notifying_user_profile_pic": fetch_profile_picture(notification[5])
            }
            notifications.append(single_notification)
        mycursor.close()
        return notifications
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()
        return list()


def generate_notif_msg(notifying_user, typ):
    msg = notifying_user + " "
    if typ == "like":
        msg = msg + "likes your post."
    elif typ == "comment":
        msg = msg + "commented on your post."
    elif typ == "follow":
        msg = msg + "started following you."
    return msg


def fetch_followed_topics(username):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute("SELECT topic_name FROM User_follows_topic WHERE username='%s'" % (username))
        interests = list()
        for topic in mycursor:
            single_topic = {
                "name": topic[0],
                "link": process_tag_links(topic[0])
            }
            interests.append(single_topic)
        mycursor.close()
        return interests
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()


def if_is_liked(username, post_id):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute('''SELECT * FROM User_likes_post WHERE username = '%s' AND post_id = '%s' ''' % (username, post_id))
        likes = mycursor.fetchone()
        mycursor.close()
        if likes:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()


def if_is_saved(username, post_id):
    mycursor = db.cursor(buffered=True)
    try:
        mycursor.execute('''SELECT * FROM User_saves_post WHERE username = '%s' AND post_id = '%s' ''' % (username, post_id))
        saved = mycursor.fetchone()
        mycursor.close()
        if saved:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()


def add_remove_to_saved(username, post_id, is_saved):
    mycursor = db.cursor(buffered=True)
    if is_saved == "True":
        try:
            mycursor.execute("DELETE FROM User_saves_post WHERE username= '%s' AND post_id= '%s'" % (username, post_id))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    else:
        try:
            mycursor.execute('''INSERT INTO User_saves_post(username, post_id) VALUES(%s, %s)''',
                             (username, post_id))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    mycursor.close()


def fetch_profile_picture(username):
    pic_cursor = db.cursor(buffered=True)
    try:
        pic_cursor.execute('''SELECT profile_picture FROM Users WHERE username = '%s' ''' % (username))
        picture = pic_cursor.fetchone()
        pic_cursor.close()
        if picture:
            return picture[0]
        else:
            return "default.jpg"
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        pic_cursor.close()
        return "default.jpg"


def process_tag_links(topic_name):
    topic_name = topic_name.split()
    link = ""
    for section in topic_name:
        link = link + "_" + section

    return link[1:]
