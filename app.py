from flask import Flask, request, jsonify
import random

app = Flask(__name__) #referencing this file

# dictionary with question, correct answer, and explanation
question_bank = [
    {
        "question": "Which word has the underlined part pronounced differently from that of the others? \nA. destroys \nB. controls \nC. predicts \nD. wanders",
        "correct_answer": "C. predicts",
        "explanation": "Sounds ending in: /f/, /k/ /p/, /t/, /θ/: s is pronounced as /s/\nSounds ending in: /s/, /t∫/, /dʒ/, /z/, / ∫ /, /ʒ/: s is pronounced as /iz/\nThe remaining sounds: s is pronounced as /z/\n\n→ destroys, controls, wanders: /z/\npredicts: /s/"
    },
    {
        "question": "Jane: There's a crack in the pipe in my kitchen. What should I do?\nAnnie: You should _____ a plumber check it tomorrow\nA. have\nB. having\nC. allow\nD. allowing",
        "correct_answer": "A. have",
        "explanation": "Have + somebody + V0: yêu cầu ai làm gì"
    },
]

# Route to get a random question
@app.route('/get_question', methods=['GET'])
def get_question():
    question_data = random.choice(question_bank)  # Pick a random question
    return jsonify({"question": question_data["question"]})

# Route to check the answer
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    user_question = data.get("question", "")
    user_answer = data.get("answer", "")

    # Find the matching question in the bank
    matched_question = next((q for q in question_bank if q["question"] == user_question), None)

    if matched_question:
        correct_answer = matched_question["correct_answer"]
        explanation = matched_question["explanation"]

        if user_answer == correct_answer:
            return jsonify({
                "question": user_question,
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "message": "✅ Correct! 🎉",
                "explanation": explanation
            })
        else:
            return jsonify({
                "question": user_question,
                "your_answer": user_answer,
                "correct_answer": correct_answer,
                "message": "❌ Incorrect.",
                "explanation": explanation
            })
    else:
        return jsonify({"message": "Question not found."})
    
