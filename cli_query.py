"""This program allows the user to revise for a specific subject (maths, science or english).
Within these subjects the user can choose to look at a specific category such as physics in science or algebra in maths
The questions will be displayed in a random order"""

import sqlite3
import random

DATABASE = "quiz.db"
db = sqlite3.connect(DATABASE)
cursor = db.cursor()
query = "SELECT question FROM questions"
cursor.execute(query)
results = cursor.fetchall()
random.shuffle(results)

def main():
    # Variable declarations
    ans_no = 0
    ans_list = []
    score = 0
    # Intro
    print("Welcome to the revision quiz database!")
    print("You can exit this quiz and select another category by entering 'exit' at anytime")
    print("You can break this application by entering 'break' at anytime")
    print("What category would you like to revise: ")
    print("1. Physics\n2. Biology\n3. Chemistry\n4. Geometry\n5. Algebra\n6. Language features\n7. Parts of speech")
    num = input("Enter the number of the category you want to revise (1-7): ")
    # Check if the input is a number or not
    while not num.isnumeric():
        if num.lower() == "break":
            print("\n QUIZ EXITED")
            exit()
        elif num.lower() == "exit":
            print("\n RESTARTING QUIZ \n")
            main()
        print("Please enter a number between 1 and 7")
        num = input("Enter the number of the category you want to revise (1-7): ")
    # Check if the number is between 1 and 7
    while 0 > int(num) or 7 < int(num):
        print("Please enter a number between 1 and 7")
        num = input("Enter the number of the category you want to revise (1-7): ")    
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    # Substitute the category id
    query = "SELECT question FROM questions WHERE category_id = ?;"
    cursor.execute(query, num)
    results = cursor.fetchall()
    random.shuffle(results)
    for question in results:
        ans_list.clear()
        ans_no = 0
        # Print the question in bold
        print("\n" + "\033[1m" + "".join(question) + "\033[0m")
        # Find the id of the question
        id_query = "SELECT id FROM questions WHERE question = ?"
        cursor.execute(id_query, question)
        q_id = cursor.fetchall()
        # Turn the id from a number inside a tuple inside a list to a string
        for item in q_id:
            for num in item:
                id = str(num)
        # Find the correct answers
        cor_ans = "SELECT answer FROM ans_options WHERE id > 210 AND question_id = ?"
        cursor.execute(cor_ans, (id,))
        cor_answer = cursor.fetchall()
        for tup in cor_answer:
            cor_ans = "".join(tup)
        # Find the wrong answers
        ans_query = "SELECT answer FROM ans_options WHERE question_id = ?"
        cursor.execute(ans_query, (id,))
        wr_ans = cursor.fetchall()
        for ans in wr_ans:
            # Append each of the wrong answers into the answer list
            ans_list.append("".join(ans))
        # Shuffle the questions
        random.shuffle(ans_list)
        # Print each of the answers
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
        if inp == "BREAK":
            print("\n QUIZ EXITED")
            exit()
        if inp == "EXIT":
            print("\n RESTARTING QUIZ \n")
            main()
        while inp != "A" and inp != "B"  and inp != "C" and inp != "D":
            inp = input("Please enter a valid letter: ")
            inp = inp.upper()
        if inp == letter:
            print("CORRECT!")
            score += 1
        else:
            print("WRONG!")
            print(f"The correct answer was {letter} - {cor_ans}")

    # Output the score the user got
    print(f"You got {score} answers correct out of 10.")

main()