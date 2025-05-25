"""This program allows the user to revise for a specific subject (maths, science or english).
Within these subjects the user can choose to look at a specific category such as physics in science or algebra in maths
The questions will be displayed in a random order"""
from flask import Flask, session, request, render_template, redirect, url_for
import sqlite3
import random

DATABASE = "quiz.db"
ans_list = []
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def question():
    q = get_question()  # using only the first question for now
    question_text = q[0]
    cor_ans = q[1]
    ans_list = [cor_ans] + ans_options(q[2])
    result = None
    selected_answer = None
    show_next = False

    if request.method == 'POST':
        selected_answer = request.form.get('answer')
        if selected_answer == cor_ans:
            result = "✅ Correct!"
        else:
            result = f"❌ Wrong! The correct answer is {cor_ans}."
        show_next = True

    return render_template(
        'main.html',
        question=question_text,
        choices=ans_list,
        result=result,
        selected=selected_answer,
        show_next=show_next
    )

def get_question():
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    query = "SELECT question, cor_ans, id FROM questions WHERE category_id = 1;"
    cursor.execute(query)
    results = cursor.fetchall()
    random.shuffle(results)
    qe = results[0]
    id = qe[2]
    results.remove(qe)
    return qe

def ans_options(question):
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    query = "SELECT wr_ans FROM ans_options WHERE question_id = ?"
    ans_list = []
    cursor.execute(query, tuple(int(id)))
    results = cursor.fetchall()
    for item in results:
        ans_list.append(item)

if __name__ == "__main__":
    app.run(debug=True)


# def math_questions():
#     query = "SELECT question FROM questions WHERE category_id = 4 OR category_id = 5;"
#     cursor.execute(query)
#     results = cursor.fetchall()
#     random.shuffle(results)
#     for question in results:
#         print("".join(question))

# def choices(question):
#     id = "SELECT ID FROM questions WHERE question IS ?;"
#     cursor.execute(id, question)
#     results = cursor.fetchall()
#     for item in results:
#         string_id = "".join(results)
#     cor_ans_query = "SELECT cor_ans FROM questions WHERE question IS ?;"
#     cursor.execute(cor_ans_query, question)
#     results = cursor.fetchall()
#     for item in results:
#         questions["cor_ans"] = "".join(item)
#     ans_query = "SELECT wr_ans FROM ans_options WHERE question_id = ?"
#     cursor.execute(ans_query, id)
#     results = cursor.fetchall()
#     ans_options = []
#     for item in results:
#         ans_options.append("".join(item))
#     questions["answers"] = ans_options
