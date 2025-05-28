let current_question = {};


document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('fetch-btn').addEventListener('click', fetch_questionAndShowUI);
    document.getElementById('submit-btn').addEventListener('click', submit_answer);

    processQuestionBank();
});

function getQuestionType(answer) {
    const cleanedAnswer = String(answer).trim().toUpperCase();
    const trueFalseOptions = ['T', 'F', 'TRUE', 'FALSE'];
    const multipleChoiceOptions = ['A', 'B', 'C', 'D'];
        if (trueFalseOptions.includes(cleanedAnswer)) {
            return 'true_false';
        }
        else if (multipleChoiceOptions.includes(cleanedAnswer)) {
             return 'multiple_choice';
        }
        return 'open_ended';
    }

async function processQuestionBank() {
    try {
        const response = await fetch('https://b982ace8-9b10-45a0-ae5c-7c004cc46047-00-205szs3wf7kek.pike.replit.dev:3000/api/questions');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const questionBank = await response.json();
            console.log("Question bank fetched successfully!");
            console.log("--- True/False Questions Found ---");

                let tfCount = 0;
                let totalCount = 0;

                // Iterate through each category
                for (const categoryName in questionBank) {
                    const questionsList = questionBank[categoryName];

                    if (!Array.isArray(questionsList)) {
                        console.warn(`Category '${categoryName}' did not contain a list of questions. Skipping.`);
                        continue;
                    }

                    // Iterate through each question in the current category
                    questionsList.forEach(q => {
                        totalCount++;
                        if (q && 'answer' in q) { // Ensure question object and 'answer' key exist
                            const questionType = getQuestionType(q.answer);
                            if (questionType === 'true_false') {
                                tfCount++;
                                console.log(`  - Question ID: ${q.id}, Category: ${categoryName}, Answer: '${q.answer}'`);
                            }
                        } else {
                            console.warn(`Question in category '${categoryName}' (ID: ${q ? q.id : 'N/A'}) is missing 'answer' key or malformed.`);
                        }
                    });
                }
                console.log(`--- Finished Processing ---`);
                console.log(`Total questions processed: ${totalCount}`);
                console.log(`Total True/False questions identified: ${tfCount}`);

            } catch (error) {
                console.error("Failed to fetch or process questions:", error);
                console.error("Please ensure your Flask backend (app.py) is running on http://127.0.0.1:5000.");
            }
        }

document.addEventListener('DOMContentLoaded', processQuestionBank);

async function fetch_question() {
    const question_display = document.getElementById('question-display');
    const type = document.getElementById('question_type').value;
    question_display.innerHTML = '';
    question_display.classList.remove('border', 'show');
    document.getElementById('results').classList.remove('border', 'show');

    if (!type) {
        question_display.innerHTML = '<div class="error"><p>Please select a question type.</p></div>';
        question_display.classList.add('show');
        return null;
    }


    question_display.innerHTML = '<div class="loading">Loading your question...</div>';
    question_display.classList.add('show');

    try {
        const response = await fetch(`https://b982ace8-9b10-45a0-ae5c-7c004cc46047-00-205szs3wf7kek.pike.replit.dev:3000/get-question?category=${encodeURIComponent(type)}&r=${Math.random()}`);
        const data = await response.json();

        if (data.error) {
            question_display.innerHTML = `<div class="error"><p>Error: ${data.error}</p></div>`;
            return null;
        } else {
            current_question = data;
            return data;
        }
    } catch (error) {
        question_display.innerHTML = '<div class="error"><p>Error fetching data. Please try again.</p></div>';
        return null;
    }
}

function displayQuestion(data) {
    const question_display = document.getElementById('question-display');
    question_display.innerHTML = `
        <h3>Question:</h3><p>${data.question}</p>
    `;
    question_display.classList.add('border');


    setTimeout(() => {
        question_display.classList.add('show');
    }, 100);
}

