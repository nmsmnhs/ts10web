    let correctAnswer = '';
    let explanation = '';

    document.getElementById('fetch-btn').addEventListener('click', fetch_questionAndShowUI);
    document.getElementById('submit-btn').addEventListener('click', submit_answer);

    // Get question
    async function fetch_question() {
        const question_display = document.getElementById('question-display');
        const type = document.getElementById('question_type').value;
        question_display.innerHTML = '';
        question_display.classList.remove('border');
        document.getElementById('results').classList.remove('border');

        if (!type) {
            question_display.innerHTML = '<p>Please select a question type.</p>';
            return null;
        }

        try {
            const response = await fetch(`questionrandomtest.php?type=${encodeURIComponent(type)}`);
            const data = await response.json();

            if (data.error) {
                question_display.innerHTML = `<p>Error: ${data.error}</p>`;
                return null;
            } else {
                return data;
            }
        } catch (error) {
            question_display.innerHTML = '<p>Error fetching data.</p>';
            return null;
        }
    }

    function displayQuestion(data) {
        const question_display = document.getElementById('question-display');
        question_display.innerHTML = `
            <h3>Question:</h3><p>${data.Question}</p>
        `;
        question_display.classList.add('border');
    }

    function showAnswerInput(questionType) {
        document.getElementById('answer-label').style.display = 'block';
        document.getElementById('user-answer').style.display = 'none';
        document.getElementById('radio-answer').style.display = 'none';

        if (questionType === "Wordform" || questionType === "Rearrangement" || questionType === "Sentence_transformation") {
            document.getElementById('user-answer').style.display = 'block';
        } else if (questionType) {
            document.getElementById('radio-answer').style.display = 'block';
            // Clear radio buttons
            document.querySelectorAll('input[name="user-answer"][type="radio"]').forEach(radio => {
                radio.checked = false;
            });
        }
        document.getElementById('submit-btn').style.display = 'block';
    }

    function hideAnswerUI() {
        document.getElementById('answer-label').style.display = 'none';
        document.getElementById('user-answer').style.display = 'none';
        document.getElementById('radio-answer').style.display = 'none';
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('results').style.display = 'none';
    }

    async function fetch_questionAndShowUI() {
        hideAnswerUI();
        const questionData = await fetch_question();
        if (questionData) {
            correctAnswer = questionData.Answer.trim().toLowerCase();
            explanation = questionData.Explanation;
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
                results.innerHTML = 'Please enter your answer.';
                return;
            }
        } else if (document.getElementById('radio-answer').style.display === 'block') {
            const selectedRadio = document.querySelector('input[name="user-answer"]:checked');
            if (selectedRadio) {
                userAnswer = selectedRadio.value.toLowerCase();
            } else {
                results.innerHTML = 'Please select your answer.';
                return;
            }
        } else {
            console.error('No answer input is visible.');
            results.innerHTML = "An unexpected error occurred. Please try again."; // User feedback
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
        results.innerHTML = resultMsg;
    }