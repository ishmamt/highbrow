import mysql.connector
from highbrow import db
from datetime import datetime
HYPERLINK_POST = 1
HYPERLINK_USER = 2


def fetch_notifications(username):
    mycursor = db.cursor()
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
