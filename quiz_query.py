""""""

import sqlite3

DATABASE = "quiz.db"

db = sqlite3.connect(DATABASE)
cursor = db.cursor()
query = "SELECT question FROM questions WHERE category_id = 1;"
cursor.execute(query)
results = cursor.fetchall()
for question in results:
    print("".join(question))