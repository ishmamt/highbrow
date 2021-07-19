from highbrow import db
import mysql.connector


def find_user(username):
    mycursor = db.cursor()
    try:
        mycursor.execute("SELECT * FROM Users WHERE username = '%s'" % (username))
        user = mycursor.fetchone()
        mycursor.close()
        return user
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
