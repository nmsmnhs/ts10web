from flask import Flask, request, jsonify
import random

app = Flask(__name__)  # Referencing this file

# Store the current question
current_question = None

# Dictionary with question, correct answer, and explanation
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
    global current_question
    current_question = random.choice(question_bank)
    return jsonify({"question": current_question["question"]})

# Route to check the answer
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    global current_question

    if not current_question:
        return jsonify({"message": "No question has been asked yet. Call /get_question first."})

    data = request.json
    user_answer = data.get("answer", "").strip()

    correct_answer = current_question["correct_answer"]
    explanation = current_question["explanation"]

    if user_answer.lower() == correct_answer.lower():
        return jsonify({
            "question": current_question["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "message": "✅ Correct! 🎉",
            "explanation": explanation
        })
    else:
        return jsonify({
            "question": current_question["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "message": "❌ Incorrect.",
            "explanation": explanation
        })

if __name__ == '__main__':
    app.run(debug=True)