function showAnswerInput(questionType) {
    const answerSection = document.querySelector('.answer-section');
    const userAnswerTextarea = document.getElementById('user-answer');
    const radioAnswerABCD = document.getElementById('radio-answer');
    const radioAnswerTrueFalse = document.getElementById('true-false-answer');
    const answerLabel = document.getElementById('answer-label');
    const submitBtn = document.getElementById('submit-btn');

    answerLabel.style.display = 'block';
    userAnswerTextarea.style.display = 'none';
    radioAnswerABCD.style.display = 'none';
    radioAnswerTrueFalse.style.display = 'none';

    const currentQuestionAnswerType = current_question.answer ? getQuestionType(current_question.answer) : null;

    if (questionType === "WordForm" || questionType === "SentenceTransformation") {
        userAnswerTextarea.style.display = 'block';
        answerLabel.innerText = "Your Answer:";
    } else if (currentQuestionAnswerType === 'true_false') {
        radioAnswerTrueFalse.style.display = 'grid';
        answerLabel.innerText = "Your Answer:";
        document.querySelectorAll('input[name="user-answer"][type="radio"]').forEach(radio => {
            radio.checked = false;
        });
    } else if (questionType) {
        radioAnswerABCD.style.display = 'grid';
        answerLabel.innerText = "Your Answer:";
        document.querySelectorAll('input[name="user-answer"][type="radio"]').forEach(radio => {
            radio.checked = false;
        });
    }
    submitBtn.style.display = 'block';


    setTimeout(() => {
        answerSection.classList.add('show');
        answerSection.classList.remove('no-transition');
    }, 300);
}

function hideAnswerUI() {
    const answerSection = document.querySelector('.answer-section');
    answerSection.classList.remove('show');
    answerSection.classList.add('no-transition');

    document.getElementById('answer-label').style.display = 'none';
    document.getElementById('user-answer').style.display = 'none';
    document.getElementById('radio-answer').style.display = 'none';
    document.getElementById('true-false-answer').style.display = 'none';
    document.getElementById('submit-btn').style.display = 'none';
    document.getElementById('results').style.display = 'none';
    document.getElementById('results').classList.remove('show');
}

async function fetch_questionAndShowUI() {
    hideAnswerUI();
    const questionData = await fetch_question();
    if (questionData) {
        displayQuestion(questionData);
        showAnswerInput(document.getElementById('question_type').value);
        document.getElementById('results').innerHTML = '';
        document.getElementById('user-answer').value = '';
    }
}

function submit_answer() {
    let userAnswer = '';
    const results = document.getElementById('results');
    results.style.display = 'block';

    if (document.getElementById('user-answer').style.display === 'block') {
        userAnswer = document.getElementById('user-answer').value.trim().toLowerCase();
        if (userAnswer && !/[.!?]$/.test(userAnswer) && document.getElementById('question_type').value == "SentenceTransformation") {
            userAnswer = userAnswer + ".";
          }
        if (userAnswer === '') {
            results.innerHTML = '<div class="error"><p>Please enter your answer.</p></div>';
            results.classList.add('show');
            return;
        }
    } else if (document.getElementById('radio-answer').style.display === 'grid' || document.getElementById('true-false-answer').style.display === 'grid') {
        const selectedRadio = document.querySelector('input[name="user-answer"]:checked');
        if (selectedRadio) {
            userAnswer = selectedRadio.value.toLowerCase();
        } else {
            results.innerHTML = '<div class="error"><p>Please select your answer.</p></div>';
            results.classList.add('show');
            return;
        }
    } else {
        console.error('No answer input is visible.');
        results.innerHTML = '<div class="error"><p>An unexpected error occurred. Please try again.</p></div>';
        results.classList.add('show');
        return;
    }

    fetch(`https://b982ace8-9b10-45a0-ae5c-7c004cc46047-00-205szs3wf7kek.pike.replit.dev:3000/get-answer`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify ({
            id: current_question.id,
            userAnswer: userAnswer
        })
    })
    .then(res => res.json())
    .then(data => {
        let resultMsg = '';
            results.classList.remove('border', 'correct-result', 'incorrect-result');
        if (data.correct === true) {
            results.classList.add('border', 'correct-result');
            resultMsg = `<span style="color:#15803d; font-weight: 700; font-size: 18px;">✅ Correct! Well done!</span>`;
        } else {
            results.classList.add('border', 'incorrect-result');
            resultMsg = `<span style="color:#fa2323; font-weight: 700; font-size: 18px;">❌ Incorrect.</span>`;
        }
        resultMsg += `<h4>Explanation:</h4><p>${data.explanation}</p>`;
        results.innerHTML = resultMsg;

        setTimeout(() => {
            results.classList.add('show');
            results.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    })
    .catch(error => {
        console.error("Error submitting answer:", error);
        results.innerHTML = '<div class="error"><p>Error submitting answer. Please try again.</p></div>';
        results.classList.add('show');
    });
}