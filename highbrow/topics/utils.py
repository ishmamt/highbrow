from highbrow import db
import mysql.connector
from highbrow.utils import if_is_liked, fetch_profile_picture, process_tag_links


def fetch_topic_posts(topic_name, current_user):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor(buffered=True)
    mycursor_topics = topics_connection.cursor(buffered=True)
    topic_name = link_to_tag(topic_name)
    try:
        posts = list()
        mycursor.execute("""SELECT * FROM Posts WHERE post_id IN (
                        SELECT post_id FROM post_has_topic WHERE topic_name = '%s') ORDER BY created_on DESC""" % (topic_name))
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
                "creator_profile_pic": fetch_profile_picture(post[0])
            }
            posts.append(single_post)
        mycursor.close()
        topics_connection.close()
        return posts
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        topics_connection.close()
        mycursor.close()


def follow_unfollow_topic(username, topic_name, is_following):
    mycursor = db.cursor(buffered=True)
    topic_name = link_to_tag(topic_name)
    if is_following == "True":
        # unfollow
        try:
            mycursor.execute("DELETE FROM User_follows_topic WHERE username='%s' AND topic_name='%s'" % (username, topic_name))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    else:
        # follow
        try:
            mycursor.execute('''INSERT INTO User_follows_topic(username, topic_name) VALUES(%s, %s)''',
                             (username, topic_name))
            db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            db.rollback()
    mycursor.close()


def if_is_following_topic(follower, topic_name):
    mycursor = db.cursor(buffered=True)
    topic_name = link_to_tag(topic_name)
    try:
        mycursor.execute('''SELECT * FROM User_follows_topic WHERE username = '%s' AND topic_name = '%s' ''' % (follower, topic_name))
        follows = mycursor.fetchone()
        mycursor.close()
        if follows:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        mycursor.close()


def link_to_tag(link):
    link = link.split("_")
    tag = ""
    for element in link:
        tag = tag + " " + element
    return tag[1:]
