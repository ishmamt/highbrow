import mysql.connector
from highbrow import db


def process_tag_links(topic_name):
    topic_name = topic_name.split()
    link = ""
    for section in topic_name:
        link = link + section

    return link


def fetch_post(post_id):
    topics_connection = mysql.connector.connect(host="localhost",
                                                user="root",
                                                passwd="root",
                                                database='highbrow_db')
    mycursor = db.cursor()
    mycursor_topics = topics_connection.cursor()
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
            "user_profile_link": post[0]
        }
        mycursor.close()
        topics_connection.close()
        return post
    except mysql.connector.Error as err:
        print("Something went wrong {}".format(err))
        topics_connection.close()
        mycursor.close()
