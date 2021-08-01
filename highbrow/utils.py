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
                "type": notif_type
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
                "link": topic[0]
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
