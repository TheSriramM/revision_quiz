""""""

import sqlite3
import random

DATABASE = "quiz.db"
ans_no = 0
ans_list = []
score = 0

print("Welcome to the Y11 revision database!")
# For next time
# category = input("What subject do you want to revise (maths, science or english): ")
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
    cor_ans_query = "SELECT cor_answer FROM questions WHERE id = ?"
    cursor.execute(cor_ans_query, (int(id),))
    cor_ans = cursor.fetchall()
    for tup in cor_ans:
        cor_ans = "".join(tup)
    ans_list.append(cor_ans)
    ans_query = "SELECT wr_ans FROM ans_options WHERE question_id = ?"
    cursor.execute(ans_query, (id,))
    wr_ans = cursor.fetchall()
    for ans in wr_ans:
        ans_list.append("".join(ans))
    random.shuffle(ans_list)
    for item in ans_list:
        ans_no += 1
        if ans_no == 1:
            print(f"A) {item}")
            if cor_ans == item:
                letter = "A"
        elif ans_no == 2:
            print(f"B) {item}")
            if cor_ans == item:
                letter = "B"
        elif ans_no == 3:
            print(f"C) {item}")
            if cor_ans == item:
                letter = "C"
        elif ans_no == 4:
            print(f"D) {item}")
            if cor_ans == item:
                letter = "D"
    inp = input("Please enter A, B, C or D: ")
    inp = inp.upper()
    if inp == letter:
        print("CORRECT!")
        score += 1
    else:
        print("WRONG!")
        print(f"The correct answer was {letter} - {cor_ans}")

print(f"You got {score} answers correct out of 10.")
db.close()