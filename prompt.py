import google.generativeai as genai

# initialize with your API key
genai.configure(api_key="AIzaSyBmSwTIkBu_DckMfQceWxZ3FEdvKNVdMS8")

# choose the model
model = genai.GenerativeModel("gemini-2.0-flash-lite")

def generate_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"error: {e}"
    
def base_prompt(category):
    return f'''closely follow the format given below (especially the explanation) and generate 1 questions for the category {category} as an array (exclude the category name)

Ignore the references that are not for the required category



{

"Grammar": [

{

"question": "Helen: I've got to help my mom with the housework so I can't go with you tonight.\nTom: What a pity! I wish you _____ with me.\nA. goes\nB. go\nC. can go\nD. could go",

"answer": "D",

"explanation": "Cấu trúc Wish ở hiện tại: S + wish + S + V-ed/V2 \ncould = can V2"

},

{

"question": "Jane: There's a crack in the pipe in my kitchen. What should I do?\nAnnie: You should _____ a plumber check it tomorrow\nA. have\nB. having\nC. allow\nD. allowing",

"answer": "A",

"explanation": "Have + somebody + V0: yêu cầu ai làm gì"

}

],

"Vocabulary": [

{

"question": "David: Which natural __________usually occurs in the United States?\nNancy: Tornados quite often strike the nation.\nA. pollution \nB. Disaster \nC. extinction \nD. hurricane",

"answer": "B",

"explanation": "B. disaster (n): thiên tai\nDavid: Thiên tai nào thường xảy ra ở Hoa Kỳ?\nNancy: Lốc xoáy khá thường xuyên tấn công quốc gia."

},

{

"question": "Mark: What do you think about your Chemistry teacher?\nHelen: He’s great. He always __________ his students to do their best.\nA. encourages \nB. sends \nC. lets \nD. makes",

"answer": "A",

"explanation": "A. encourages (v): khuyến khích \nMark: Bạn nghĩ gì về giáo viên Hóa học của mình?\nHelen: Thầy ấy rất tuyệt. Thầy luôn khuyến khích các học trò của mình cố gắng hết sức."

}

],

"Reading": [

{

"question": "The boy in the family was responsible for buying Mother a silk hat as a gift.",

"answer": "T",

"explanation": "I was so excited with the idea that I was the person who bought Mother a new silk hat from the money Father had secretly given to me before."

},

{

"question": "The passage is about __________________.\nA. how the family prepared a Mother's Day\nB. what holiday is the best for the family\nC. how exciting a drive to the country was\nD. when people celebrate Mother's Day",

"answer": "A",

"explanation": "how the family prepared a Mother's Day: gia đình đã chuẩn bị Ngày của Mẹ như thế nào"

}

],

"Wordform": [

{

"question": "We need to our house to welcome the new year _______ (beauty)",

"answer": "beautifully",

"explanation": "welcome là verb → cần adverb để bổ nghĩa → dùng beautifully"

},

{

"question": "AI like Chat GPT is believed to be __________ in the search of information. (benefit)",

"answer": "Beneficial",

"explanation": "benefit là verb-> cần tính từ -> beneficial\nTạm dịch: AI như Chat GPT được cho là có ích trong việc tìm kiếm thông tin."

}

],

"Rearrangement": [

{

"question": "India, downing trees / and power lines, causing /has hit / widespread damage/ a powerful cyclone /./\n-> A powerful cyclone__________",

"answer": "has hit India, downing trees and power lines, causing widespread damage.",

"explanation": "India: nước Ấn Độ\ndowning trees: làm đổ cây\npower lines: dây điện\ncausing + N: gây ra cái gì đó \nwidespread damage: thiệt hại trên diện rộng\nA powerful cyclone: Một cơn bão lốc xoáy mạnh\nTạm dịch: Một cơn bão lốc xoáy mạnh đã tấn công Ấn Độ, làm đổ cây và dây điện, gây thiệt hại trên diện rộng."

},

{

"question": "that family members/ a celebration/ Tet is so important/ try to come back home/ living apart/./\n=> Tet is so important _____________________.",

"answer": "a celebration that family members living apart try to come back home.",

"explanation": "S + V + so + adj + a + noun (đếm được số ít) + that + S + V"

}

],

"GuidedCloze": [

{

"question": "Good evening. Welcome to our Fun Science Program. This week we have received a lot of questions about life on the moon. We have talked to some experts and these are what we have (17) ___________ out. There is no water or air on the moon. It is all silent (18) ___________ there is no air. Of course there will be no music, no sounds. There are no rivers and no lakes. At night it is very cold. The (19) _____________ goes down to 151°C below zero. But during the day it rises to 100°C above zero.\n\nThere are great round holes on the moon. They are called craters. There are more than 30,000 of them. There are also high mountains. The (20) ___________ mountains on the moon are about 26,000 feet or 8,000 meters.\n\nAnd here is something very interesting for you (21) ____________: on the moon you weigh one sixth of what you weigh on the earth. If you weigh 50 kilos, on the moon you will weigh only a little more than 8 kilos. You will be able to jump very high, (22) ___________ higher than any high jump Olympic champions. You can take very long steps as well. And ... Maybe you won't sleep very well because one day on the moon lasts two weeks. So, is there life on the moon? I'll leave the question for you to answer yourselves in the group discussion.\n17.\n\nA. found B. known C. brought D. learned",

"answer": "A",

"explanation": "A. found (v): tìm \nB. known (v): biết \nC. brought (v): mua \nD. learned (v): học\nTạm dịch: Chúng tôi đã nói chuyện với một số chuyên gia và đây là những gì chúng tôi đã tìm ra."

},

{

"question": "Good evening. Welcome to our Fun Science Program. This week we have received a lot of questions about life on the moon. We have talked to some experts and these are what we have (17) ___________ out. There is no water or air on the moon. It is all silent (18) ___________ there is no air. Of course there will be no music, no sounds. There are no rivers and no lakes. At night it is very cold. The (19) _____________ goes down to 151°C below zero. But during the day it rises to 100°C above zero.\n\nThere are great round holes on the moon. They are called craters. There are more than 30,000 of them. There are also high mountains. The (20) ___________ mountains on the moon are about 26,000 feet or 8,000 meters.\n\nAnd here is something very interesting for you (21) ____________: on the moon you weigh one sixth of what you weigh on the earth. If you weigh 50 kilos, on the moon you will weigh only a little more than 8 kilos. You will be able to jump very high, (22) ___________ higher than any high jump Olympic champions. You can take very long steps as well. And ... Maybe you won't sleep very well because one day on the moon lasts two weeks. So, is there life on the moon? I'll leave the question for you to answer yourselves in the group discussion.\n18.\n\nA. but B. because C. though D. while",

"answer": "B",

"explanation": "A. but: nhưng \nB. because: bởi vi \nC. though: mặc dù \nD. while: trong khi\nTạm dịch: Tất cả đều im lặng vì không có không khí."

}

],

"Phonetics": [

{"question":"Which word has the underlined part pronounced differently from that of the others? \nA. destroys \nB. controls \nC. predicts \nD. wanders",

"answer": "c",

"explanation":"Sounds ending in: /f/, /k/ /p/, /t/, /θ/: s is pronounced as /s/\nSounds ending in: /s/, /t∫/, /dʒ/, /z/, / ∫ /, /ʒ/: s is pronounced as /iz/\nThe remaining sounds: s is pronounced as /z/\n\n→ destroys, controls, wanders: /z/\npredicts: /s/",

},

{"question":"Which word has the underlined part pronounced differently from that of the others?\nA. mentioned\nB. consisted \nC. described \nD. studied",

"answer":"b",

"explanation":"A. mentioned /ˈmenʃnd/\nB. consisted /kənˈsɪstid/\nC. described /dɪˈskraɪbd/\nD. studied /ˈstʌdid/\nPhương án B phát âm là /id/, còn lại là /d/"

}

],

"Stress": [

{"question":"Which word has a different stress pattern from that of the others?\nA. official\nB. regular\nC. violent\nD. wonderful",

"answer": "a",

"explanation":"Official → /əˈfɪʃ.əl/\nRegular → /ˈrɛɡ.jə.lɚ/\nViolent → /ˈvaɪ.ə.lənt/\nWonderful → /ˈwʌn.dɚ.fəl/\n→ A stresses the second syllable, the others stress the first",

},

{"question":"Which word has a different stress pattern form that of the others?\nA. refresh\nB. intend\nC. excite\nD. eager",

"answer":"d",

"explanation":"A. refresh /rɪˈfreʃ/\nB. intend /ɪnˈtend/\nC. excite /ɪkˈsaɪt/\nD. eager /ˈiːɡə(r)/\nPhương án D có trọng âm rơi vào âm tiết thứ 1, còn lại là 2.",

}

],

"Sentence_transformation": [

{"question":"Change the way you learn vocabulary, and you can improve your English.\n=> If you _____________________________",

"answer":"change the way you learn vocabulary, you can improve your english.",

"explanation":"Câu điều kiện loại 1: If + S + V(hiện tại đơn), S + can/ will + V-infinitive"

},

{"question":"“Why don’t we collect those empty bottles for recycling?” said Robert.\n=> Robert suggested that those _________________",

"answer":"empty bottles should be collected for recycling.",

"explanation":"Cấu trúc “suggest”: S + suggest + that + S + V + O"

}

]

}



for GuidedCloze generate 1 medium-length distinct paragraphs with 4-5 blanks (questions) each; and for Reading generate 1 passages (at least 2 paragraphs) with 2 true/false questions and 2-3 multiple choice questions (including "main topic" and "rename the passage" questions). Include the entire passage/paragraph in each of the questions even if only one blank is being asked about. include the choices in the value of the key "question". for Phonetics, only include choices' phonetics in the explanation

include basic to intermediate english knowledge that a vietnamese student graduating ninth grade should know, typically: present simple, continuous, and perfect; past simple, continuous, and perfect; future simple; passive voice of the aforementioned tenses; reported speech; wish, comparison, and conditional structures; relative clause; mostly A2 to B1 ( sometimes A1 and seldomly B2) vocabulary; and phrasal verbs (Beat oneself up, Let sb down, Break down, Look after sb, Look around, Break up with, Break in, Look at sth, Bring sth up, Look down on sb, Call for, Look forward to V-ing / sth, Bring sb up, Look for, Carry out, Look into sth, Catch up with, Look sth up, Check in, Look up to sb, Cut off, Run into, Do away with, Run out of sth, Drop by, Show up, Drop sb off, End up, Wind up, Figure out, Take off, Take up, Move on to sth, Find out, Give up sth, Pick sb up, Get along, Get along with, Get on with sb, Help sb out, Put sb down, etc.)
'''