import mysql.connector
from datetime import datetime

db = mysql.connector.connect(host="localhost",
                             user="root",
                             passwd="root",
                             database='highbrow_db')
mycursor = db.cursor()

# try:
#     mycursor.execute('''INSERT INTO Users(full_name, username, email, password) VALUES(%s, %s, %s, %s)''',
#                      ("Tauseef Tajwar", "tauseef09", "tauseef.tajwar36@gmail.com", "password"))
#     db.commit()
# except mysql.connector.Error as err:
#     db.rollback()
#     print("Something went wrong: {}".format(err))


# try:
#     mycursor.execute('''SELECT * FROM users''')
# except mysql.connector.Error as err:
#     print("Something went wrong: {}".format(err))

# for x in mycursor:
#     print(x)


# topic1 = "Machine Learning"
# topic2 = "HTML"
# topic3 = "CSS"
# topic4 = "Python"
# try:
#     mycursor.execute('''INSERT INTO Topics(topic_name) VALUES('%s')''' % (topic1))
#     mycursor.execute('''INSERT INTO Topics(topic_name) VALUES('%s')''' % (topic2))
#     mycursor.execute('''INSERT INTO Topics(topic_name) VALUES('%s')''' % (topic3))
#     mycursor.execute('''INSERT INTO Topics(topic_name) VALUES('%s')''' % (topic4))
# except mysql.connector.Error as err:
#     print("Something went wrong: {}".format(err))

# db.commit()


try:
    mycursor.execute('''SELECT * FROM post_has_topic''')
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

for x in mycursor:
    print(x)

mycursor.close()
db.close()
