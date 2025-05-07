from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from questions import question_bank
import random

app = Flask(__name__)  # Referencing this file
CORS(app)

# Store the current question
current_question = None


# Route to get a random question with dropdown bar
@app.route("/get-question", methods=["GET"])
def question():
    category = request.args.get("category", "Phonetics")
    questions = question_bank.get(category, [])

    question = random.choice(questions)
    return jsonify(question)

@app.route("/get-answer", methods=["POST","GET"])
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
    

if __name__ == '__main__':
    app.run(debug=True)

#python app.py to get the link, then add /get-question to see backend's response
#run the dropdown.html file and not this one ;)