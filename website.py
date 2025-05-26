"""This program allows the user to revise for a specific subject (maths, science or english).
Within these subjects the user can choose to look at a specific category such as physics in science or algebra in maths
The questions will be displayed in a random order"""
from flask import Flask, session, request, render_template, redirect, url_for
import sqlite3
import random

DATABASE = "quiz.db"
ans_list = []
app = Flask(__name__)
app.secret_key = "my_secret_key"

def db_connect():
    # Connecting to the database
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    return cursor

@app.route('/')
def index():
    # Main page where categories are shown
    cursor = db_connect()
    query = "SELECT * FROM categories"
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    return render_template('main.html', categories=categories)

@app.route('/quiz/<int:subject_id>')
def quiz(sub_id):
    cursor = db_connect()
    # Query for getting the questions from the category selected by the user
    query = "SELECT * FROM Questions WHERE category_id = ?"
    cursor.execute(query, (sub_id,))
    questions = cursor.fetchall()
    # Start with the first question
    session["cur_question_index"] = 0
    session['questions'] = [dict(q) for q in questions]
    cursor.close()
    return redirect(url_for('question'))

@app.route('/questions')
def questions(sub_id):
    cursor = db_connect()
    cur_question_index = session.get("cur_question_index", 0)
    questions = session.get("questions")
    question = questions[cur_question_index]
    query = "SELECT * FROM ans_options WHERE question_id = ?"
    ans_options = cursor.execute(query, question['id']).fetchall()
    options_text = []
    for option in ans_options:
        options_text.append(option)
    cursor.close()

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
