from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from questions import question_bank
import random

app = Flask(__name__)
CORS(app)

current_question = None

#homepage route
@app.route('/')
def home():
    return render_template('dropdown.html') #added since replit runs straight from this file

# route to get a random question
@app.route("/get-question", methods=["GET"])
def question():
    category = request.args.get("category", "Phonetics")
    questions = question_bank.get(category, [])

    question = random.choice(questions)
    print(f"serving question from category {category}: {question}")
    return jsonify(question)

@app.route("/get-answer", methods=["POST", "GET"])
def answer():
    #receive json package & get id + answer
    data = request.get_json()
    question_id = data.get("id")
    userAnswer = data.get("userAnswer")

    #searching for id
    for categories in question_bank.values():
        for q in categories:
            if q["id"] == question_id:
                correct = userAnswer == q["answer"].strip().lower()
                return jsonify({
                    "correct": correct,
                    "explanation": q["explanation"]
                })

#get db -> transfer it to script.js -> determine which questions are multiple choice and which are t/f
@app.route('/api/questions', methods=['GET'])
def get_database():
    return jsonify(question_bank)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host="0.0.0.0", port=3000) #for public replit site
