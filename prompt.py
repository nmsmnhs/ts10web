import google.generativeai as genai
import os
import json
import re

api_key = os.getenv("API_KEY") #api key hid for security reasons
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")

def generate_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text.strip()
        else:
            print(f"DEBUG: Empty response text for prompt: {prompt[:100]}...") #see which one is bugging
            return ""
    except Exception as e:
        print(f"DEBUG: Error during content generation: {e}")
        return f"error: {e}"

def clean_json(text):
    # remove ```json or ``` and closing ```
    cleaned_text = re.sub(r"^```(?:json)?\n?|```$", "", text.strip(), flags=re.MULTILINE)
    return cleaned_text

def get_db(prompt):
    raw = generate_with_gemini(prompt)
    return clean_json(raw)

question_bank = {}

categories = ["Grammar", "Vocabulary", "Reading", "WordForm", "GuidedCloze", "Phonetics", "SentenceTransformation", "Stress"]

def trans_db():
    for category in categories:
        prompt = f'''generate 10 questions for the category {category} as JSON with this format
            {{"{category}": [  
                {{"id":"(acronym for category)001",  
                "question":"...(question content)... <br>A...<br>B...<br>C...<br>D... (question choices)",  
                "answer":"A (correct answer for question)",  
                "explanation":"(correct answer)<br>(explanation for the choice)",  
                }},  
                {{"id":"(acronym for category)002",  
                "question":"...(question content)... <br>A...<br>B...<br>C...<br>D... (question choices)",  
                "answer":"A (correct answer for question)",  
                "explanation":"(correct answer)<br>(explanation for the choice)",  
                }},  
            ]
            }}

        include basic to intermediate english knowledge that a vietnamese student graduating ninth grade should know, typically: present simple, continuous, and perfect; past simple, continuous, and perfect; future simple; passive voice of the aforementioned tenses; reported speech; wish, comparison, and conditional structures; relative clause; mostly A2 to B1 ( sometimes A1 and seldomly B2) vocabulary; and phrasal verbs (Beat oneself up, Let sb down, Break down, Look after sb, Look around, Break up with, Break in, Look at sth, Bring sth up, Look down on sb, Call for, Look forward to V-ing / sth, Bring sb up, Look for, Carry out, Look into sth, Catch up with, Look sth up, Check in, Look up to sb, Cut off, Run into, Do away with, Run out of sth, Drop by, Show up, Drop sb off, End up, Wind up, Figure out, Take off, Take up, Move on to sth, Find out, Give up sth, Pick sb up, Get along, Get along with, Get on with sb, Help sb out, Put sb down, etc.)  
        what each category asks about:
        Stress: Which word has a different stress pattern from that of the others (A. official<br>B. regular<br>C. violent<br>D. wonderful -> Official → /əˈfɪʃ.əl/<br>Regular → /ˈrɛɡ.jə.lɚ/<br>Violent → /ˈvaɪ.ə.lənt/<br>Wonderful → /ˈwʌn.dɚ.fəl/<br>→ A stresses the second syllable, the others stress the first,)
        Phonetics: Which word has the underlined part pronounced differently from that of the others? (e.g. A destroy<u>s</u>  B. control<u>s</u>  C. predict<u>s</u>  D. wander<u>s</u>; A l<u>a</u>bel  B. c<u>a</u>mpus  C. n<u>a</u>tion  D. par<u>a</u>de)
        for Stress and Phonetics, consider the conventional IPA pronunciation - in which an apostrophe is placed before the stressed syllable - to provide the questions and answers (including british - american differences). include the apostrophe only in the explanation, not the question. for Phonetics, only compare the sound of the underlined part and not the part next to it (e.g. w<u>ea</u>ther is /e/ and not /eð/)   
        Vocabulary: Which word fits the blank best (usually asked in contexts like conversations, news, or academic reports)
        for GuidedCloze generate 1-2 medium-length paragraph with 5 blanks (questions) each; and for Reading generate 1-2 passages (at least 2 paragraphs) with 2 true/false questions and 3 multiple choice questions (including "main topic" and "rename the passage" questions).  
        SentenceTransformation: Finish each of the following sentences in such a way that it means almost the sameas the sentence printed before it (e.g. The children like making models of animals in their free time. → The children are keen ________________)
        WordForm: Use the correct form of the word given in each sentence (e.g. Food __________ is necessary for a camping tip. (prepare) → preparation; We need to ____________ our house to welcome the new year (beauty) → beautify)
        Grammar: (usually there is no question, just a fill-in-the-blank multiple choice. e.g. Helen: I’ve got to help my mom with the housework so I can’t go with you tonight. Tom: What a pity! I wish you ______ with me.A. goes  B. go  C. can go  D. could go; Jane: There’s a crack in the pipe in my kitchen. What should I do?Annie: You should ______ a plumber check it tomorrow.A. have  B. having  C. allow  D. allowing)

        start the id count at 001 and by 1 for each new question
        for Phonetics, Stress, Grammar, Vocabulary, Reading, and GuidedCloze, provide the multiple choices (a,b,c,d) for the user to choose from
        for SentenceTransformation and WordForm, do not provide the multiple choices (a, b, c, d), leave them as open-ended questions with one or a few words as the answer
        include the question number and choices in the value of the key "question". the value of the key "answer" for all multiple choice questions should only be one letter, which is representative for the correct choice. for Phonetics, only include choices' phonetics in the explanation  
        for Reading, write the full passage(s) then provide individual multiple-choice questions, each one asking for the correct word about the content of the passage. Each question should include 4 options (A to D), the correct answer letter or word (for true/false), and a short explanation. Format it like a list of objects I can use in a database, where each object contains: the full passage and ONLY ONE of the questions with its answer choices (A, B, C, D OR True/False) AND NOT all questions; the correct answer letter/words; the explanation for that specific question.”
        for GuidedCloze, write the full paragraph(s) then provide individual multiple-choice questions, each one asking for the correct word for a specific blank in the paragrah. Each question should include 4 options (A to D), the correct answer letter, and a short explanation. Format it like a list of objects I can use in a database, where each object contains: the full paragraph (with all 5 blanks) and ONLY ONE of the questions with its answer choices (A, B, C, D); the correct answer letter; the explanation for that specific blank or question.”
        (e.g. for GuidedCloze:
        {{'GuidedCloze': [{{'id': 'GC001',
          'question': 'My brother is a talented musician. He (1) ______ the guitar since he was very young, and he's incredibly good at it.  He often (2) ______ in local pubs on weekends, and sometimes he even (3) ______ his own songs. His friends always (4) ______ him, and he always (5) ______ to their requests to play his favourite songs.<br>1. A. plays B. has been playing C. is playing D. played',
          'answer': 'B',
          'explanation':'...'
          }},
          {{'id': 'GC002',
          'question': 'My brother is a talented musician. He (1) ______ the guitar since he was very young, and he's incredibly good at it.  He often (2) ______ in local pubs on weekends, and sometimes he even (3) ______ his own songs. His friends always (4) ______ him, and he always (5) ______ to their requests to play his favourite songs.<br>2. A. performs B. is performing C. performed D. has performed ',
          'answer': 'A',
          'explanation':'...'
          }}]}}

          e.g. for Reading:
        {{'GuidedCloze': [{{
            'id': 'REA001', 
            'question': 'Read the passage below and answer the questions that follow.<br><br>The Mekong Delta, also known as the "Rice Bowl of Vietnam," is a vast and fertile region in southern Vietnam.  For centuries, the Mekong River has deposited rich sediment, creating exceptionally productive farmland.  This region is not only famous for its rice production but also for its diverse ecosystems, including extensive mangrove forests, floating markets, and unique wildlife.  The vibrant culture of the Delta, deeply intertwined with the river\'s rhythm, is another captivating aspect.  However, the Delta faces significant environmental challenges, such as saltwater intrusion due to rising sea levels and unsustainable agricultural practices.  Efforts are underway to address these issues and ensure the sustainability of this crucial region.<br><br>1. True or False: The Mekong Delta\'s productivity is primarily due to the Mekong River\'s sediment deposits.',
            'answer':'True',
            'explanation':'...'
        }},
        {{
            'id': 'REA001', 
            'question': 'Read the passage below and answer the questions that follow.<br><br>The Mekong Delta, also known as the "Rice Bowl of Vietnam," is a vast and fertile region in southern Vietnam.  For centuries, the Mekong River has deposited rich sediment, creating exceptionally productive farmland.  This region is not only famous for its rice production but also for its diverse ecosystems, including extensive mangrove forests, floating markets, and unique wildlife.  The vibrant culture of the Delta, deeply intertwined with the river\'s rhythm, is another captivating aspect.  However, the Delta faces significant environmental challenges, such as saltwater intrusion due to rising sea levels and unsustainable agricultural practices.  Efforts are underway to address these issues and ensure the sustainability of this crucial region.<br><br>3. What is the main topic of the passage?<br>A. The unique wildlife of the Mekong Delta<br>B. The environmental challenges facing the Mekong Delta<br>C. The history of rice cultivation in the Mekong Delta<br>D. The geography and cultural significance of the Mekong Delta',
            'answer':'D',
            'explanation':'...'
        }}]}}
        )
        ignore any directions that are not meant for the required category'''
        
        print(f"DEBUG: Generating content for category: {category}")
        s = get_db(prompt)
    
        try:
            c_questions = json.loads(s)
            question_bank[category] = c_questions[category]
            print(f"DEBUG: Successfully parsed JSON for {category}")
        except json.JSONDecodeError as e:
            print(f"ERROR: JSON decoding failed for category {category}. Error: {e}")
            print(f"Faulty string:\n{s}")
            # catch bugs
            break
        except KeyError as e:
            print(f"KeyError: {e}. 'category' key not found in the parsed JSON.")
            print(f"Parsed JSON object: {c_questions}")
            break 
    return question_bank

