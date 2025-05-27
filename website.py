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
    # Gets the data in a row format which behaves like a tuple and a dictionary
    db.row_factory = sqlite3.Row
    return db.cursor()

@app.route('/')
def index():
    # Main page where categories are shown
    cursor = db_connect()
    query = "SELECT * FROM categories"
    cursor.execute(query)
    categories = cursor.fetchall()
    cursor.close()
    return render_template('main.html', categories=categories)

@app.route('/quiz/<int:sub_id>')
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
    return redirect(url_for('show_questions', sub_id=sub_id))

@app.route('/questions/<int:sub_id>')
# Function to show the questions for the selected subject
def show_questions(sub_id):
    cursor = db_connect()
    cur_question_index = session.get("cur_question_index", 0)
    questions = session.get("questions")
    question = questions[cur_question_index]
    query = "SELECT * FROM ans_options WHERE question_id = ?"
    ans_options = cursor.execute(query, (question['id'],)).fetchall()
    options_text = []
    for option in ans_options:
        options_text.append(option)
    cursor.close()
    return render_template('question.html', question=question, options=options_text)

@app.route('/answer', methods=['POST'])
def answer():
    question_id = request.form['question_id']
    selected_option = request.form['selected_option']
    cursor = db_connect()
    query = "SELECT * FROM ans_options WHERE id > 210 AND question_id = ?"
    cursor.execute(query, (question_id,))
    questions = cursor.fetchall()
    # Check if the selected option is correct  
    correct = selected_option == questions[0]['answer']
    session['cur_question_index'] += 1
    cursor.close()
    return render_template('answer.html', correct=correct, question=questions)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
