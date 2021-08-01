import mysql.connector
from highbrow import db
from highbrow.utils import if_is_liked
from datetime import datetime
import uuid


def create_new_post(created_by, title, content, tags):
    mycursor = db.cursor(buffered=True)
    try:
        post_id = str(uuid.uuid4())
        mycursor.execute('''INSERT INTO Posts(created_by, created_on, post_id, title, content) VALUES(%s, %s, %s, %s, %s)''',
                         (created_by, datetime.now(), post_id, title, content))

        mycursor.execute('''DELETE FROM Post_has_topic WHERE post_id='%s' ''' % (post_id))
        for tag in tags:
            mycursor.execute('''INSERT INTO Post_has_topic(topic_name, post_id) VALUES(%s, %s)''', (tag, post_id))

        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()
    mycursor.close()


def process_tag_links(topic_name):
    topic_name = topic_name.split()
    link = ""
    for section in topic_name:
        link = link + section

    return link


def fetch_index_posts(current_user):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor(buffered=True)
    mycursor_topics = topics_connection.cursor(buffered=True)
    try:
        posts = list()
        mycursor.execute("""SELECT * FROM Posts WHERE post_id IN (
            SELECT post_id FROM Posts WHERE created_by IN (
                SELECT following FROM User_follows_user WHERE follower ='%s')
            ) OR post_id IN (
            SELECT DISTINCT post_id FROM Post_has_topic WHERE topic_name IN (
                SELECT topic_name FROM User_follows_topic WHERE username ='%s')
            ) ORDER BY created_on DESC
            """ % (current_user, current_user))
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
                "is_liked": if_is_liked(current_user, post[2])
            }
            if single_post not in posts:
                posts.append(single_post)
        mycursor.close()
        topics_connection.close()
        return posts
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        topics_connection.close()
        mycursor.close()
