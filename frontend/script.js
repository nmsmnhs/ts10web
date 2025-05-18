    let correctAnswer = '';
    let explanation = '';

    document.getElementById('fetch-btn').addEventListener('click', fetchAndhide);
    document.getElementById('submit-btn').addEventListener('click', submit_answer);

// Get question
    function fetch_question() {
        const question_display = document.getElementById('question-display');
        const type = document.getElementById('question_type').value;
        question_display.innerHTML = '';
        question_display.classList.remove('border');
        document.getElementById('results').classList.remove('border');
        document.querySelectorAll('input[name="user-answer"][type="radio"]').forEach(radio => {
            radio.checked = false;
        });
        if (!type) {
            question_display.innerHTML = '<p>Please select a question type.</p>';
            return;
        }
        fetch(`questionrandomtest.php?type=${encodeURIComponent(type)}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    question_display.innerHTML = `<p>Error: ${data.error}</p>`;
                    hideAnswerInput();
                } else {
                    question_display.innerHTML = `
                        <h3>Question:</h3><p>${data.Question}</p>
                    `;
                    correctAnswer = data.Answer.trim().toLowerCase();
                    explanation = data.Explanation;
                    showAnswerInput();
                    document.getElementById('results').innerHTML = '';
                    document.getElementById('user-answer').value = '';
                    question_display.classList.add('border');
                }
            })
            .catch(() => {
                question_display.innerHTML = '<p>Error fetching data.</p>';
                hideAnswerInput();
            });
    }

// Checks answer
    function submit_answer() {
        let userAnswer = '';
        const results = document.getElementById('results');
        results.style.display = 'block';
        if (document.getElementById('user-answer').style.display === 'block') {
            userAnswer = document.getElementById('user-answer').value.trim().toLowerCase();
            if (userAnswer === '') {
        results.innerHTML = 'Please enter your answer.';
        return;
    }
        }
        else if (document.getElementById('radio-answer').style.display === 'block') {
            const selected_radio = document.querySelector('input[name="user-answer"]:checked');
            if (selected_radio) {
                userAnswer = selected_radio.value.toLowerCase();
            } else {
                results.innerHTML = 'Please select your answer.';
                return;
            }
        } else {
            console.error('No answer input is visible.');
            esults.innerHTML = "An unexpected error occurred. Please try again."; // User feedback
            return;
        }
        let resultMsg = '';
        if (userAnswer === correctAnswer) {
            results.classList.add('border');
            resultMsg = `<span style="color:green;">Correct!</span>`;
        } else {
            results.classList.add('border');
            resultMsg = `<span style="color:red;">Incorrect.</span> The correct answer was: <b>${correctAnswer}</b>`;
        }
        resultMsg += `<br><h4>Explanation:</h4><p>${explanation}</p>`;
        document.getElementById('results').innerHTML = resultMsg;
        }

// Show answer input based on question type
    function showAnswerInput() {
        document.getElementById('answer-label').style.display = 'block';
        if (
            document.getElementById('question_type').value == "Wordform" ||
            document.getElementById('question_type').value == "Rearrangement" ||
            document.getElementById('question_type').value == "Sentence_transformation"
        ) {
            document.getElementById('user-answer').style.display = 'block';
        } else {
            document.getElementById('radio-answer').style.display = 'block';
        }
        document.getElementById('submit-btn').style.display = 'block';
    }
// Hide answer input and explaination when no question is selected
    function hideAnswerInput() {
        document.getElementById('answer-label').style.display = 'none';
        document.getElementById('user-answer').style.display = 'none';
        document.getElementById('radio-answer').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('results').style.display = 'none';
    }


// Combines 2 function
    function fetchAndhide() {
        fetch_question();
        hideAnswerInput();
    }