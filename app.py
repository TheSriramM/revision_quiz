"""This program is the flask version of my command line python code"""

"""This program allows the user to revise for a specific subject (maths, science or english).
Within these subjects the user can choose to look at a specific category such as physics in science or algebra in maths
The questions will be displayed in a random order"""
from flask import Flask, session, request, render_template, redirect, url_for
import sqlite3
import random

# Variable declarations
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
    # Get the category data
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
    random.shuffle(questions)
    # Define session variables that are user specific before the questions are displayed
    session["cur_question_index"] = 0
    session['questions'] = [dict(q) for q in questions]
    session["category"] = sub_id
    session["correct_no"] = 0
    session["limit"] = False
    cursor.close()
    return redirect(url_for('show_questions', sub_id=sub_id))

# Create a route with the sub_id at the end
@app.route('/questions/<int:sub_id>')
# Function to show the questions for the selected subject
def show_questions(sub_id):
    cursor = db_connect()
    # Get the session variables
    cur_question_index = session.get("cur_question_index", 0)
    questions = session.get("questions")
    # Get the specific question that needs to be displayed
    question = questions[cur_question_index]
    query = "SELECT * FROM ans_options WHERE question_id = ?"
    cursor.execute(query, (question['id'],))
    ans_options = cursor.fetchall()
    options_text = list(ans_options)
    # Shuffle the answer options
    random.shuffle(options_text)
    cursor.close()
    return render_template('question.html', questions=question, options=options_text)

# Route to manage inputs on the web server
@app.route('/answer', methods=['POST'])
def answer():
    question_id = request.form['question_id']
    selected_option = request.form['selected_option']
    cursor = db_connect()
    query = "SELECT * FROM ans_options WHERE id > 210 AND question_id = ?"
    cursor.execute(query, (question_id,))
    questions = cursor.fetchall()
    # Check if the selected option is correct
    if session["cur_question_index"] < 9:  
        session['cur_question_index'] += 1
    else:
        session["limit"]=True
    correct = selected_option == questions[0]['answer']
    if correct:
        session["correct_no"] += 1
    cursor.close()
    return render_template('answer.html', correct=correct, questions=questions, sub_id=session.get('category'), answer=questions[0]['answer'], limit=session["limit"])

@app.route('/result')
def result():
    return render_template('result.html', cor_answers=session["correct_no"])

if __name__ == "__main__":
    app.run(debug=True)