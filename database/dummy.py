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


try:
    mycursor.execute('''SELECT * FROM users''')
except mysql.connector.Error as err:
    print("Something went wrong: {}".format(err))

for x in mycursor:
    print(x)

mycursor.close()
db.close()
