""""""

import sqlite3
import random

DATABASE = "quiz.db"
ans_no = 0
ans_list = []

db = sqlite3.connect(DATABASE)
cursor = db.cursor()
query = "SELECT question FROM questions WHERE category_id = 4;"
cursor.execute(query)
results = cursor.fetchall()
for question in results:
    ans_list.clear()
    ans_no = 0
    print("".join(question))
    id_query = "SELECT id FROM questions WHERE question = ?"
    cursor.execute(id_query, question)
    q_id = cursor.fetchall()
    for item in q_id:
        for num in item:
            id = str(num)
    cor_ans_query = "SELECT cor_answer FROM questions WHERE question = ?"
    cursor.execute(cor_ans_query, (id,))
    cor_ans = cursor.fetchall()
    ans_list.append(cor_ans)
    ans_query = "SELECT wr_ans FROM ans_options WHERE question_id = ?"
    cursor.execute(ans_query, (id,))
    wr_ans = cursor.fetchall()
    for ans in wr_ans:
        ans_list.append(ans)
    random.shuffle(ans_list)     