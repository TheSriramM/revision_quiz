""""""

import sqlite3
import random

DATABASE = "quiz.db"
ans_no = 0

db = sqlite3.connect(DATABASE)
cursor = db.cursor()
query = "SELECT question FROM questions WHERE category_id = 4;"
cursor.execute(query)
results = cursor.fetchall()
for question in results:
    print("".join(question))
    id_query = "SELECT id FROM questions WHERE question = ?"
    cursor.execute(id_query, question)
    q_id = cursor.fetchall()
    for item in q_id:
        for num in item:
            id = str(num)
    ans_query = "SELECT wr_ans FROM ans_options WHERE question_id = ?"
    cursor.execute(ans_query, (id,))
    wr_ans = cursor.fetchall()
    for ans in wr_ans:
        ans_no += 1
        if ans_no == 1:
            print(f"A) {"".join(ans)}")
        if ans_no == 2:
            print(f"B) {"".join(ans)}")
        if ans_no == 3:
            print(f"C) {"".join(ans)}")           