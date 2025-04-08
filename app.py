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

if __name__ == '__main__':
    app.run(debug=True)

#python app.py to get the link, then add /get-question to see backend's response
#run the dropdown.html file and not this one ;)