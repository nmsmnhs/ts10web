let current_question = {};

document.getElementById('fetch-btn').addEventListener('click', fetch_questionAndShowUI);
document.getElementById('submit-btn').addEventListener('click', submit_answer);


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
        const response = await fetch(`http://localhost:5000/get-question?category=${encodeURIComponent(type)}&r=${Math.random()}`);
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

    document.getElementById('answer-label').style.display = 'block';
    document.getElementById('user-answer').style.display = 'none';
    document.getElementById('radio-answer').style.display = 'none';

    if (questionType === "WordForm" || questionType === "SentenceTransformation") {
        document.getElementById('user-answer').style.display = 'block';
        document.getElementById('answer-label').innerText = "Your Answer:";
    } else if (questionType) {
        document.getElementById('radio-answer').style.display = 'grid';
        document.querySelectorAll('input[name="user-answer"][type="radio"]').forEach(radio => {
            radio.checked = false;
        });
        document.getElementById('answer-label').innerText = "Your Answer:";
    }
    document.getElementById('submit-btn').style.display = 'block';


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
        if (userAnswer === '') {
            results.innerHTML = '<div class="error"><p>Please enter your answer.</p></div>';
            results.classList.add('show');
            return;
        }
    } else if (document.getElementById('radio-answer').style.display === 'grid') {
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

    fetch(`http://localhost:5000/get-answer`, {
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
        if (data.correct === true) {
            results.classList.add('border', 'correct-result');
            resultMsg = `<span style="color:#15803d; font-weight: 700; font-size: 18px;">✅ Correct! Well done!</span>`;
        } else {
            results.classList.add('border', 'incorrect-result');
            resultMsg = `<span style="color:#dc2626; font-weight: 700; font-size: 18px;">❌ Incorrect.</span>`;
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