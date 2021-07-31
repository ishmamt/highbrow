from highbrow import db
import mysql.connector


def find_user(username):
    mycursor = db.cursor()
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


def fetch_own_posts(username):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor()
    mycursor_topics = topics_connection.cursor()
    try:
        posts = list()
        mycursor.execute("SELECT * FROM Posts WHERE created_by = '%s'" % (username))
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
                "user_profile_link": post[0]
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
    mycursor = db.cursor()
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
    mycursor = db.cursor()
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
    mycursor = db.cursor()
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
    mycursor = db.cursor()
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
